"""OpenWeatherMap API client with error handling and rate limiting."""

import os
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass


class RateLimitError(WeatherAPIError):
    """Exception raised when API rate limit is exceeded."""
    pass


class WeatherClient:
    """Client for interacting with OpenWeatherMap API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    RATE_LIMIT_DELAY = 1.0  # Minimum seconds between API calls
    REQUEST_TIMEOUT = 10.0  # Seconds
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the weather client.
        
        Args:
            api_key: OpenWeatherMap API key. If None, reads from OPENWEATHER_API_KEY env var.
        
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenWeatherMap API key is required. "
                "Set OPENWEATHER_API_KEY environment variable or pass api_key parameter."
            )
        
        self.last_request_time = 0.0
        self._client = httpx.Client(timeout=self.REQUEST_TIMEOUT)
    
    def _rate_limit(self) -> None:
        """Implement simple rate limiting to respect API limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.RATE_LIMIT_DELAY:
            sleep_time = self.RATE_LIMIT_DELAY - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make an API request with error handling.
        
        Args:
            endpoint: API endpoint path (e.g., 'weather', 'forecast')
            params: Query parameters for the request
        
        Returns:
            JSON response from the API
        
        Raises:
            WeatherAPIError: For API-related errors
            RateLimitError: When rate limit is exceeded
        """
        self._rate_limit()
        
        # Add API key to params
        params["appid"] = self.api_key
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            logger.info(f"Making request to {endpoint} with params: {params}")
            response = self._client.get(url, params=params)
            
            # Handle different error codes
            if response.status_code == 401:
                raise WeatherAPIError("Invalid API key. Please check your OPENWEATHER_API_KEY.")
            elif response.status_code == 404:
                raise WeatherAPIError("Location not found. Please check the city name or coordinates.")
            elif response.status_code == 429:
                raise RateLimitError("API rate limit exceeded. Please try again later.")
            elif response.status_code >= 400:
                raise WeatherAPIError(f"API error: {response.status_code} - {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except httpx.TimeoutException:
            raise WeatherAPIError(f"Request timeout after {self.REQUEST_TIMEOUT}s")
        except httpx.NetworkError as e:
            raise WeatherAPIError(f"Network error: {str(e)}")
        except Exception as e:
            if isinstance(e, (WeatherAPIError, RateLimitError)):
                raise
            raise WeatherAPIError(f"Unexpected error: {str(e)}")
    
    def get_current_weather(
        self,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        units: str = "metric"
    ) -> Dict[str, Any]:
        """Get current weather for a location.
        
        Args:
            city: City name (e.g., "London", "New York,US")
            lat: Latitude (alternative to city)
            lon: Longitude (must be provided with lat)
            units: Units of measurement (metric, imperial, standard)
        
        Returns:
            Dictionary containing weather data
        
        Raises:
            ValueError: If neither city nor coordinates are provided
            WeatherAPIError: For API-related errors
        """
        params = {"units": units}
        
        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("Either city name or lat/lon coordinates must be provided")
        
        data = self._make_request("weather", params)
        return self._format_current_weather(data)
    
    def get_forecast(
        self,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        units: str = "metric"
    ) -> Dict[str, Any]:
        """Get 5-day weather forecast for a location.
        
        Args:
            city: City name (e.g., "London", "New York,US")
            lat: Latitude (alternative to city)
            lon: Longitude (must be provided with lat)
            units: Units of measurement (metric, imperial, standard)
        
        Returns:
            Dictionary containing forecast data
        
        Raises:
            ValueError: If neither city nor coordinates are provided
            WeatherAPIError: For API-related errors
        """
        params = {"units": units}
        
        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("Either city name or lat/lon coordinates must be provided")
        
        data = self._make_request("forecast", params)
        return self._format_forecast(data)
    
    def _format_current_weather(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw API response into a clean structure."""
        return {
            "location": {
                "name": data.get("name", "Unknown"),
                "country": data.get("sys", {}).get("country", ""),
                "coordinates": {
                    "lat": data.get("coord", {}).get("lat"),
                    "lon": data.get("coord", {}).get("lon")
                }
            },
            "current": {
                "temperature": data.get("main", {}).get("temp"),
                "feels_like": data.get("main", {}).get("feels_like"),
                "temp_min": data.get("main", {}).get("temp_min"),
                "temp_max": data.get("main", {}).get("temp_max"),
                "pressure": data.get("main", {}).get("pressure"),
                "humidity": data.get("main", {}).get("humidity"),
                "description": data.get("weather", [{}])[0].get("description", ""),
                "wind_speed": data.get("wind", {}).get("speed"),
                "wind_deg": data.get("wind", {}).get("deg"),
                "cloudiness": data.get("clouds", {}).get("all"),
                "visibility": data.get("visibility"),
            },
            "timestamp": datetime.fromtimestamp(data.get("dt", 0)).isoformat(),
            "timezone": data.get("timezone", 0)
        }
    
    def _format_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format forecast API response into a clean structure."""
        forecasts = []
        for item in data.get("list", []):
            forecasts.append({
                "timestamp": datetime.fromtimestamp(item.get("dt", 0)).isoformat(),
                "temperature": item.get("main", {}).get("temp"),
                "feels_like": item.get("main", {}).get("feels_like"),
                "temp_min": item.get("main", {}).get("temp_min"),
                "temp_max": item.get("main", {}).get("temp_max"),
                "pressure": item.get("main", {}).get("pressure"),
                "humidity": item.get("main", {}).get("humidity"),
                "description": item.get("weather", [{}])[0].get("description", ""),
                "wind_speed": item.get("wind", {}).get("speed"),
                "wind_deg": item.get("wind", {}).get("deg"),
                "cloudiness": item.get("clouds", {}).get("all"),
                "pop": item.get("pop", 0) * 100,  # Probability of precipitation as percentage
            })
        
        return {
            "location": {
                "name": data.get("city", {}).get("name", "Unknown"),
                "country": data.get("city", {}).get("country", ""),
                "coordinates": {
                    "lat": data.get("city", {}).get("coord", {}).get("lat"),
                    "lon": data.get("city", {}).get("coord", {}).get("lon")
                }
            },
            "forecasts": forecasts,
            "total_entries": len(forecasts)
        }
    
    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
