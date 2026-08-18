# trendsapi (Python)

Official Python client for [Trends API](https://trendsapi.ai). Three methods. Decoded payloads. You never parse the HTTP `body` string.

HTTP contract and field tables: [trendsapi-ai/trendsapi](https://github.com/trendsapi-ai/trendsapi).

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pip-trendsapi-blue.svg)](https://pypi.org/project/trendsapi/)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)](https://trendsapi.ai)

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
| `get_time_series` | `get_time_series` | `source`, `keyword` | `list[dict]` of weekly points |
| `get_growth` | `get_growth` | `source`, `keyword` | growth `dict` |
| `get_top_trends` | `get_top_trends` | `type` | feed `dict` |

```python
weekly = client.get_time_series(source="google search", keyword="solar battery")
growth = client.get_growth(source="amazon", keyword="solar battery", percent_growth=["3M", "12M"])
now = client.get_top_trends(type="Google Trends", limit=10)
```

`source` is lowercase (`google search`). `type` is exact (`Google Trends`). Mixing them is a 400.

## get_time_series

```python
points = client.get_time_series(source="google search", keyword="bitcoin")
```

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
print(g["results"][0]["growth"], g["results"][0]["direction"])
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
# chart["data"] == [[1, "matcha"], ...]
```

| Field | Meaning |
|---|---|
| `as_of_ts` | Snapshot time |
| `type` | Feed name |
| `limit`, `offset`, `count` | Pagination |
| `data` | `[rank, label]` rows |

Optional `offset=`, `category=` (`Amazon Best Sellers by Category`, `Top Websites` only).

## Keyword sources

Pass as `source=`. Full notes: [hub README](https://github.com/trendsapi-ai/trendsapi#keyword-sources).

| `source` | `keyword` |
|---|---|
| `google search`, `google images`, `google news`, `google shopping` | Any phrase |
| `youtube` | Any phrase |
| `tiktok` | Hashtag or topic |
| `reddit` | Subreddit, no `r/` |
| `amazon` | Product phrase |
| `wikipedia` | Article title |
| `news volume`, `news sentiment` | Any phrase |
| `app downloads`, `app rankings` | Android bundle ID (`com.openai.chatgpt`) |
| `npm` | Exact package name |
| `steam` | Game display name |

## Live feeds

Pass as `type=` on `get_top_trends`. Exact strings: `Google Trends`, `Google News Top News`, `TikTok Trending Hashtags`, `TikTok Trending Searches`, `TikTok Shop Hot Products`, `YouTube Trending`, `X (Twitter) Trending`, `Reddit Hot Posts`, `Reddit World News`, `Wikipedia Trending`, `Amazon Best Sellers Top Rated`, `Amazon Best Sellers by Category`, `App Store Top Free`, `App Store Top Paid`, `Google Play`, `Top Websites`, `Spotify Top Podcasts`, `Steam Most Played`, `GitHub Trending Repos`, `IMDb MOVIEmeter`, `Open Library Trending Books`.

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
import pandas as pd
from trendsapi import TrendsAPI

df = pd.DataFrame(TrendsAPI().get_time_series(source="google search", keyword="solar battery"))
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
