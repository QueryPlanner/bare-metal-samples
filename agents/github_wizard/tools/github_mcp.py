import os
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

def _get_github_mcp_tools():
    github_token = os.getenv("GITHUB_TOKEN")
    tools = []
    if github_token:
        tools = [
            McpToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url="https://api.githubcopilot.com/mcp/",
                    headers={"Authorization": f"Bearer {github_token}"}
                )
            )
        ]
    else:
        print("Warning: GITHUB_TOKEN not found. GitHub MCP tools will not be available.")
    return tools

github_mcp_tools = _get_github_mcp_tools()
