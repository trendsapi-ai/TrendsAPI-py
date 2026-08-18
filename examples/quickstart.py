"""Trends API Python client. Get a free key at https://trendsapi.ai/#get-key"""
from trendsapi import TrendsAPI

client = TrendsAPI()  # TRENDSAPI_KEY
print(client.get_top_trends(type="Google Trends", limit=10))
