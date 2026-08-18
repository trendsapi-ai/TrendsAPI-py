"""Type definitions for the Trends API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional, Union

TrendsSource = Literal[
    "google search",
    "google images",
    "google news",
    "google shopping",
    "youtube",
    "tiktok",
    "reddit",
    "amazon",
    "wikipedia",
    "news volume",
    "news sentiment",
    "app downloads",
    "app rankings",
    "npm",
    "steam",
]

KEYWORD_SOURCES: tuple[str, ...] = (
    "google search",
    "google images",
    "google news",
    "google shopping",
    "youtube",
    "tiktok",
    "reddit",
    "amazon",
    "wikipedia",
    "news volume",
    "news sentiment",
    "app downloads",
    "app rankings",
    "npm",
    "steam",
)


@dataclass
class TrendsDataPoint:
    date: str
    value: float
    keyword: str
    volume: Optional[float] = None
    source: Optional[str] = None
    datatype: Optional[str] = None
    volume_cumulative: Optional[float] = None


GetTrendsResponse = List[TrendsDataPoint]
GetTimeSeriesResponse = GetTrendsResponse

GrowthPreset = Literal[
    "7D",
    "14D",
    "30D",
    "1M",
    "2M",
    "3M",
    "6M",
    "9M",
    "12M",
    "1Y",
    "18M",
    "24M",
    "2Y",
    "36M",
    "3Y",
    "48M",
    "60M",
    "5Y",
    "MTD",
    "QTD",
    "YTD",
]


@dataclass
class CustomGrowthPeriod:
    recent: str
    baseline: str
    name: Optional[str] = None


@dataclass
class GrowthResult:
    """One growth window. On success ``status`` is usually ``success``.

    When a preset is outside available history the API still returns HTTP 200
    with ``status=\"error\"`` and ``error`` / ``message`` fields - those rows
    omit growth numbers.
    """

    period: str
    growth: Optional[float] = None
    direction: Optional[str] = None
    recent_date: Optional[str] = None
    baseline_date: Optional[str] = None
    recent_value: Optional[float] = None
    baseline_value: Optional[float] = None
    volume_available: bool = False
    recent_volume: Optional[float] = None
    baseline_volume: Optional[float] = None
    volume_growth: Optional[float] = None
    status: Optional[str] = None
    error: Optional[str] = None
    message: Optional[str] = None
    data_start: Optional[str] = None
    data_end: Optional[str] = None
    calculation_method: Optional[str] = None
    growth_unit: Optional[str] = None
    volume_estimated: Optional[bool] = None
    volume_direction: Optional[str] = None
    volume_growth_omitted_reason: Optional[str] = None


@dataclass
class GrowthMetadata:
    total_data_points: int
    calculations_completed: int
    all_successful: bool


@dataclass
class GetGrowthResponse:
    search_term: str
    data_source: str
    results: List[GrowthResult]
    metadata: GrowthMetadata


TopTrendsFeed = Literal[
    "Google Trends",
    "Google News Top News",
    "TikTok Trending Hashtags",
    "TikTok Trending Searches",
    "TikTok Shop Hot Products",
    "YouTube Trending",
    "X (Twitter) Trending",
    "Reddit Hot Posts",
    "Reddit World News",
    "Wikipedia Trending",
    "Amazon Best Sellers Top Rated",
    "Amazon Best Sellers by Category",
    "App Store Top Free",
    "App Store Top Paid",
    "Google Play",
    "Top Websites",
    "Spotify Top Podcasts",
    "Steam Most Played",
    "GitHub Trending Repos",
    "IMDb MOVIEmeter",
    "Open Library Trending Books",
]

LIVE_FEEDS: tuple[str, ...] = (
    "Google Trends",
    "Google News Top News",
    "TikTok Trending Hashtags",
    "TikTok Trending Searches",
    "TikTok Shop Hot Products",
    "YouTube Trending",
    "X (Twitter) Trending",
    "Reddit Hot Posts",
    "Reddit World News",
    "Wikipedia Trending",
    "Amazon Best Sellers Top Rated",
    "Amazon Best Sellers by Category",
    "App Store Top Free",
    "App Store Top Paid",
    "Google Play",
    "Top Websites",
    "Spotify Top Podcasts",
    "Steam Most Played",
    "GitHub Trending Repos",
    "IMDb MOVIEmeter",
    "Open Library Trending Books",
)


@dataclass
class GetTopTrendsResponse:
    type: str
    count: int
    data: List[list]
    limit: Optional[int] = None
    offset: Optional[int] = None
    as_of_ts: Optional[str] = None
