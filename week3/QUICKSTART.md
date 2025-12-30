# Quick Start Guide - Weather MCP Server

Get up and running in 5 minutes!

## Step 1: Get Your API Key (2 minutes)

1. Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. Click "Sign Up" (top right)
3. Create a free account
4. Go to "API keys" section in your account
5. Copy your API key
6. **Note**: New keys take 10-15 minutes to activate, so grab a coffee! ☕

## Step 2: Configure Environment (30 seconds)

```bash
cd week3
cp .env.example .env
```

Edit `.env` and paste your API key:

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

## Step 3: Test the Setup (1 minute)

```bash
cd /Users/thg/modern-software-dev-assignments
poetry run python week3/test_setup.py
```

You should see:

```
✅ All tests passed! Your Weather MCP Server is ready to use.
```

If you get errors:

- **"Invalid API key"**: Wait 10-15 minutes for activation
- **"Network error"**: Check your internet connection
- **"Module not found"**: Run `poetry install` first

## Step 4: Configure Claude Desktop (2 minutes)

1. Open Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Create it if it doesn't exist

2. Add this configuration (replace YOUR_API_KEY):

```json
{
  "mcpServers": {
    "weather": {
      "command": "poetry",
      "args": ["run", "python", "-m", "week3.server.main"],
      "cwd": "/Users/thg/modern-software-dev-assignments",
      "env": {
        "OPENWEATHER_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

1. Save the file
2. **Restart Claude Desktop completely** (Cmd+Q, then reopen)

## Step 5: Test in Claude Desktop (1 minute)

Look for the 🔌 icon in Claude Desktop - you should see "weather" server connected.

Try asking Claude:

- "What's the weather in Paris?"
- "Give me a 5-day forecast for Tokyo"
- "What's the current temperature in New York in Fahrenheit?"

## Troubleshooting

### Claude Desktop doesn't show the weather server

1. Check the config file path is correct
2. Verify JSON syntax (use [jsonlint.com](https://jsonlint.com))
3. Make sure you completely quit and restarted Claude
4. Check logs in Claude Desktop (Help → View Logs)

### "Invalid API key" error

- Wait 10-15 minutes after creating the key
- Double-check you copied the full key
- Make sure there are no quotes around the key in .env

### "Module not found" error

```bash
cd /Users/thg/modern-software-dev-assignments
poetry install
```

## Manual Testing (Without Claude Desktop)

You can also test using the MCP Inspector:

```bash
cd week3
npx @modelcontextprotocol/inspector poetry run python -m server.main
```

This opens a web UI at <http://localhost:5173> where you can test the tools directly.

## What's Next?

Once everything works:

1. **Read the full README.md** for detailed documentation
2. **Try different locations** - cities, coordinates, different countries
3. **Test error handling** - try invalid city names, see how errors are handled
4. **Explore the code** - check out `server/main.py` and `server/weather_client.py`

## Common Test Queries

Try these in Claude Desktop:

```
"What's the weather like in London right now?"

"Give me a detailed 5-day forecast for San Francisco"

"What's the temperature at coordinates 35.6762, 139.6503?"

"Show me the weather in Berlin in Fahrenheit"

"Compare the weather in Tokyo and New York"
```

Enjoy your Weather MCP Server! 🌦️
