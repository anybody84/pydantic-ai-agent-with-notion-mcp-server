import json

from pydantic_ai.mcp import MCPServerStdio


class NotionMCPServerStdio(MCPServerStdio):
    """
    MCP server for Notion.
    This server is used to interact with Notion's API to fetch data.
    It runs a Docker container with the Notion MCP server and sets the necessary headers for authentication.
    """

    def __init__(self, token: str, notion_version: str = "2022-06-28", **kwargs):
        super().__init__(
            command="docker",
            args=["run", "--rm", "-i", "-e", "OPENAPI_MCP_HEADERS", "mcp/notion"],
            env={
                "OPENAPI_MCP_HEADERS": json.dumps(
                    {"Authorization": f"Bearer {token}", "Notion-Version": notion_version}
                )
            },
            **kwargs,
        )
