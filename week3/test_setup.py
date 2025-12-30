"""Simple test script to verify the Weather MCP Server setup."""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from week3.server.weather_client import WeatherClient, WeatherAPIError


async def test_weather_client():
    """Test the weather client functionality."""
    print("=" * 60)
    print("Weather MCP Server - Setup Verification")
    print("=" * 60)
    print()
    
    # Check for API key
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENWEATHER_API_KEY environment variable not set!")
        print()
        print("Please set your API key:")
        print("  export OPENWEATHER_API_KEY='your_api_key_here'")
        print()
        print("Or create a .env file in week3/ directory")
        return False
    
    print(f"✓ API key found: {api_key[:8]}...")
    print()
    
    try:
        # Initialize client
        print("Initializing Weather Client...")
        client = WeatherClient(api_key)
        print("✓ Client initialized successfully")
        print()
        
        # Test current weather
        print("Testing get_current_weather for London...")
        weather = client.get_current_weather(city="London,GB", units="metric")
        print("✓ Current weather retrieved successfully")
        print(f"  Location: {weather['location']['name']}, {weather['location']['country']}")
        print(f"  Temperature: {weather['current']['temperature']}°C")
        print(f"  Conditions: {weather['current']['description']}")
        print(f"  Humidity: {weather['current']['humidity']}%")
        print()
        
        # Test forecast
        print("Testing get_forecast for Tokyo...")
        forecast = client.get_forecast(city="Tokyo,JP", units="metric")
        print("✓ Forecast retrieved successfully")
        print(f"  Location: {forecast['location']['name']}, {forecast['location']['country']}")
        print(f"  Total forecast entries: {forecast['total_entries']}")
        print(f"  First forecast: {forecast['forecasts'][0]['timestamp']}")
        print(f"  First forecast temp: {forecast['forecasts'][0]['temperature']}°C")
        print()
        
        # Test with coordinates
        print("Testing with coordinates (New York)...")
        weather_coords = client.get_current_weather(lat=40.7128, lon=-74.0060, units="imperial")
        print("✓ Coordinate-based query successful")
        print(f"  Location: {weather_coords['location']['name']}")
        print(f"  Temperature: {weather_coords['current']['temperature']}°F")
        print()
        
        client.close()
        
        print("=" * 60)
        print("✅ All tests passed! Your Weather MCP Server is ready to use.")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Configure your MCP client (e.g., Claude Desktop)")
        print("2. Restart the client")
        print("3. Start using the weather tools!")
        print()
        return True
        
    except WeatherAPIError as e:
        print(f"❌ Weather API Error: {e}")
        print()
        print("Common issues:")
        print("- Invalid API key (check if it's activated)")
        print("- Rate limit exceeded (wait a moment)")
        print("- Network connectivity issues")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Try to load .env file if python-dotenv is available
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded environment from {env_path}")
            print()
    except ImportError:
        pass
    
    success = asyncio.run(test_weather_client())
    sys.exit(0 if success else 1)
