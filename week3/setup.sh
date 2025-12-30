#!/bin/bash
# Setup script for Week 3 Weather MCP Server

echo "=========================================="
echo "Weather MCP Server - Setup Wizard"
echo "=========================================="
echo ""

# Check if API key is already set
if [ -f ".env" ]; then
    echo "✓ .env file already exists"
    source .env
    if [ -n "$OPENWEATHER_API_KEY" ]; then
        echo "✓ API key is configured"
        echo ""
        echo "Your API key: ${OPENWEATHER_API_KEY:0:8}..."
        echo ""
    else
        echo "⚠ .env file exists but API key is empty"
    fi
else
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Get your API key from OpenWeatherMap:"
echo "   → Visit: https://home.openweathermap.org/users/sign_up"
echo "   → Register (takes 2 minutes)"
echo "   → Get your API key from: https://home.openweathermap.org/api_keys"
echo ""
echo "2. Add your API key to .env file:"
echo "   → Open: week3/.env"
echo "   → Add: OPENWEATHER_API_KEY=your_key_here"
echo ""
echo "3. Run the test:"
echo "   → cd /Users/thg/modern-software-dev-assignments"
echo "   → poetry run python week3/test_setup.py"
echo ""
echo "=========================================="
echo ""

# Offer to open the registration page
read -p "Want me to open the registration page in your browser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "https://home.openweathermap.org/users/sign_up"
    echo "✓ Opening registration page..."
fi
