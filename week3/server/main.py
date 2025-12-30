"""Weather MCP Server - Provides weather data through Model Context Protocol."""

import os
import sys
import logging
import json
from typing import Any, Optional
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio

from .weather_client import WeatherClient, WeatherAPIError, RateLimitError

# Configure logging to stderr (stdout is reserved for MCP communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


class WeatherMCPServer:
    """MCP Server for weather data."""
    
    def __init__(self):
        """Initialize the Weather MCP Server."""
        self.server = Server("weather-server")
        self.weather_client: Optional[WeatherClient] = None
        
        # Register tool handlers
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register MCP tools with their handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available weather tools."""
            return [
                Tool(
                    name="get_current_weather",
                    description=(
                        "Get current weather conditions for a specific location. "
                        "Provide either a city name or latitude/longitude coordinates. "
                        "Returns temperature, humidity, wind speed, conditions, and more."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": (
                                    "City name. Can include country code for precision "
                                    "(e.g., 'London', 'New York,US', 'Tokyo,JP')"
                                )
                            },
                            "lat": {
                                "type": "number",
                                "description": "Latitude coordinate (-90 to 90)"
                            },
                            "lon": {
                                "type": "number",
                                "description": "Longitude coordinate (-180 to 180)"
                            },
                            "units": {
                                "type": "string",
                                "enum": ["metric", "imperial", "standard"],
                                "description": (
                                    "Units of measurement: "
                                    "metric (Celsius, m/s), "
                                    "imperial (Fahrenheit, mph), "
                                    "standard (Kelvin, m/s). Default: metric"
                                ),
                                "default": "metric"
                            }
                        },
                        "oneOf": [
                            {"required": ["city"]},
                            {"required": ["lat", "lon"]}
                        ]
                    }
                ),
                Tool(
                    name="get_weather_forecast",
                    description=(
                        "Get 5-day weather forecast with 3-hour intervals. "
                        "Provide either a city name or latitude/longitude coordinates. "
                        "Returns timestamped forecasts including temperature, conditions, "
                        "and precipitation probability."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": (
                                    "City name. Can include country code for precision "
                                    "(e.g., 'London', 'Paris,FR', 'Beijing,CN')"
                                )
                            },
                            "lat": {
                                "type": "number",
                                "description": "Latitude coordinate (-90 to 90)"
                            },
                            "lon": {
                                "type": "number",
                                "description": "Longitude coordinate (-180 to 180)"
                            },
                            "units": {
                                "type": "string",
                                "enum": ["metric", "imperial", "standard"],
                                "description": (
                                    "Units of measurement: "
                                    "metric (Celsius, m/s), "
                                    "imperial (Fahrenheit, mph), "
                                    "standard (Kelvin, m/s). Default: metric"
                                ),
                                "default": "metric"
                            }
                        },
                        "oneOf": [
                            {"required": ["city"]},
                            {"required": ["lat", "lon"]}
                        ]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            logger.info(f"Tool called: {name} with arguments: {arguments}")
            
            try:
                # Initialize weather client if not already done
                if self.weather_client is None:
                    self.weather_client = WeatherClient()
                
                if name == "get_current_weather":
                    result = await self._handle_current_weather(arguments)
                elif name == "get_weather_forecast":
                    result = await self._handle_forecast(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except ValueError as e:
                error_msg = f"Invalid input: {str(e)}"
                logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]
            
            except RateLimitError as e:
                error_msg = (
                    f"Rate limit exceeded: {str(e)}\n"
                    "Please wait a moment before making another request."
                )
                logger.warning(error_msg)
                return [TextContent(type="text", text=error_msg)]
            
            except WeatherAPIError as e:
                error_msg = f"Weather API error: {str(e)}"
                logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]
            
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                logger.exception(error_msg)
                return [TextContent(type="text", text=error_msg)]
    
    async def _handle_current_weather(self, arguments: dict) -> dict:
        """Handle get_current_weather tool call."""
        city = arguments.get("city")
        lat = arguments.get("lat")
        lon = arguments.get("lon")
        units = arguments.get("units", "metric")
        
        result = self.weather_client.get_current_weather(
            city=city,
            lat=lat,
            lon=lon,
            units=units
        )
        
        # Add units information to the result
        result["units"] = self._get_units_info(units)
        
        return result
    
    async def _handle_forecast(self, arguments: dict) -> dict:
        """Handle get_weather_forecast tool call."""
        city = arguments.get("city")
        lat = arguments.get("lat")
        lon = arguments.get("lon")
        units = arguments.get("units", "metric")
        
        result = self.weather_client.get_forecast(
            city=city,
            lat=lat,
            lon=lon,
            units=units
        )
        
        # Add units information to the result
        result["units"] = self._get_units_info(units)
        
        return result
    
    @staticmethod
    def _get_units_info(units: str) -> dict:
        """Get units information for the response."""
        units_map = {
            "metric": {
                "temperature": "Celsius",
                "wind_speed": "m/s",
                "pressure": "hPa",
                "humidity": "%"
            },
            "imperial": {
                "temperature": "Fahrenheit",
                "wind_speed": "mph",
                "pressure": "hPa",
                "humidity": "%"
            },
            "standard": {
                "temperature": "Kelvin",
                "wind_speed": "m/s",
                "pressure": "hPa",
                "humidity": "%"
            }
        }
        return units_map.get(units, units_map["metric"])
    
    async def run(self) -> None:
        """Run the MCP server using STDIO transport."""
        logger.info("Starting Weather MCP Server...")
        
        # Verify API key is available
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            logger.error(
                "OPENWEATHER_API_KEY environment variable is not set. "
                "The server will fail when tools are called."
            )
        else:
            logger.info("OpenWeatherMap API key found")
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("Server running on STDIO")
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the Weather MCP Server."""
    server = WeatherMCPServer()
    await server.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
