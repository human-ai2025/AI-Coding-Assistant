For docker containers of the mcp servers 
1. docker built -t terminal_server .
2. docker run --rm -p 8081:8081 -v D:\devlopment\mcp\workspace:/root/mcp/workspace terminal_server