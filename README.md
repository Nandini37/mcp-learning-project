# MCP Learning Project - Complete Guide

Welcome to the **Model Context Protocol (MCP) Learning Project**! This is a comprehensive end-to-end tutorial designed to teach interns how to build, test, and deploy MCP servers.

## 📚 Project Overview

This project contains:
- **Template Files**: Generic MCP structure to learn from
- **Working Example**: Fully functional Weather MCP server
- **Documentation**: Step-by-step learning guides
- **Test Cases**: Real examples with error handling

## 🎯 Learning Path

### Phase 1: Understand MCP Concepts (30 minutes)
1. Read `LEARNING_GUIDE.md` - MCP fundamentals
2. Study `template/README.md` - Template overview
3. Review `template/mcp_server_template.py` - Generic structure
4. Review `template/mcp_tool_template.py` - Tool patterns

### Phase 2: Run the Working Example (15 minutes)
1. Install dependencies: `pip install -r example/requirements.txt`
2. Run: `python example/weather_mcp_server.py`
3. Observe 5 different test cases (success + errors)
4. Read `example/README.md` - Understand each tool

### Phase 3: Modify & Experiment (30 minutes)
1. Add a new weather tool (e.g., `get_extreme_weather`)
2. Modify existing tool parameters
3. Add caching to reduce API calls
4. Test error cases

### Phase 4: Build Your Own (60+ minutes)
1. Create your own MCP (News, Sports, Stocks, etc.)
2. Use template as reference
3. Implement 3+ tools
4. Add comprehensive error handling
5. Test thoroughly

## 📁 Project Structure

```
mcp-learning-project/
├── README.md (this file)
├── LEARNING_GUIDE.md (foundational concepts)
├── template/
│   ├── README.md (template overview)
│   ├── mcp_server_template.py (generic server structure)
│   └── mcp_tool_template.py (tool patterns & examples)
├── example/
│   ├── README.md (weather example docs)
│   ├── requirements.txt (dependencies)
│   └── weather_mcp_server.py (fully working example)
└── .gitignore
```

## 🚀 Quick Start

### Option A: Just Run the Example
```bash
cd example
pip install -r requirements.txt
python weather_mcp_server.py
```

Expected output: 5 tests with weather data and error handling demos.

### Option B: Learn from Template
```bash
# Read the template structure
cat template/README.md

# Study generic server
python template/mcp_server_template.py

# Study tool patterns
python template/mcp_tool_template.py
```

### Option C: Full Learning Path
1. Read all READMEs in order
2. Run template examples
3. Run weather example
4. Modify weather example
5. Create your own MCP

## 🎓 What You'll Learn

### Concepts
- ✅ What is MCP and why it matters
- ✅ How tools are defined with JSON schemas
- ✅ How servers handle tool execution
- ✅ Error handling and validation
- ✅ Real API integration patterns

### Skills
- ✅ Reading and understanding schemas
- ✅ Implementing tool handlers
- ✅ Calling external APIs
- ✅ Data transformation
- ✅ Error handling best practices
- ✅ Testing and debugging

### Practical Experience
- ✅ Running production-like code
- ✅ Handling real API responses
- ✅ Validating user input
- ✅ Formatting output properly
- ✅ Logging and debugging

## 📖 File Descriptions

### `template/mcp_server_template.py`
**Purpose**: Generic MCP server skeleton

**Key Components**:
- `MCPServerTemplate` class
- `define_tools()` method
- `execute_tool()` method
- Example tools: echo, process_data

**Learning Focus**: Understanding server lifecycle and tool registration

### `template/mcp_tool_template.py`
**Purpose**: Individual tool structure patterns

**Key Components**:
- Abstract `MCPTool` base class
- `SimpleExampleTool` (add numbers)
- `AdvancedExampleTool` (calculator)
- Validation and error handling

**Learning Focus**: How to structure individual tools properly

### `example/weather_mcp_server.py`
**Purpose**: Production-ready weather MCP implementation

**Key Components**:
- `WeatherMCPServer` class
- Tool 1: `get_current_weather`
- Tool 2: `get_weather_forecast`
- Tool 3: `get_air_quality`
- Real API integration with Open-Meteo
- Comprehensive error handling

**Learning Focus**: Real-world implementation + API integration

## 🔧 How to Extend (Assignments)

### Assignment 1: Add New Tool
Add a `get_weather_alerts` tool to the weather server.

### Assignment 2: Add Caching
Cache results for 1 hour to reduce API calls.

### Assignment 3: Create Your Own MCP
Build an MCP for: News, Stocks, Sports, or Crypto

### Assignment 4: Add Retry Logic
Handle API timeouts with exponential backoff.

## 🧪 Testing Checklist

Before submitting, test:

- [ ] All tools execute without errors
- [ ] Tools return correct response format
- [ ] Invalid inputs handled gracefully
- [ ] Missing parameters raise errors
- [ ] API timeouts are caught
- [ ] External failures don't crash server
- [ ] Logging shows execution flow
- [ ] Response data formatted correctly
- [ ] Schema validation works
- [ ] Error messages are helpful

## 📚 Key Patterns

### Pattern 1: Tool Definition
```python
tool = {
    "name": "tool_name",
    "description": "What it does",
    "inputSchema": {
        "type": "object",
        "properties": {...},
        "required": [...]
    }
}
```

### Pattern 2: Tool Execution
```python
def execute_tool(self, tool_name, arguments):
    try:
        if tool_name == "my_tool":
            return self._execute_my_tool(arguments)
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Pattern 3: Input Validation
```python
if not arguments.get("required_field"):
    return {"status": "error", "message": "Missing: required_field"}
```

### Pattern 4: API Integration
```python
try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {"status": "success", "data": data}
except requests.exceptions.Timeout:
    return {"status": "error", "message": "API timeout"}
```

## 🐛 Debugging Tips

```python
# Check output
print(json.dumps(result, indent=2))

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Test components
lat, lon, name = server._geocode_city("London")
print(f"Geocoded: {lat}, {lon}, {name}")
```

## 🚨 Common Mistakes

| Mistake | Solution |
|---------|----------|
| Missing schema fields | Copy from examples, validate JSON |
| No error handling | Use try-except, always return status |
| Hardcoded values | Use parameters from arguments |
| Timeouts not handled | Add timeout=10 to requests.get() |
| Wrong data types | Use type hints, validate inputs |

## 📞 Resources

- [MCP Official Docs](https://modelcontextprotocol.io/)
- [Open-Meteo API](https://open-meteo.com/en/docs)
- [Python Requests Library](https://requests.readthedocs.io/)
- [JSON Schema Guide](https://json-schema.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## ✅ Success Criteria

You've mastered MCP when you can:

1. ✅ Explain what MCP is
2. ✅ Understand MCP schemas
3. ✅ Run the weather example
4. ✅ Modify an existing tool
5. ✅ Add a new tool
6. ✅ Handle errors gracefully
7. ✅ Call external APIs
8. ✅ Create your own MCP
9. ✅ Test thoroughly
10. ✅ Deploy to production

## 🎉 Next Steps

1. **Today**: Run the examples
2. **This Week**: Complete assignments 1-2
3. **Next Week**: Complete assignments 3-4
4. **Beyond**: Deploy MCPs, contribute to ecosystem

---

**Made with ❤️ for interns learning MCP**

Questions? Review guides, check examples, and experiment!
