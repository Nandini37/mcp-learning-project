# MCP Learning Guide for Interns

## What is MCP?
Model Context Protocol (MCP) is a standardized protocol that allows AI models to connect with external data sources and tools. It's like building a bridge between your AI application and external services.

## Project Structure

```
mcp-learning-project/
├── template/
│   ├── mcp_server_template.py       # Template to learn from
│   ├── mcp_tool_template.py         # Basic tool structure
│   └── README.md                    # Template documentation
├── example/
│   ├── weather_mcp_server.py        # Working weather example
│   ├── requirements.txt             # Dependencies
│   └── README.md                    # How to run example
└── LEARNING_GUIDE.md                # This file
```

## Learning Path

### Step 1: Understand the Template
- Read `template/README.md` - Explains MCP concepts
- Study `template/mcp_server_template.py` - Generic MCP structure
- Study `template/mcp_tool_template.py` - Tool definition pattern

### Step 2: Run the Working Example
- Read `example/README.md` - Understand weather MCP
- Install dependencies: `pip install -r example/requirements.txt`
- Run: `python example/weather_mcp_server.py`
- Test the tools

### Step 3: Modify & Experiment
- Modify the weather example to add new tools
- Create your own MCP server based on the template
- Test with different inputs

## Key Concepts

### 1. **MCP Server**
- Listens for requests from clients
- Executes tools/functions
- Returns results

### 2. **Tools**
- Functions exposed to the AI model
- Each tool has:
  - Name
  - Description
  - Input parameters
  - Implementation logic

### 3. **Resources** (Optional)
- Data sources that the model can access
- Files, APIs, databases, etc.

## Common MCP Patterns

```python
# Pattern 1: Define a tool
tool = {
    "name": "tool_name",
    "description": "What this tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter 1"}
        },
        "required": ["param1"]
    }
}

# Pattern 2: Implement tool execution
def execute_tool(tool_name, arguments):
    if tool_name == "tool_name":
        result = do_something(arguments["param1"])
        return result
```

## Debugging Tips

1. **Check logs**: Run with verbose mode
2. **Validate JSON**: Ensure schema is valid
3. **Test locally**: Run server and test directly
4. **Check dependencies**: Ensure all packages installed

## Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [GitHub Discussions](https://github.com/modelcontextprotocol/)
- Weather API: [OpenWeatherMap](https://openweathermap.org/api)

## Next Steps

Once you master this template, try building:
1. A database MCP server
2. An API wrapper MCP
3. A file system MCP
4. A custom domain-specific MCP
