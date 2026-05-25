# MCP Server Template

## Overview
This template shows the basic structure of an MCP (Model Context Protocol) server. Use this as a reference for building your own MCPs.

## What You'll Learn

1. **Server Structure**: How to initialize and run an MCP server
2. **Tool Definition**: How to define tools with proper schema
3. **Tool Implementation**: How to implement tool logic
4. **Error Handling**: Best practices for handling errors
5. **Testing**: How to test your MCP server

## Key Components

### 1. Tool Definition
Every tool needs:
- **name**: Unique identifier
- **description**: What it does (for the AI model)
- **inputSchema**: JSON Schema defining parameters

### 2. Tool Handler
Function that:
- Receives tool name and arguments
- Executes the logic
- Returns results or errors

### 3. Server Lifecycle
- Initialize server
- Register tools
- Handle requests
- Shut down gracefully

## Template Files

- `mcp_server_template.py` - Complete MCP server skeleton
- `mcp_tool_template.py` - Individual tool structure

## Common Mistakes to Avoid

❌ **Wrong**: Missing required fields in schema
✅ **Right**: Complete schema with type, description, required

❌ **Wrong**: No error handling
✅ **Right**: Try-catch with meaningful error messages

❌ **Wrong**: Hardcoded values
✅ **Right**: Parameterized, configurable inputs

## Quick Reference

```python
# Define a tool
tool = {
    "name": "my_tool",
    "description": "Tool description",
    "inputSchema": {
        "type": "object",
        "properties": {
            "input_param": {"type": "string"}
        },
        "required": ["input_param"]
    }
}

# Register tool
tools.append(tool)

# Handle execution
if tool_name == "my_tool":
    return execute_my_tool(arguments)
```
