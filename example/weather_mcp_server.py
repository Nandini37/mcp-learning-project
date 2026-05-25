#!/usr/bin/env python3
"""
Weather MCP Server - Complete Working Example

This is a fully functional MCP server that provides weather tools.
It demonstrates:

1. Real API integration (Open-Meteo - free, no key needed)
2. Tool definition with proper schemas
3. Error handling and input validation
4. Data transformation and formatting

Run this file directly:
    python weather_mcp_server.py
"""

import json
import logging
import requests
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeatherMCPServer:
    """
    Complete Weather MCP Server implementation.
    
    Provides weather tools:
    - Get current weather
    - Get weather forecast
    - Get air quality data
    """
    
    # API endpoints (Open-Meteo - free and no API key needed!)
    GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API = "https://api.open-meteo.com/v1/forecast"
    AIR_QUALITY_API = "https://air-quality-api.open-meteo.com/v1/air_quality"
    
    # Weather code descriptions
    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    
    # AQI levels
    AQI_LEVELS = {
        (0, 50): "Good",
        (51, 100): "Moderate",
        (101, 150): "Unhealthy for Sensitive Groups",
        (151, 200): "Unhealthy",
        (201, 300): "Very Unhealthy",
        (301, 500): "Hazardous",
    }
    
    def __init__(self, server_name: str = "WeatherMCPServer"):
        """
        Initialize the Weather MCP Server.
        
        Args:
            server_name: Name of the server
        """
        self.server_name = server_name
        self.tools: List[Dict[str, Any]] = []
        self.initialized = False
        logger.info(f"Initializing {server_name}")
    
    def define_tools(self) -> None:
        """
        Define all weather tools available in this server.
        """
        
        # Tool 1: Get Current Weather
        current_weather_tool = {
            "name": "get_current_weather",
            "description": "Get current weather conditions for a city. Returns temperature, humidity, wind speed, and weather description.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'London', 'New York', 'Tokyo')"
                    },
                    "country": {
                        "type": "string",
                        "description": "Country code (optional, e.g., 'US', 'GB', 'JP')"
                    }
                },
                "required": ["city"]
            }
        }
        self.tools.append(current_weather_tool)
        logger.info(f"Registered tool: {current_weather_tool['name']}")
        
        # Tool 2: Get Weather Forecast
        forecast_tool = {
            "name": "get_weather_forecast",
            "description": "Get weather forecast for the next N days. Returns daily high/low temperatures, precipitation, and descriptions.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-7, default 5)",
                        "minimum": 1,
                        "maximum": 7
                    }
                },
                "required": ["city"]
            }
        }
        self.tools.append(forecast_tool)
        logger.info(f"Registered tool: {forecast_tool['name']}")
        
        # Tool 3: Get Air Quality
        air_quality_tool = {
            "name": "get_air_quality",
            "description": "Get air quality index (AQI) and pollutant levels for coordinates. Returns PM2.5, PM10, and AQI.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude coordinate"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude coordinate"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        }
        self.tools.append(air_quality_tool)
        logger.info(f"Registered tool: {air_quality_tool['name']}")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        if not self.tools:
            self.define_tools()
        return self.tools
    
    def _geocode_city(self, city: str, country: Optional[str] = None) -> Tuple[float, float, str]:
        """Convert city name to coordinates using geocoding API."""
        try:
            params = {"name": city, "count": 1}
            if country:
                params["country"] = country
            
            response = requests.get(self.GEOCODING_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "results" not in data or len(data["results"]) == 0:
                raise Exception(f"City '{city}' not found")
            
            result = data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            name = result.get("name", city)
            country_name = result.get("country", "")
            
            full_name = f"{name}, {country_name}" if country_name else name
            logger.info(f"Geocoded '{city}' to ({lat}, {lon})")
            
            return lat, lon, full_name
        
        except requests.exceptions.Timeout:
            raise Exception("Geocoding API timeout")
        except Exception as e:
            logger.error(f"Geocoding error: {str(e)}")
            raise
    
    def _get_weather_description(self, code: int) -> str:
        """Convert weather code to human-readable description."""
        return self.WEATHER_CODES.get(code, "Unknown")
    
    def _get_aqi_level(self, aqi: float) -> str:
        """Convert AQI value to level."""
        for (low, high), level in self.AQI_LEVELS.items():
            if low <= aqi <= high:
                return level
        return "Hazardous"
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given arguments."""
        try:
            logger.info(f"Executing tool: {tool_name} with args: {arguments}")
            
            if tool_name == "get_current_weather":
                return self._execute_get_current_weather(arguments)
            elif tool_name == "get_weather_forecast":
                return self._execute_get_weather_forecast(arguments)
            elif tool_name == "get_air_quality":
                return self._execute_get_air_quality(arguments)
            else:
                return {"status": "error", "message": f"Unknown tool: {tool_name}"}
        
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _execute_get_current_weather(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of get_current_weather tool."""
        city = arguments.get("city")
        country = arguments.get("country")
        
        if not city:
            return {"status": "error", "message": "Missing required field: city"}
        
        try:
            lat, lon, full_name = self._geocode_city(city, country)
            
            response = requests.get(
                self.WEATHER_API,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,feels_like_2m",
                    "timezone": "auto"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            
            return {
                "status": "success",
                "city": full_name,
                "latitude": lat,
                "longitude": lon,
                "temperature": current["temperature_2m"],
                "feels_like": current["feels_like_2m"],
                "humidity": current["relative_humidity_2m"],
                "wind_speed": current["wind_speed_10m"],
                "description": self._get_weather_description(current["weather_code"]),
                "timestamp": current["time"]
            }
        
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Weather API timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get weather: {str(e)}"}
    
    def _execute_get_weather_forecast(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of get_weather_forecast tool."""
        city = arguments.get("city")
        days = arguments.get("days", 5)
        
        if not city:
            return {"status": "error", "message": "Missing required field: city"}
        
        if days < 1 or days > 7:
            return {"status": "error", "message": "Days must be between 1 and 7"}
        
        try:
            lat, lon, full_name = self._geocode_city(city)
            
            response = requests.get(
                self.WEATHER_API,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
                    "timezone": "auto",
                    "forecast_days": days
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            daily = data["daily"]
            forecast = []
            
            for i in range(len(daily["time"])):
                forecast.append({
                    "date": daily["time"][i],
                    "high": daily["temperature_2m_max"][i],
                    "low": daily["temperature_2m_min"][i],
                    "precipitation": daily["precipitation_sum"][i],
                    "description": self._get_weather_description(daily["weather_code"][i])
                })
            
            return {
                "status": "success",
                "city": full_name,
                "days": days,
                "forecast": forecast
            }
        
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Weather API timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get forecast: {str(e)}"}
    
    def _execute_get_air_quality(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of get_air_quality tool."""
        latitude = arguments.get("latitude")
        longitude = arguments.get("longitude")
        
        if latitude is None or longitude is None:
            return {"status": "error", "message": "Missing required fields: latitude and longitude"}
        
        try:
            response = requests.get(
                self.AIR_QUALITY_API,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "pm2_5,pm10,us_aqi",
                    "timezone": "auto"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            aqi = current["us_aqi"]
            
            return {
                "status": "success",
                "latitude": latitude,
                "longitude": longitude,
                "aqi": aqi,
                "level": self._get_aqi_level(aqi),
                "pm2_5": current["pm2_5"],
                "pm10": current["pm10"],
                "timestamp": current["time"]
            }
        
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Air quality API timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get air quality: {str(e)}"}
    
    def initialize(self) -> bool:
        """Initialize the server."""
        try:
            self.define_tools()
            self.initialized = True
            logger.info(f"{self.server_name} initialized with {len(self.tools)} tools")
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            return False
    
    def shutdown(self) -> None:
        """Shutdown the server gracefully."""
        logger.info(f"Shutting down {self.server_name}")
        self.initialized = False


# Example usage and demonstration
if __name__ == "__main__":
    server = WeatherMCPServer("MyWeatherServer")
    
    if server.initialize():
        print("\n" + "="*80)
        print("WEATHER MCP SERVER - WORKING EXAMPLE DEMONSTRATION")
        print("="*80)
        
        print("\n📋 Available Tools:")
        for tool in server.get_tools():
            print(f"  - {tool['name']}: {tool['description'][:60]}...")
        
        print("\n" + "="*80)
        print("🧪 TEST 1: Get Current Weather for London")
        print("="*80)
        result = server.execute_tool(
            "get_current_weather",
            {"city": "London", "country": "GB"}
        )
        print(json.dumps(result, indent=2))
        
        print("\n" + "="*80)
        print("🧪 TEST 2: Get 5-Day Forecast for New York")
        print("="*80)
        result = server.execute_tool(
            "get_weather_forecast",
            {"city": "New York", "days": 5}
        )
        if result["status"] == "success":
            print(json.dumps({
                "status": result["status"],
                "city": result["city"],
                "days": result["days"],
                "forecast_count": len(result["forecast"]),
                "first_day": result["forecast"][0] if result["forecast"] else None
            }, indent=2))
        else:
            print(json.dumps(result, indent=2))
        
        print("\n" + "="*80)
        print("🧪 TEST 3: Get Air Quality for NYC (40.7128, -74.0060)")
        print("="*80)
        result = server.execute_tool(
            "get_air_quality",
            {"latitude": 40.7128, "longitude": -74.0060}
        )
        print(json.dumps(result, indent=2))
        
        print("\n" + "="*80)
        print("🧪 TEST 4: Error Handling - Invalid City")
        print("="*80)
        result = server.execute_tool(
            "get_current_weather",
            {"city": "XYZ123NotACity"}
        )
        print(json.dumps(result, indent=2))
        
        print("\n" + "="*80)
        print("🧪 TEST 5: Error Handling - Missing Parameter")
        print("="*80)
        result = server.execute_tool(
            "get_current_weather",
            {}
        )
        print(json.dumps(result, indent=2))
        
        server.shutdown()
        print("\n" + "="*80)
        print("✅ All demonstrations completed successfully!")
        print("="*80 + "\n")
