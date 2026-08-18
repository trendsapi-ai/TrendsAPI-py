"""Trends API client - sync and async.

Docs: https://trendsapi.ai/#quickstart
Machine-readable reference: https://trendsapi.ai/llms.txt
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import fields
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import httpx

from .exceptions import TrendsAPIError
from .types import (
    CustomGrowthPeriod,
    GetGrowthResponse,
    GetTopTrendsResponse,
    GetTrendsResponse,
    GrowthMetadata,
    GrowthResult,
    TrendsDataPoint,
)

T = TypeVar("T")

BASE_URL = "https://api.trendsapi.ai/api"
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3


def _from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
    allowed = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in allowed})  # type: ignore[arg-type]


def _resolve_api_key(api_key: Optional[str]) -> str:
    key = (api_key or os.environ.get("TRENDSAPI_KEY") or "").strip()
    if not key:
        raise ValueError(
            "api_key is required. Pass TrendsAPI(api_key=...) or set TRENDSAPI_KEY. "
            "Get a free key at https://trendsapi.ai/#get-key"
        )
    return key


def _parse_error(status: int, body: Any) -> TrendsAPIError:
    if isinstance(body, dict):
        return TrendsAPIError(
            status,
            str(body.get("error", status)),
            str(body.get("message", body.get("error", "Unknown error"))),
        )
    return TrendsAPIError(status, str(status), str(body))


def _unwrap(raw: Any, status: int) -> Any:
    """Unwrap Lambda proxy envelope { statusCode, body: '<json>' } when present."""
    if (
        isinstance(raw, dict)
        and isinstance(raw.get("statusCode"), int)
        and isinstance(raw.get("body"), str)
    ):
        parsed = json.loads(raw["body"])
        if raw["statusCode"] >= 400:
            raise _parse_error(raw["statusCode"], parsed)
        return parsed
    if status >= 400:
        raise _parse_error(status, raw)
    return raw


def _build_growth_period(p: Union[str, CustomGrowthPeriod]) -> Any:
    if isinstance(p, str):
        return p
    d: Dict[str, str] = {"recent": p.recent, "baseline": p.baseline}
    if p.name:
        d["name"] = p.name
    return d


def _parse_trends(data: List[Dict]) -> GetTrendsResponse:
    return [_from_dict(TrendsDataPoint, dp) for dp in data]


def _parse_growth(data: Dict) -> GetGrowthResponse:
    results = [_from_dict(GrowthResult, r) for r in data["results"]]
    metadata = _from_dict(GrowthMetadata, data["metadata"])
    return GetGrowthResponse(
        search_term=data["search_term"],
        data_source=data["data_source"],
        results=results,
        metadata=metadata,
    )


def _parse_top_trends(data: Dict) -> GetTopTrendsResponse:
    return _from_dict(GetTopTrendsResponse, data)


def _should_retry(status: int) -> bool:
    return status == 429 or status >= 500


class TrendsAPI:
    """Synchronous Trends API client.

    Example::

        from trendsapi import TrendsAPI

        client = TrendsAPI()  # or TrendsAPI(api_key="...") / TRENDSAPI_KEY
        series = client.get_time_series(source="google search", keyword="bitcoin")
        growth = client.get_growth(source="tiktok", keyword="bitcoin", percent_growth=["3M", "12M"])
        trending = client.get_top_trends(type="Google Trends", limit=10)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        self._headers = {
            "Authorization": f"Bearer {_resolve_api_key(api_key)}",
            "Content-Type": "application/json",
            "User-Agent": "trendsapi-python/1.0.2",
        }
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    def _post(self, body: Dict) -> Any:
        last_exc: Optional[Exception] = None
        with httpx.Client(timeout=self._timeout) as client:
            for attempt in range(self._max_retries + 1):
                resp = client.post(self._base_url, json=body, headers=self._headers)
                if resp.status_code < 400 or not _should_retry(resp.status_code):
                    return _unwrap(resp.json(), resp.status_code)
                last_exc = _parse_error(resp.status_code, resp.json() if resp.content else {})
                if attempt < self._max_retries:
                    time.sleep(min(2**attempt, 8))
        assert last_exc is not None
        raise last_exc

    def get_time_series(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        """Return historical trend points for one source + keyword (default ~5y weekly)."""
        body: Dict = {"mode": "get_time_series", "source": source, "keyword": keyword}
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_trends(self._post(body))

    def get_trends(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        """Alias for :meth:`get_time_series`."""
        return self.get_time_series(source=source, keyword=keyword, data_mode=data_mode)

    def get_growth(
        self,
        source: str,
        keyword: str,
        percent_growth: Optional[List[Union[str, CustomGrowthPeriod]]] = None,
        data_mode: Optional[str] = None,
    ) -> GetGrowthResponse:
        """Period-over-period growth. Defaults to ``["12M"]`` when omitted by the API."""
        body: Dict = {"mode": "get_growth", "source": source, "keyword": keyword}
        if percent_growth is not None:
            body["percent_growth"] = [_build_growth_period(p) for p in percent_growth]
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_growth(self._post(body))

    def get_top_trends(
        self,
        type: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> GetTopTrendsResponse:
        """Live trending feed. Omit ``type`` on REST to receive all feeds."""
        body: Dict = {"mode": "get_top_trends"}
        if type:
            body["type"] = type
        if category:
            body["category"] = category
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        return _parse_top_trends(self._post(body))


class AsyncTrendsAPI:
    """Async Trends API client (requires ``await``)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        self._headers = {
            "Authorization": f"Bearer {_resolve_api_key(api_key)}",
            "Content-Type": "application/json",
            "User-Agent": "trendsapi-python/1.0.2",
        }
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def _post(self, body: Dict) -> Any:
        import asyncio

        last_exc: Optional[Exception] = None
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            for attempt in range(self._max_retries + 1):
                resp = await client.post(self._base_url, json=body, headers=self._headers)
                if resp.status_code < 400 or not _should_retry(resp.status_code):
                    return _unwrap(resp.json(), resp.status_code)
                last_exc = _parse_error(resp.status_code, resp.json() if resp.content else {})
                if attempt < self._max_retries:
                    await asyncio.sleep(min(2**attempt, 8))
        assert last_exc is not None
        raise last_exc

    async def get_time_series(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        body: Dict = {"mode": "get_time_series", "source": source, "keyword": keyword}
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_trends(await self._post(body))

    async def get_trends(
        self,
        source: str,
        keyword: str,
        data_mode: Optional[str] = None,
    ) -> GetTrendsResponse:
        return await self.get_time_series(source=source, keyword=keyword, data_mode=data_mode)

    async def get_growth(
        self,
        source: str,
        keyword: str,
        percent_growth: Optional[List[Union[str, CustomGrowthPeriod]]] = None,
        data_mode: Optional[str] = None,
    ) -> GetGrowthResponse:
        body: Dict = {"mode": "get_growth", "source": source, "keyword": keyword}
        if percent_growth is not None:
            body["percent_growth"] = [_build_growth_period(p) for p in percent_growth]
        if data_mode:
            body["data_mode"] = data_mode
        return _parse_growth(await self._post(body))

    async def get_top_trends(
        self,
        type: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> GetTopTrendsResponse:
        body: Dict = {"mode": "get_top_trends"}
        if type:
            body["type"] = type
        if category:
            body["category"] = category
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        return _parse_top_trends(await self._post(body))
