"""Minimal live example. Set TRENDSAPI_KEY or pass api_key=."""

from trendsapi import TrendsAPI

client = TrendsAPI()
keyword = "creatine gummies"

for source in ("google search", "tiktok", "amazon"):
    g = client.get_growth(source=source, keyword=keyword, percent_growth=["12M"])
    r = g.results[0]
    print(source, r.growth, r.direction)

series = client.get_time_series(source="google search", keyword=keyword)
print("latest:", series[-1].date, series[-1].value)

hot = client.get_top_trends(type="TikTok Trending Hashtags", limit=5)
print("hot:", hot.data)
