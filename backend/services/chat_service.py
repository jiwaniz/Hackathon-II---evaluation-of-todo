"""Chat orchestration service - connects ADK agent with MCP tools and conversation persistence.

Stateless request cycle:
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent
4. Store user message in database
5. Run agent with MCP tools
6. Store assistant response in database
7. Return response to client
"""

import json
import logging

from google import genai
from google.genai import types
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
- add_task: Create a new task (requires title, optional description)
- list_tasks: View tasks (filter by status: "all", "pending", "completed")
- complete_task: Mark a task as done (requires task_id)
- delete_task: Remove a task (requires task_id)
- update_task: Change task title or description (requires task_id)

Guidelines:
- When a user mentions adding, creating, or remembering something, use add_task
- When a user asks to see, show, or list tasks, use list_tasks with appropriate filter
- When a user says done, complete, or finished, use complete_task
- When a user says delete, remove, or cancel, use delete_task
- When a user says change, update, or rename, use update_task
- Always confirm actions with a friendly response including task details
- If a user gives an ambiguous command (like "delete the meeting task"), use list_tasks first to find the right task, then perform the action
- If you cannot determine which task the user means, ask for clarification
- If a message is not related to task management, politely explain you can only help with tasks
- Format task lists in a clear, readable way
"""


def _build_tool_declarations() -> list[types.FunctionDeclaration]:
    """Build Gemini function declarations for MCP tools."""
    return [
        types.FunctionDeclaration(
            name="add_task",
            description="Create a new task for the user",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "title": types.Schema(type=types.Type.STRING, description="Task title (required)"),
                    "description": types.Schema(type=types.Type.STRING, description="Task description (optional)"),
                },
                required=["title"],
            ),
        ),
        types.FunctionDeclaration(
            name="list_tasks",
            description="Retrieve tasks with optional status filter",
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
            description="Mark a task as complete",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="The task ID to complete"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="delete_task",
            description="Remove a task permanently",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="The task ID to delete"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="update_task",
            description="Modify task title or description",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="The task ID to update"),
                    "title": types.Schema(type=types.Type.STRING, description="New title (optional)"),
                    "description": types.Schema(type=types.Type.STRING, description="New description (optional)"),
                },
                required=["task_id"],
            ),
        ),
    ]


def _execute_tool(tool_name: str, args: dict, user_id: str) -> str:
    """Execute an MCP tool by name with the given arguments."""
    from mcp_server.tools import add_task, complete_task, delete_task, list_tasks, update_task

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


def _get_gemini_client() -> genai.Client:
    """Create a Gemini client."""
    return genai.Client(api_key=settings.google_api_key)


def _get_groq_response(messages: list[dict], user_id: str) -> tuple[str, list[dict]]:
    """Fallback: use Groq for chat completion (without tool calling)."""
    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)

    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=groq_messages,
        max_tokens=1024,
    )

    return response.choices[0].message.content or "I'm sorry, I couldn't process that.", []


async def process_chat_message(
    session: Session,
    user_id: str,
    message: str,
    conversation_id: int | None = None,
) -> dict:
    """Process a chat message through the AI agent.

    Stateless cycle: fetch history → store user msg → run agent → store response → return.

    Args:
        session: Database session
        user_id: Authenticated user ID
        message: User's natural language message
        conversation_id: Existing conversation ID (creates new if None)

    Returns:
        Dict with conversation_id, response text, and tool_calls
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

    # Try Gemini first, fall back to Groq
    tool_calls_log = []
    try:
        response_text, tool_calls_log = await _run_gemini_agent(history_for_agent, user_id)
    except Exception as e:
        logger.warning(f"Gemini failed, falling back to Groq: {e}")
        try:
            response_text, tool_calls_log = _get_groq_response(history_for_agent, user_id)
        except Exception as groq_err:
            logger.error(f"Both Gemini and Groq failed: {groq_err}")
            response_text = "I'm sorry, I'm having trouble processing your request right now. Please try again in a moment."

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


async def _run_gemini_agent(messages: list[dict], user_id: str) -> tuple[str, list[dict]]:
    """Run the Gemini agent with function calling for MCP tools.

    Returns:
        Tuple of (response_text, tool_calls_log)
    """
    client = _get_gemini_client()

    tools = types.Tool(function_declarations=_build_tool_declarations())

    # Build contents from history
    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    tool_calls_log = []
    max_turns = 5  # Prevent infinite tool-calling loops

    for _ in range(max_turns):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[tools],
                temperature=0.7,
            ),
        )

        # Check if model wants to call a function
        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        if part.function_call:
            fc = part.function_call
            tool_name = fc.name
            tool_args = dict(fc.args) if fc.args else {}

            logger.info(f"Agent calling tool: {tool_name} with args: {tool_args}")

            # Execute the tool
            result = _execute_tool(tool_name, tool_args, user_id)

            tool_calls_log.append({
                "tool": tool_name,
                "input": tool_args,
                "output": json.loads(result),
            })

            # Add function call and result to contents for next turn
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
            # Model returned text response
            return part.text or "Done!", tool_calls_log

    # If we exhausted turns, return last response
    return "I've completed the operations. Is there anything else you'd like me to do?", tool_calls_log
