# AI Coding Assistant with Decoupled LangGraph Agent and MCP Tool Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 

This project demonstrates a powerful and flexible architecture for building AI agents, specifically an AI Coding Assistant. It features a **LangGraph** agent for orchestrating workflows, decoupled from a **Model Context (MCP)** tool server that handles actual tool execution. Communication between the agent and the tool server is achieved in real-time using **Server-Sent Events (SSE)**, and the tool server is **Dockerized** for ease of deployment and scalability.

**GitHub Repository:** [https://github.com/human-ai2025/AI-Coding-Assistant](https://github.com/human-ai2025/AI-Coding-Assistant)

## Table of Contents

-   [Overview](#overview)
-   [Key Features](#key-features)
-   [Architecture](#architecture)
-   [How It Works](#how-it-works)
-   [Tech Stack](#tech-stack)
-   [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Running the MCP Tool Server (Docker)](#running-the-mcp-tool-server-docker)
    -   [Running the LangGraph Agent](#running-the-langgraph-agent)
-   [Usage Example](#usage-example)
-   [Future Enhancements](#future-enhancements)
-   [Contributing](#contributing)
-   [License](#license)

## Overview

The primary goal of this project is to showcase a robust architecture where AI agent logic (LangGraph) is separated from tool execution (MCP server). This decoupling offers significant advantages:

*   **Modularity:** Tools can be developed, updated, and scaled independently.
*   **Scalability:** Tool servers can be scaled based on demand without affecting the agent.
*   **Flexibility:** Different tool servers (potentially in different languages) can be integrated.
*   **Real-time Interaction:** SSE enables live streaming of tool outputs and logs to the agent.

This AI Coding Assistant can leverage tools (like a terminal executor) hosted on the MCP server to perform tasks requested by the user, orchestrated by the LangGraph agent.

## Key Features

*   **Decoupled Architecture:** Separation of concerns between agent orchestration and tool execution.
*   **Model Context Protocol (MCP):** A standardized way for agents to discover and interact with tools.
*   **LangGraph Orchestration:** Leverages the power of LangGraph to define complex agentic workflows.
*   **Server-Sent Events (SSE):** Enables real-time, unidirectional communication from the MCP server to the LangGraph agent for streaming logs and results.
*   **Dockerized Tool Server:** The MCP tool server (e.g., `terminal_server.py`) is containerized for portability and easy deployment.
*   **Extensible Toolset:** Designed to easily integrate new tools into the MCP server.

## Architecture

The system consists of two main components:

1.  **LangGraph Agent:**
    *   Receives user requests.
    *   Orchestrates the workflow using a graph-based state machine.
    *   Decides when to call a tool.
    *   Communicates with the MCP Tool Server to execute tools.
    *   Processes tool results and formulates a response.

2.  **MCP Tool Server (Dockerized):**
    *   Exposes tools (e.g., a terminal execution tool) via the Model Context Protocol.
    *   Listens for requests from the LangGraph agent.
    *   Executes the requested tool with the provided parameters.
    *   Streams output, logs, and results back to the LangGraph agent using Server-Sent Events (SSE).

```
+---------------------+                         I       +---------------------+
|     User / Client   |<------------------------------->|  LangGraph Agent    |
+---------------------+                                 | (e.g., agent.py)    |
                                                        +----------^----------+
                                                                   |
                                           Tool Invocation Request |
                                           (e.g., HTTP POST)       |
                                                                   | SSE Connection
                                                                   V (for streaming results)
+------------------------------------------------------------------+
| Docker Container                                                 |
| +--------------------------------------------------------------+ |
| | MCP Tool Server (e.g., terminal_server.py)                   | |
| | - Listens for tool calls                                     | |
| | - Executes tools (e.g., run terminal command)                | |
| | - Streams output via SSE                                     | |
| +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

## How It Works

1.  A user interacts with the LangGraph agent (e.g., through a CLI or an API exposed by the agent).
2.  The LangGraph agent processes the input and, based on its defined workflow, determines that a specific tool needs to be executed.
3.  The LangGraph agent sends a request to the MCP Tool Server, specifying the tool name and its parameters. This initial request might be a standard HTTP call.
4.  The MCP Tool Server receives the request and invokes the corresponding tool.
5.  As the tool executes, the MCP Tool Server streams any output, logs, or intermediate results back to the LangGraph agent over an established Server-Sent Events (SSE) connection.
6.  The LangGraph agent receives these real-time updates, processes them, and can update its state or decide on further actions.
7.  Once the tool execution is complete and the agent's workflow finishes, a final response is provided to the user.

## Tech Stack

*   **Python:** Core programming language.
*   **LangChain & LangGraph:** For AI agent orchestration and state management.
*   **MCP (Model Context Protocol):** Custom implementation for tool interaction.
*   **Server-Sent Events (SSE):** For real-time communication from server to client (MCP server to LangGraph agent).
*   **Docker:** For containerizing and deploying the MCP Tool Server.


## Getting Started

### Prerequisites

*   [Git](https://git-scm.com/)
*   [Python](https://www.python.org/downloads/) (3.9+ recommended)
*   [Docker](https://www.docker.com/get-started)
*   `uv` 
*    `langGraph`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/human-ai2025/AI-Coding-Assistant.git
    cd AI-Coding-Assistant
    ```

2.  **Set up a Python virtual environment (recommended):**
    ```bash
    uv venv
    uv sync (assuming you have the toml file)
    ```


### Running the MCP Tool Server (Docker)

The `terminal_server.py` is designed to be run inside a Docker container.

1.  **Build the Docker image:**
    (Ensure your `Dockerfile` is correctly configured to copy necessary files and expose the correct port, e.g., 8080 )
    ```bash
    docker build -t mcp-tool-server .
    ```

2.  **Run the Docker container:**
    (Replace `8080` with the port your MCP server listens on if different)
    ```bash
    docker run -d -p 8080:8080  D:\devlopment\mcp\workspace:/root/mcp/workspace terminal_server
    ```
    *   `-d`: Run in detached mode.
    *   `-p 8080:8080`: Map port 8080 on the host to port 8080 in the container.
    *   `-v  D:\devlopment\mcp\workspace:/root/mcp/workspace terminal_server` : mount volume 

### Running the LangGraph Agent

1.  **Configure Agent (if needed):**
    Ensure your LangGraph agent script (e.g., `client/client.py`) is configured with the correct URL for the MCP Tool Server 

2.  **Run the agent script:**
    ```bash
    cd client
    uv run client.py http://localhost:8080/sse
    ```

## Usage Example

Once both the MCP Tool Server (in Docker) and the LangGraph Agent are running:

1.  Interact with your LangGraph agent (this might be through a command-line interface it provides, or by sending requests if it exposes an API).
2.  **Example Interaction (Conceptual):**
    *   **User to Agent:** "List files in the /tmp directory."
    *   **LangGraph Agent:** Determines it needs the `terminal_tool`.
    *   **LangGraph Agent to MCP Server:** Sends request: `{ "tool": "terminal_tool", "command": "ls /tmp" }` (or similar structure).
    *   **MCP Server (terminal_tool):** Executes `ls /tmp`.
    *   **MCP Server to LangGraph Agent (via SSE):**
        ```
        data: {"type": "stdout", "content": "file1.txt\n"}
        data: {"type": "stdout", "content": "another_dir\n"}
        data: {"type": "log", "content": "Command execution started."}
        data: {"type": "result", "content": "Execution successful", "exit_code": 0}
        ```
    *   **LangGraph Agent:** Processes the streamed output and final result, then presents it to the user.


## Future Enhancements

*   **More Tools:** Implement additional tools for the MCP server (e.g., file I/O, git operations, API clients).
*   **Authentication & Authorization:** Secure the MCP server endpoints.
*   **Observability:** Integrate logging, tracing, and metrics for better monitoring.
*   **Error Handling & Resilience:** Improve error handling in both the agent and the server.
*   **Multi-Modal Tools:** Extend MCP and tools to support image/audio inputs/outputs.


## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please make sure your code adheres to any existing style guidelines and includes tests where appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
references:
1. https://www.youtube.com/watch?v=s0YJNcT1XMA
