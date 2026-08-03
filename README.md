# trendsapi-py - Python client for the Trends API

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![API v1](https://img.shields.io/badge/API-v1-blue.svg)](https://trendsapi.ai) [![MCP compatible](https://img.shields.io/badge/MCP-compatible-blueviolet.svg)](https://modelcontextprotocol.io) [![Free tier](https://img.shields.io/badge/free%20tier-100%20req%2Fmo-orange.svg)](https://trendsapi.ai/#pricing)

> **Trend data in three lines of Python.** Keyword trend time series and growth rates across Google Search, YouTube, TikTok, Reddit, Amazon, Wikipedia, npm, Steam and more - normalized to one 0-100 score.

**Docs:** [https://trendsapi.ai/#quickstart](https://trendsapi.ai/#quickstart) · **API key (100 req/mo free):** [https://trendsapi.ai/#get-key](https://trendsapi.ai/#get-key)

---

## Install

```bash
pip install trendsapi
```

Zero system dependencies. Python 3.9+.

## Quickstart

```python
from trendsapi import TrendsAPI

client = TrendsAPI(api_key="YOUR_API_KEY")  # or set TRENDSAPI_KEY

# 5-year weekly time series
series = client.get_time_series(source="google search", keyword="bitcoin")

# Period-over-period growth
growth = client.get_growth(source="tiktok", keyword="bitcoin", percent_growth=["3M", "12M"])

# What is trending right now (no keyword needed)
trending = client.get_top_trends(type="Google Trends", limit=10)
```

## Async

```python
import asyncio
from trendsapi import AsyncTrendsAPI

async def main():
    client = AsyncTrendsAPI(api_key="YOUR_API_KEY")
    google, tiktok, reddit = await asyncio.gather(
        client.get_time_series(source="google search", keyword="bitcoin"),
        client.get_time_series(source="tiktok", keyword="bitcoin"),
        client.get_time_series(source="reddit", keyword="bitcoin"),
    )

asyncio.run(main())
```

## Why not raw requests?

You can absolutely use `requests` against `https://api.trendsapi.ai/api` directly - the API is one POST endpoint. The client adds typed responses, retries with backoff, async support, and source/feed constants so you never typo a source name.

## Coverage

| Source | `source` value | What it measures |
|---|---|---|
| Google Search | `google search` | Search volume |
| Google Images | `google images` | Image search volume |
| Google News | `google news` | News search volume |
| Google Shopping | `google shopping` | Shopping search volume |
| YouTube | `youtube` | Search volume |
| TikTok | `tiktok` | Hashtag volume |
| Reddit | `reddit` | Subreddit subscribers |
| Amazon | `amazon` | Product search volume |
| Wikipedia | `wikipedia` | Page views |
| News volume | `news volume` | Article mention volume |
| News sentiment | `news sentiment` | Positive / negative score |
| App downloads | `app downloads` | Android downloads (AppBrain) |
| App rankings | `app rankings` | Android chart position |
| npm | `npm` | Weekly package downloads |
| Steam | `steam` | Concurrent players (monthly) |

Plus 21 live trending feeds via `get_top_trends` - see the [main repo](https://github.com/trendsapi/trendsapi) for the full list.

## Use it from your AI assistant (MCP)

The same API key powers the Trends API MCP server, so Claude, Cursor, VS Code, ChatGPT and any MCP-compatible client can query this data in natural language.

[**+ Add to Cursor (one click)**](cursor://anysphere.cursor-deeplink/mcp/install?name=trendsapi&config=eyJ1cmwiOiAiaHR0cHM6Ly9hcGkudHJlbmRzYXBpLmFpL21jcCIsICJoZWFkZXJzIjogeyJBdXRob3JpemF0aW9uIjogIkJlYXJlciBZT1VSX0FQSV9LRVkifX0=)

**Cursor / Windsurf / Cline** (`~/.cursor/mcp.json` or equivalent):

```json
{
  "mcpServers": {
    "trendsapi": {
      "url": "https://api.trendsapi.ai/mcp",
      "transport": "http",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**VS Code / GitHub Copilot** (`.vscode/mcp.json`):

```json
{
  "servers": {
    "trendsapi": {
      "type": "http",
      "url": "https://api.trendsapi.ai/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "trendsapi": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.trendsapi.ai/mcp", "--header", "Authorization:${AUTH_HEADER}"],
      "env": { "AUTH_HEADER": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**Claude.ai (browser):** Settings -> Connectors -> Add custom connector -> `https://api.trendsapi.ai/mcp`

Then ask things like:

```
How did "creatine gummies" grow on TikTok vs Google over the last 12 months?
What is trending on YouTube right now?
```

---

## Links

- **Docs & quickstart:** [https://trendsapi.ai/#quickstart](https://trendsapi.ai/#quickstart)
- **llms.txt (machine-readable API reference):** [https://trendsapi.ai/llms.txt](https://trendsapi.ai/llms.txt)
- **Pricing (free tier: 100 requests/month):** [https://trendsapi.ai/#pricing](https://trendsapi.ai/#pricing)
- **Get an API key:** [https://trendsapi.ai/#get-key](https://trendsapi.ai/#get-key)

## License

MIT - see [LICENSE](LICENSE). Data is served by [Trends API](https://trendsapi.ai); usage of the API itself is subject to the plan limits on your key.
