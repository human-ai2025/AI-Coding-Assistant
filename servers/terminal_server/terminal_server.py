import os
import subprocess 
from mcp.server.fastmcp import FastMCP  
from mcp.server import Server  
from mcp.server.sse import SseServerTransport 

from starlette.applications import Starlette  
from starlette.routing import Route, Mount 
from starlette.requests import Request 

import uvicorn 


mcp = FastMCP("terminal")

DEFAULT_WORKSPACE = os.path.expanduser("~/mcp/workspace")


@mcp.tool()
async def run_command(command: str) -> str:
    """
    Executes a shell command in the default workspace and returns the result.

    Args:
        command (str): A shell command like 'ls', 'pwd', etc.

    Returns:
        str: Standard output or error message from running the command.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=DEFAULT_WORKSPACE,
            capture_output=True,
            text=True
        )
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)



def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """
    Constructs a Starlette app with SSE and message endpoints.

    Args:
        mcp_server (Server): The core MCP server instance.
        debug (bool): Enable debug mode for verbose logs.

    Returns:
        Starlette: The full Starlette app with routes.
    """
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        """
        Handles a new SSE client connection and links it to the MCP server.
        """

        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send, 
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )


    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),       
            Mount("/messages/", app=sse.handle_post_message),  
        ],
    )



if __name__ == "__main__":
    mcp_server = mcp._mcp_server  

    import argparse

    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8081, help='Port to listen on')
    args = parser.parse_args()

    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)