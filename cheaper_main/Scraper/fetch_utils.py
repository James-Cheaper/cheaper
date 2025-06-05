import requests
import logging
from functools import lru_cache
from typing import Optional


@lru_cache(maxsize=128)
def cached_get(url: str, user_agent: str) -> Optional[str]:
    print(f"[HTTP Request] Fetching from web: {url}")
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

            


