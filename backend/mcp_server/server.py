"""MCP server setup with tool registration for the Todo AI Chatbot."""

from mcp.server.fastmcp import FastMCP

from mcp_server.tools import add_task, complete_task, delete_task, list_tasks, update_task

mcp = FastMCP("todo-chatbot")

# Register tools
mcp.tool()(add_task)
mcp.tool()(list_tasks)
mcp.tool()(complete_task)
mcp.tool()(delete_task)
mcp.tool()(update_task)
