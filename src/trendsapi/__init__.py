"""
trendsapi - Official Python client for the Trends API.

Normalized 0-100 trend scores across Google, TikTok, Amazon, Reddit, YouTube,
Steam, npm and 30+ sources from one REST endpoint.

Get a free API key: https://trendsapi.ai/#get-key
Quickstart: https://trendsapi.ai/#quickstart
"""

from .client import AsyncTrendsAPI, TrendsAPI
from .exceptions import TrendsAPIError
from .types import (
    KEYWORD_SOURCES,
    LIVE_FEEDS,
    CustomGrowthPeriod,
    GetGrowthResponse,
    GetTimeSeriesResponse,
    GetTopTrendsResponse,
    GetTrendsResponse,
    GrowthMetadata,
    GrowthPreset,
    GrowthResult,
    TopTrendsFeed,
    TrendsDataPoint,
    TrendsSource,
)

__version__ = "1.0.0"
__all__ = [
    "TrendsAPI",
    "AsyncTrendsAPI",
    "TrendsAPIError",
    "TrendsSource",
    "TrendsDataPoint",
    "GetTrendsResponse",
    "GetTimeSeriesResponse",
    "GrowthPreset",
    "CustomGrowthPeriod",
    "GrowthResult",
    "GrowthMetadata",
    "GetGrowthResponse",
    "TopTrendsFeed",
    "GetTopTrendsResponse",
    "KEYWORD_SOURCES",
    "LIVE_FEEDS",
]
