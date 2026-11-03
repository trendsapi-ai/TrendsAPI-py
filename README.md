# trendsapi (Python)

Official Python client for [Trends API](https://trendsapi.ai). Three methods. Decoded payloads. You never parse the HTTP `body` string.

HTTP contract and field tables: [trendsapi-ai/trendsapi](https://github.com/trendsapi-ai/trendsapi).

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/trendsapi.svg)](https://pypi.org/project/trendsapi/)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)](https://trendsapi.ai)

## First call

```bash
curl -X POST https://api.trendsapi.ai/api \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"mode":"get_growth","source":"tiktok","keyword":"matcha"}'
```

## Authentication

```bash
pip install trendsapi
export TRENDSAPI_KEY=your_key
```

Key: [trendsapi.ai/#get-key](https://trendsapi.ai/#get-key). Python 3.9+.

```python
from trendsapi import TrendsAPI

client = TrendsAPI()                    # TRENDSAPI_KEY
# client = TrendsAPI(api_key="YOUR_KEY")
```

## Methods

| Method | REST `mode` | Required arguments | Returns |
|---|---|---|---|
| `get_time_series` | `get_time_series` | `source`, `keyword` | `list[TrendsDataPoint]` |
| `get_growth` | `get_growth` | `source`, `keyword` | `GetGrowthResponse` |
| `get_top_trends` | `get_top_trends` | `type` | `GetTopTrendsResponse` |

```python
weekly = client.get_time_series(source="google search", keyword="solar battery")
growth = client.get_growth(source="amazon", keyword="solar battery", percent_growth=["3M", "12M"])
now = client.get_top_trends(type="Google Trends", limit=10)
```

`source` is lowercase (`google search`). `type` is exact (`Google Trends`). Mixing them is a 400.

## get_time_series

```python
points = client.get_time_series(source="google search", keyword="bitcoin")
print(points[-1].date, points[-1].value)
```

Python returns dataclasses. Use `.date` / `.value`, not `["date"]`.

Each point:

| Field | Always | Meaning |
|---|---|---|
| `date` | yes | `YYYY-MM-DD` |
| `value` | yes | 0-100 index for this series |
| `keyword` | yes | Echo |
| `volume` | no | Absolute volume when available |
| `source` or `datatype` | no | Pipeline label |

## get_growth

```python
g = client.get_growth(source="google search", keyword="nike", percent_growth=["12M", "3M", "YTD"])
print(g.results[0].growth, g.results[0].direction)
```

`percent_growth` default: `["12M"]`. Presets: `7D` `14D` `30D` `1M` `2M` `3M` `6M` `9M` `12M`/`1Y` `18M` `24M`/`2Y` `36M`/`3Y` `48M` `60M`/`5Y` `MTD` `QTD` `YTD`. Custom: `{"name": "Launch", "recent": "2024-06-01", "baseline": "2024-01-01"}`.

| Field | Meaning |
|---|---|
| `search_term` | Keyword |
| `data_source` | Source |
| `results` | One object per window (`period`, `growth`, `direction`, dates, values) |
| `metadata` | Counts / success flag |

Several windows still count as one request.

## get_top_trends

```python
chart = client.get_top_trends(type="TikTok Trending Hashtags", limit=10)
# chart.data == [[1, "matcha"], ...]
```

| Field | Meaning |
|---|---|
| `as_of_ts` | Snapshot time |
| `type` | Feed name |
| `limit`, `offset`, `count` | Pagination |
| `data` | `[rank, label]` rows |

Optional `offset=`, `category=` (the `by Category` boards and `Top Websites`).

## Keyword sources

Pass as `source=`. Full notes: [hub README](https://github.com/trendsapi-ai/trendsapi#keyword-sources).

| `source` | `keyword` |
|---|---|
| `Google Search` | Any name or phrase (`electric vehicles`) |
| `Google Images` | Any name or phrase (`electric vehicles`) |
| `Google News` | Any name or phrase (`electric vehicles`) |
| `Google Shopping` | Any name or phrase (`running shoes`) |
| `YouTube` | Any name or phrase (`stanley cup`) |
| `Wikipedia` | Any name or phrase (`Bitcoin`) |
| `TikTok` | Any name or phrase (`booktok`) |
| `Amazon` | Any name or phrase (`air fryer`) |
| `Pinterest` | Any name or phrase (`matcha`) |
| `npm` | Exact npmjs.com package name, case-sensitive (`langchain`) |
| `Python` | Exact PyPI project name (`pandas`) |
| `Steam` | Game display name in plain English, not a Steam App ID (`Elden Ring`) |
| `App Downloads` | Android bundle ID only (the id= value on Google Play) (`com.openai.chatgpt`) |
| `App Rankings` | Android bundle ID only (the id= value on Google Play) (`com.openai.chatgpt`) |

This client covers the three keyword and board methods. The API also has `get_context` (what people are posting about a keyword) and `get_top_posts` (top posts for a hashtag, Business plan); call those over raw HTTP for now: [hub, get_context](https://github.com/trendsapi-ai/trendsapi#get_context).

## Live boards

Pass as `type=` on `get_top_trends`. Exact strings: `Amazon Best Sellers Top Rated`, `Amazon Best Sellers by Category`, `App Store Top Free`, `App Store Top Paid`, `GitHub`, `Google News Top News`, `Google Play`, `Google Trends`, `Google Trends by Category`, `IMDb MOVIEmeter`, `Open Library Trending Books`, `Pinterest Trending`, `Pinterest Trending by Category`, `Polymarket Top Markets`, `Reddit Hot Posts`, `Reddit World News`, `Top Websites`, `Spotify Top Podcasts`, `Steam Most Played`, `Substack`, `Substack by Category`, `TikTok Trending Hashtags`, `TikTok Trending Hashtags by Category`, `TikTok Trending Searches`, `Wikipedia Trending`, `X (Twitter) Trending`, `YouTube Trending`.

## Async

```python
import asyncio
from trendsapi import AsyncTrendsAPI

async def compare(term: str):
    c = AsyncTrendsAPI()
    return await asyncio.gather(
        c.get_time_series(source="google search", keyword=term),
        c.get_time_series(source="google shopping", keyword=term),
        c.get_time_series(source="wikipedia", keyword=term),
    )

asyncio.run(compare("solar battery"))
```

Each 200 is one billed request.

## Pandas

```python
from dataclasses import asdict
import pandas as pd
from trendsapi import TrendsAPI

df = pd.DataFrame(asdict(p) for p in TrendsAPI().get_time_series(source="google search", keyword="solar battery"))
df["date"] = pd.to_datetime(df["date"])
print(df.set_index("date")["value"].resample("ME").mean().tail())
```

## Errors

| Code | Client |
|---|---|
| 200 | Returns parsed payload |
| 400 | Raises. Fix `source` / `type` |
| 401 | Raises. Check `TRENDSAPI_KEY` |
| 404 | Raises. No series. Do not retry |
| 429 | Raises. Quota |
| 5xx | Retries, then raises |

Raw `requests` (second parse required): see [hub, Raw HTTP](https://github.com/trendsapi-ai/trendsapi#raw-http).

## License

MIT. See [LICENSE](LICENSE).
