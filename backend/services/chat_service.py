"""Chat orchestration service - connects AI agent with MCP tools and conversation persistence.

Stateless request cycle:
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent
4. Store user message in database
5. Run agent with MCP tools
6. Store assistant response in database
7. Return response to client

LLM priority: Gemini 2.0 Flash → Gemini 2.0 Flash-Lite → Groq (with tool calling)
"""

import json
import logging

from sqlmodel import Session

from config import settings
from models import MessageRole
from services.conversation_service import (
    add_message,
    create_conversation,
    get_conversation,
    get_messages,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful todo task management assistant. You help users manage their tasks through natural language conversation.

You have access to the following tools:
- add_task: Create a NEW task (requires title, optional description and priority). ONLY use this for brand new tasks.
- list_tasks: View tasks (filter by status: "all", "pending", "completed"). Returns task objects with numeric "id" fields.
- complete_task: Mark a task as done (requires task_id as an INTEGER, e.g. 42)
- delete_task: Remove a task (requires task_id as an INTEGER, e.g. 42)
- update_task: Change an EXISTING task's title, description, or priority (requires task_id as an INTEGER, e.g. 42)

CRITICAL RULES:
1. task_id MUST always be a numeric INTEGER (like 5, 12, 42). NEVER pass a task title string as task_id.
2. When a user wants to update, complete, delete, or modify an EXISTING task, you MUST call list_tasks FIRST to find the correct numeric task ID, then use the appropriate tool with that numeric ID.
3. NEVER use add_task when the user wants to update/modify/change an existing task. Use update_task instead.
4. NEVER use add_task when the user wants to complete an existing task. Use complete_task instead.

Guidelines:
- "add", "create", "new task", "remember to" → add_task (only for NEW tasks)
- "show", "list", "see my tasks", "what tasks" → list_tasks
- "done", "complete", "finished", "mark as done" → list_tasks first to get ID, then complete_task
- "delete", "remove", "cancel" → list_tasks first to get ID, then delete_task
- "change", "update", "rename", "edit", "modify" → list_tasks first to get ID, then update_task
- Always confirm actions with a friendly response including task details
- If a user refers to a task by name (like "complete the exam task"), ALWAYS call list_tasks first, find the matching task's numeric ID, then call complete_task/update_task/delete_task with that integer ID
- If you cannot determine which task the user means, ask for clarification
- If a message is not related to task management, politely explain you can only help with tasks
- Format task lists in a clear, readable way
- When a user first greets you or says "hi"/"hello", respond with a brief welcome and show example commands like:
  • "Create a task called Buy groceries with high priority"
  • "Show my tasks"
  • "Mark task Buy groceries as complete"
  • "Update task Buy groceries priority to low"
  • "Delete task Buy groceries"

IMPORTANT RESPONSE STYLE:
- Do NOT explain your reasoning, thinking process, or intermediate steps
- Do NOT show tool call names, parameters, or say things like "Let me call list_tasks first"
- Just perform the actions silently and give a brief, friendly confirmation of what was done
- Example good response: "Done! Updated 'Hackathon 2' priority to high."
- Example bad response: "I'll first call list_tasks to find the ID, then call update_task..."
"""


def _build_groq_tools() -> list[dict]:
    """Build OpenAI-compatible tool definitions for Groq."""
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user. ONLY for brand new tasks, never for updating existing ones.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Task title (required)"},
                        "description": {"type": "string", "description": "Task description (optional)"},
                        "priority": {"type": "string", "description": "Priority: 'high', 'medium', or 'low' (default: medium)", "enum": ["high", "medium", "low"]},
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve tasks with optional status filter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter: 'all', 'pending', or 'completed'",
                            "enum": ["all", "pending", "completed"],
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete. IMPORTANT: You MUST call list_tasks first to get the numeric task ID. task_id must be an integer like 5 or 42, NOT a task title.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The numeric task ID to complete. Get this from list_tasks. Example: 42"},
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Remove a task permanently. IMPORTANT: You MUST call list_tasks first to get the numeric task ID. task_id must be an integer like 5 or 42, NOT a task title.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The numeric task ID to delete. Get this from list_tasks. Example: 42"},
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Modify an EXISTING task's title, description, or priority. IMPORTANT: You MUST call list_tasks first to get the numeric task ID. NEVER use add_task to update an existing task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The numeric task ID to update. Get this from list_tasks. Example: 42"},
                        "title": {"type": "string", "description": "New title (optional)"},
                        "description": {"type": "string", "description": "New description (optional)"},
                        "priority": {"type": "string", "description": "New priority: 'high', 'medium', or 'low' (optional)", "enum": ["high", "medium", "low"]},
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]


def _execute_tool(tool_name: str, args: dict, user_id: str) -> str:
    """Execute an MCP tool by name with the given arguments."""
    from mcp_server.tools import add_task, complete_task, delete_task, list_tasks, update_task

    # Coerce task_id to int — LLMs sometimes pass strings like "42" or even task titles
    if "task_id" in args:
        try:
            args["task_id"] = int(args["task_id"])
        except (ValueError, TypeError):
            return json.dumps({"error": f"Invalid task_id '{args['task_id']}'. task_id must be a numeric integer. Use list_tasks to find the correct task ID."})

    tool_map = {
        "add_task": lambda a: add_task(user_id=user_id, **a),
        "list_tasks": lambda a: list_tasks(user_id=user_id, **a),
        "complete_task": lambda a: complete_task(user_id=user_id, **a),
        "delete_task": lambda a: delete_task(user_id=user_id, **a),
        "update_task": lambda a: update_task(user_id=user_id, **a),
    }

    handler = tool_map.get(tool_name)
    if not handler:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    return handler(args)


def _get_groq_response(messages: list[dict], user_id: str) -> tuple[str, list[dict]]:
    """Groq fallback with full tool calling support."""
    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)

    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages:
        # Only include user and assistant text messages (skip any tool-related history)
        if msg["role"] in ("user", "assistant") and msg.get("content"):
            groq_messages.append({"role": msg["role"], "content": msg["content"]})

    tools = _build_groq_tools()
    tool_calls_log = []
    max_turns = 5

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1024,
        )

        choice = response.choices[0]

        # If the model wants to call tools
        if choice.message.tool_calls:
            # Add assistant message with tool calls
            groq_messages.append(choice.message)

            for tc in choice.message.tool_calls:
                tool_name = tc.function.name
                try:
                    parsed = json.loads(tc.function.arguments) if tc.function.arguments else {}
                    tool_args = parsed if isinstance(parsed, dict) else {}
                except (json.JSONDecodeError, TypeError):
                    tool_args = {}

                logger.info(f"[Groq] Agent calling tool: {tool_name} with args: {tool_args}")

                try:
                    result = _execute_tool(tool_name, tool_args, user_id)
                except Exception as tool_err:
                    logger.error(f"[Groq] Tool {tool_name} execution error: {tool_err}")
                    result = json.dumps({"error": f"Tool execution failed: {str(tool_err)}"})

                try:
                    tool_calls_log.append({
                        "tool": tool_name,
                        "input": tool_args,
                        "output": json.loads(result),
                    })
                except json.JSONDecodeError:
                    tool_calls_log.append({
                        "tool": tool_name,
                        "input": tool_args,
                        "output": {"raw": result},
                    })

                # Add tool result as a message
                groq_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })
        else:
            # Model returned a text response
            return choice.message.content or "Done!", tool_calls_log

    return "I've completed the operations. Is there anything else?", tool_calls_log


async def process_chat_message(
    session: Session,
    user_id: str,
    message: str,
    conversation_id: int | None = None,
) -> dict:
    """Process a chat message through the AI agent.

    LLM priority: Gemini 2.0 Flash → Gemini 2.0 Flash-Lite → Groq with tools.
    """
    # Get or create conversation
    if conversation_id:
        conversation = get_conversation(session, conversation_id, user_id)
        if not conversation:
            conversation = create_conversation(session, user_id)
    else:
        conversation = create_conversation(session, user_id)

    # Store user message
    add_message(session, conversation.id, user_id, MessageRole.USER, message)

    # Fetch conversation history
    history = get_messages(session, conversation.id, user_id)
    history_for_agent = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history
    ]

    # Try Gemini models first, fall back to Groq
    tool_calls_log = []
    response_text = None

    logger.info(f"LLM keys: google_api_key={'SET' if settings.google_api_key else 'EMPTY'}, groq_api_key={'SET' if settings.groq_api_key else 'EMPTY'}")

    # Attempt 1: Gemini 2.0 Flash
    if settings.google_api_key:
        for model_name in ["gemini-2.0-flash", "gemini-2.0-flash-lite"]:
            try:
                logger.info(f"Trying {model_name}...")
                response_text, tool_calls_log = await _run_gemini_agent(
                    history_for_agent, user_id, model_name
                )
                logger.info(f"{model_name} succeeded")
                break
            except Exception as e:
                logger.warning(f"{model_name} failed: {e}")
                continue
    else:
        logger.warning("No GOOGLE_API_KEY configured, skipping Gemini")

    # Attempt 2: Groq with tool calling
    if response_text is None and settings.groq_api_key:
        try:
            logger.info("Trying Groq llama-3.3-70b-versatile...")
            response_text, tool_calls_log = _get_groq_response(history_for_agent, user_id)
            logger.info("Groq succeeded")
        except Exception as groq_err:
            logger.error(f"Groq also failed: {groq_err}", exc_info=True)
    elif response_text is None:
        logger.warning("No GROQ_API_KEY configured, skipping Groq")

    # Attempt 3: If tools-based Groq failed, try Groq without tools as last resort
    # Use a different system prompt that does NOT mention tools, to prevent fake tool output
    if response_text is None and settings.groq_api_key:
        try:
            logger.info("Trying Groq without tools as last resort...")
            from groq import Groq
            client = Groq(api_key=settings.groq_api_key)
            no_tools_prompt = (
                "You are a todo task assistant but your task management tools are temporarily unavailable. "
                "You CANNOT create, update, delete, list, or complete any tasks right now. "
                "Do NOT pretend to call any functions or show any tool outputs. "
                "Apologize briefly and ask the user to try again in a moment."
            )
            simple_messages = [{"role": "system", "content": no_tools_prompt}]
            for msg in history_for_agent[-4:]:
                if msg["role"] in ("user", "assistant") and msg.get("content"):
                    simple_messages.append({"role": msg["role"], "content": msg["content"]})
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=simple_messages,
                max_tokens=256,
            )
            response_text = resp.choices[0].message.content or "I'm having trouble with my tools right now. Please try again shortly."
            logger.info("Groq without tools succeeded (degraded mode)")
        except Exception as e:
            logger.error(f"Groq without tools also failed: {e}")

    if response_text is None:
        logger.error("ALL LLM providers failed or unconfigured — returning fallback error message")
        response_text = "I'm sorry, I'm having trouble right now. Please try again in a moment."

    # Store assistant response
    tool_calls_json = json.dumps(tool_calls_log) if tool_calls_log else None
    add_message(
        session,
        conversation.id,
        user_id,
        MessageRole.ASSISTANT,
        response_text,
        tool_calls=tool_calls_json,
    )

    return {
        "conversation_id": conversation.id,
        "response": response_text,
        "tool_calls": tool_calls_log,
    }


async def _run_gemini_agent(
    messages: list[dict], user_id: str, model_name: str = "gemini-2.0-flash"
) -> tuple[str, list[dict]]:
    """Run the Gemini agent with function calling for MCP tools."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.google_api_key)

    tool_declarations = [
        types.FunctionDeclaration(
            name="add_task",
            description="Create a NEW task. Only for brand new tasks, never for updating existing ones.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "title": types.Schema(type=types.Type.STRING, description="Task title (required)"),
                    "description": types.Schema(type=types.Type.STRING, description="Task description (optional)"),
                    "priority": types.Schema(type=types.Type.STRING, description="Priority: high, medium, or low", enum=["high", "medium", "low"]),
                },
                required=["title"],
            ),
        ),
        types.FunctionDeclaration(
            name="list_tasks",
            description="Retrieve tasks with optional status filter. Returns task objects with numeric id fields.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "status": types.Schema(
                        type=types.Type.STRING,
                        description="Filter: 'all', 'pending', or 'completed'",
                        enum=["all", "pending", "completed"],
                    ),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="complete_task",
            description="Mark a task as complete. Call list_tasks first to get the numeric task ID.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="The numeric task ID to complete"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="delete_task",
            description="Remove a task permanently. Call list_tasks first to get the numeric task ID.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="The numeric task ID to delete"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="update_task",
            description="Modify an existing task's title, description, or priority. Call list_tasks first to get the numeric task ID. Never use add_task to update.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="The numeric task ID to update"),
                    "title": types.Schema(type=types.Type.STRING, description="New title (optional)"),
                    "description": types.Schema(type=types.Type.STRING, description="New description (optional)"),
                    "priority": types.Schema(type=types.Type.STRING, description="New priority: high, medium, or low", enum=["high", "medium", "low"]),
                },
                required=["task_id"],
            ),
        ),
    ]

    tools = types.Tool(function_declarations=tool_declarations)

    # Build contents from history
    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    tool_calls_log = []
    max_turns = 5

    for _ in range(max_turns):
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[tools],
                temperature=0.7,
            ),
        )

        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        if part.function_call:
            fc = part.function_call
            tool_name = fc.name
            tool_args = dict(fc.args) if fc.args else {}

            logger.info(f"[{model_name}] Agent calling tool: {tool_name} with args: {tool_args}")

            result = _execute_tool(tool_name, tool_args, user_id)

            tool_calls_log.append({
                "tool": tool_name,
                "input": tool_args,
                "output": json.loads(result),
            })

            contents.append(candidate.content)
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=tool_name,
                        response=json.loads(result),
                    )],
                )
            )
        else:
            return part.text or "Done!", tool_calls_log

    return "I've completed the operations. Is there anything else?", tool_calls_log
