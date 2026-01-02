"""API client for No as a Service."""
import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)

API_URL = "https://naas.isalman.dev/no"
TIMEOUT = 10


class NoAsAServiceAPI:
    """API client for No as a Service."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def get_no(self) -> dict[str, Any] | None:
        """Get a 'no' response from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.get(API_URL)
                response.raise_for_status()
                data = await response.json()

                # The API returns {"reason": "rejection reason text"}
                if "reason" in data:
                    return data

                _LOGGER.warning("Unexpected API response format: %s", data)
                return None

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from No as a Service API: %s", err)
            return None
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching data from No as a Service API")
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error fetching from API: %s", err)
            return None
