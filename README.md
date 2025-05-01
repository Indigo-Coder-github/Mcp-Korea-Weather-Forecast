# MCP-Korea-Weather-Forecast

**MCP-Korea-Weather-Forecast** is the MCP server that utilizes the API provided by Korea Meteorology Administration (KMA) through [Korea Public Data Portal](https://www.data.go.kr/en/index.do).

---

## Features

- Based on the given latitude and longitude, the server provides the current weather, 6-hours forecasts, and5-days forecasts.
  - Current Date and Time is automatically detected by datetime module in Python.
  - This server can not detect your location automatically. Recommend to use other servers to get the latitude and longitude (ex. [Google Map](https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps)).

### get_ultra_short_nowcast

- Based on the given latitude and longitude, it provides the current weather.

### get_ultra_short_forecast

- Based on the given latitude and longitude, it provides the weather forecasting for 6 hours from now.

### get_vilage_forecast

- **This method will not operate due to very long json (120 hours with 12 Features). The Claude Free was stuck when I tested.**
- Based on the given latitude and longitude, it provides the hourly weather forecasting for 5 days from now.

---

## Quick Start

### Requirements

- Python 3.10+
- Data.go.kr account and API Key
  - For Korean, [take the API key from here.](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084)
  - For English, [take the API key from here.](https://www.data.go.kr/en/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084)
- MCP-compatible client (e.g., Claude for Desktop)

---

### 1. Clone and Setup

Clone and replace this repository where you want.

``` bash
git clone https://github.com/Indigo-Coder-github/Mcp-Korea-Weather-Forecast.git
```

### 2. Configure MCP Client

Register this server in your MCP client (e.g., Claude for Desktop).

Edit ~/Library/Application Support/Claude/claude_desktop_config.json:

```json
{
  "mcpServers": {
    "mcp-naver-location": {
      "command": "python",
      "args": [
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/server.py",
        "--api_key",
        "YOUR_API_KEY_IS_IN_HERE"
      ]
    }
  }
}
```

## License

- Built with [Model Context Protocol](https://modelcontextprotocol.io/introduction)