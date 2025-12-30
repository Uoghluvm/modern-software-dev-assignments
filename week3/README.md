# Weather MCP Server

A Model Context Protocol (MCP) server that provides real-time weather data and forecasts using the OpenWeatherMap API.

## Overview

This MCP server exposes two powerful tools for accessing weather information:

- **`get_current_weather`**: Get current weather conditions for any location
- **`get_weather_forecast`**: Get a 5-day weather forecast with 3-hour intervals

The server runs locally using STDIO transport and can be integrated with any MCP-compatible client like Claude Desktop, Cursor, or custom applications.

## Features

✅ **Two Weather Tools**: Current conditions and 5-day forecast  
✅ **Flexible Location Input**: Support for city names or GPS coordinates  
✅ **Multiple Unit Systems**: Metric (Celsius), Imperial (Fahrenheit), or Standard (Kelvin)  
✅ **Error Handling**: Graceful handling of API failures, timeouts, and invalid inputs  
✅ **Rate Limiting**: Built-in rate limiting to respect API quotas  
✅ **Comprehensive Logging**: Detailed logging to stderr for debugging  
✅ **Type Safety**: Full type hints for better IDE support

## Prerequisites

- **Python**: 3.10 or higher
- **OpenWeatherMap API Key**: Free tier available at [openweathermap.org](https://openweathermap.org/api)

## Setup Instructions

### 1. Get an OpenWeatherMap API Key

1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to "API keys" section
4. Copy your API key (it may take a few minutes to activate)

### 2. Install Dependencies

```bash
cd week3
pip install -r requirements.txt
```

Or if you're using the project's Poetry environment:

```bash
cd /Users/thg/modern-software-dev-assignments
poetry install
```

### 3. Configure Environment Variables

Create a `.env` file in the `week3/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

**Security Note**: Never commit your `.env` file. It's already in `.gitignore`.

## Running the Server

### Local STDIO Mode

The server runs using STDIO transport, which is the standard way to integrate with MCP clients.

#### Option 1: Direct Python

```bash
cd week3
export OPENWEATHER_API_KEY="your_api_key_here"
python -m server.main
```

#### Option 2: Using Poetry (recommended)

```bash
cd /Users/thg/modern-software-dev-assignments
poetry run python -m week3.server.main
```

The server will start and listen for MCP protocol messages on STDIN/STDOUT.

## Configuring MCP Clients

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["-m", "week3.server.main"],
      "cwd": "/Users/thg/modern-software-dev-assignments",
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Alternative using Poetry**:

```json
{
  "mcpServers": {
    "weather": {
      "command": "poetry",
      "args": ["run", "python", "-m", "week3.server.main"],
      "cwd": "/Users/thg/modern-software-dev-assignments",
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

After saving, restart Claude Desktop. The weather tools should appear in the available tools list.

### Cursor IDE Configuration

If using Cursor, you can configure the MCP server in your workspace settings:

1. Open Settings → Extensions → MCP
2. Add a new server with the command and environment variables above

## Tool Reference

### 1. `get_current_weather`

Get current weather conditions for a location.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `city` | string | conditional* | City name, optionally with country code (e.g., "London", "New York,US") |
| `lat` | number | conditional* | Latitude coordinate (-90 to 90) |
| `lon` | number | conditional* | Longitude coordinate (-180 to 180) |
| `units` | string | optional | Units: "metric", "imperial", or "standard" (default: "metric") |

*Either `city` OR both `lat` and `lon` must be provided.

#### Example Inputs

**Using city name:**

```json
{
  "city": "Tokyo,JP",
  "units": "metric"
}
```

**Using coordinates:**

```json
{
  "lat": 51.5074,
  "lon": -0.1278,
  "units": "imperial"
}
```

#### Example Output

```json
{
  "location": {
    "name": "Tokyo",
    "country": "JP",
    "coordinates": {
      "lat": 35.6895,
      "lon": 139.6917
    }
  },
  "current": {
    "temperature": 15.5,
    "feels_like": 14.2,
    "temp_min": 13.0,
    "temp_max": 17.0,
    "pressure": 1013,
    "humidity": 65,
    "description": "partly cloudy",
    "wind_speed": 3.5,
    "wind_deg": 180,
    "cloudiness": 40,
    "visibility": 10000
  },
  "timestamp": "2025-12-30T15:04:00",
  "timezone": 32400,
  "units": {
    "temperature": "Celsius",
    "wind_speed": "m/s",
    "pressure": "hPa",
    "humidity": "%"
  }
}
```

### 2. `get_weather_forecast`

Get a 5-day weather forecast with data points every 3 hours.

#### Parameters

Same as `get_current_weather`.

#### Example Input

```json
{
  "city": "Paris,FR",
  "units": "metric"
}
```

#### Example Output

```json
{
  "location": {
    "name": "Paris",
    "country": "FR",
    "coordinates": {
      "lat": 48.8566,
      "lon": 2.3522
    }
  },
  "forecasts": [
    {
      "timestamp": "2025-12-30T18:00:00",
      "temperature": 8.5,
      "feels_like": 6.2,
      "temp_min": 7.0,
      "temp_max": 9.0,
      "pressure": 1015,
      "humidity": 75,
      "description": "light rain",
      "wind_speed": 4.2,
      "wind_deg": 220,
      "cloudiness": 85,
      "pop": 45.0
    },
    // ... more forecast entries (up to 40 data points)
  ],
  "total_entries": 40,
  "units": {
    "temperature": "Celsius",
    "wind_speed": "m/s",
    "pressure": "hPa",
    "humidity": "%"
  }
}
```

## Usage Examples

### In Claude Desktop

Once configured, you can ask Claude:

1. **"What's the current weather in London?"**
   - Claude will use `get_current_weather` with `city: "London"`

2. **"Give me a 5-day forecast for New York"**
   - Claude will use `get_weather_forecast` with `city: "New York,US"`

3. **"What's the weather at coordinates 40.7128, -74.0060?"**
   - Claude will use `get_current_weather` with the lat/lon parameters

4. **"Show me the forecast for Tokyo in Fahrenheit"**
   - Claude will use `get_weather_forecast` with `city: "Tokyo"` and `units: "imperial"`

### Testing the Server Manually

You can test the tools using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python -m week3.server.main
```

This opens a web UI where you can:

- View available tools
- Test tool calls with custom parameters
- See request/response details
- Debug any issues

## Error Handling

The server handles various error scenarios gracefully:

### Invalid API Key

```
Weather API error: Invalid API key. Please check your OPENWEATHER_API_KEY.
```

### Location Not Found

```
Weather API error: Location not found. Please check the city name or coordinates.
```

### Rate Limit Exceeded

```
Rate limit exceeded: API rate limit exceeded. Please try again later.
Please wait a moment before making another request.
```

### Network Issues

```
Weather API error: Request timeout after 10.0s
```

### Invalid Input

```
Invalid input: Either city name or lat/lon coordinates must be provided
```

## Rate Limiting

The server implements basic rate limiting:

- Minimum 1 second between API requests
- Automatic delay if requests come too quickly
- User-friendly error messages when API rate limits are hit

The free OpenWeatherMap tier allows:

- 60 calls/minute
- 1,000,000 calls/month

## Architecture

```
week3/
├── server/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # MCP server implementation
│   └── weather_client.py    # OpenWeatherMap API client
├── .env.example             # Environment variable template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Key Components

1. **`weather_client.py`**: HTTP client for OpenWeatherMap API
   - Handles authentication, rate limiting, and error handling
   - Formats raw API responses into clean structures
   - Provides type-safe interface

2. **`main.py`**: MCP server implementation
   - Registers and exposes MCP tools
   - Validates input parameters
   - Routes tool calls to weather client
   - Formats responses for MCP protocol

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio

# Run tests (to be implemented)
pytest week3/tests/
```

### Debugging

The server logs to stderr. To see debug output:

```bash
export OPENWEATHER_API_KEY="your_key"
python -m week3.server.main 2> debug.log
```

Then monitor the log file:

```bash
tail -f debug.log
```

## API Documentation

- **OpenWeatherMap Current Weather**: [https://openweathermap.org/current](https://openweathermap.org/current)
- **OpenWeatherMap 5-Day Forecast**: [https://openweathermap.org/forecast5](https://openweathermap.org/forecast5)
- **MCP Specification**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

## Limitations & Future Enhancements

### Current Limitations

- Free API tier limits to 60 calls/minute
- Forecast limited to 5 days / 3-hour intervals
- No caching (every request hits the API)

### Potential Enhancements

- [ ] Add caching to reduce API calls
- [ ] Implement HTTP transport for remote deployment
- [ ] Add more tools (air quality, historical data)
- [ ] Add authentication/authorization for HTTP mode
- [ ] Add comprehensive test suite
- [ ] Support for more weather data providers
- [ ] Add weather alerts and warnings

## Troubleshooting

### Server won't start

- Check that `OPENWEATHER_API_KEY` is set
- Verify Python version (3.10+)
- Ensure all dependencies are installed

### "Invalid API key" error

- Verify your API key is correct
- Wait a few minutes after creating a new key (activation delay)
- Check that the key is properly set in environment

### "Location not found"

- Check spelling of city name
- Try adding country code: "London,GB" instead of "London"
- Verify coordinates are in valid range

### No response from tools

- Check Claude Desktop configuration file syntax
- Restart Claude Desktop after config changes
- Check stderr logs for error messages

## License

This project is for educational purposes as part of the Modern Software Development course.

## Author

Created for Week 3 Assignment - MCP Server Implementation
