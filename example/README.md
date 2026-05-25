# Weather MCP Server - Working Example

## Overview
This is a **fully functional MCP server** that demonstrates real-world usage. It provides weather-related tools that an AI model can use.

## What This Example Teaches

✅ **API Integration** - How to call external APIs
✅ **Error Handling** - Graceful error management
✅ **Real Data Processing** - Working with actual weather data
✅ **Tool Composition** - Multiple related tools in one server

## Setup Instructions

### 1. Install Dependencies
```bash
cd example
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python weather_mcp_server.py
```

### 3. Expected Output
```
================================================================================
WEATHER MCP SERVER - WORKING EXAMPLE DEMONSTRATION
================================================================================

📋 Available Tools:
  - get_current_weather: Get current weather for a city
  - get_weather_forecast: Get weather forecast
  - get_air_quality: Get air quality index

✅ All demonstrations completed successfully!
```

## Tools Available

### Tool 1: `get_current_weather`
Get current weather for any city (no API key required!)

```python
result = server.execute_tool(
    "get_current_weather",
    {"city": "London", "country": "GB"}
)
```

### Tool 2: `get_weather_forecast`
Get 5-7 day weather forecast

```python
result = server.execute_tool(
    "get_weather_forecast",
    {"city": "New York", "days": 5}
)
```

### Tool 3: `get_air_quality`
Get air quality index for coordinates

```python
result = server.execute_tool(
    "get_air_quality",
    {"latitude": 40.7128, "longitude": -74.0060}
)
```

## Key Features

- ✅ **No API Key Required** - Uses free Open-Meteo API
- ✅ **Real Data** - Actual weather data from live APIs
- ✅ **Error Handling** - Graceful error messages
- ✅ **Geocoding** - Converts city names to coordinates
- ✅ **Data Formatting** - Human-readable output

## How It Works

1. Server defines tools with schemas
2. Client calls tool with city name
3. Server geocodes city to coordinates
4. Server fetches weather from API
5. Returns formatted result

## Error Handling Examples

### Success Case
```python
{"status": "success", "city": "London", "temperature": 15, ...}
```

### Error Case - City Not Found
```python
{"status": "error", "message": "City 'XYZ123' not found"}
```

### Error Case - Missing Parameter
```python
{"status": "error", "message": "Missing required field: city"}
```

## Next Steps for Learning

1. ✅ Run the example as-is
2. ✅ Modify to add a new weather tool
3. ✅ Add caching to avoid repeated API calls
4. ✅ Create your own MCP (News, Sports, Stocks, etc.)
5. ✅ Deploy to production

## Resources

- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Python Requests Library](https://requests.readthedocs.io/)
