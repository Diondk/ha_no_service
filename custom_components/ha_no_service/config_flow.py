"""Config flow for HA No Service integration."""
from __future__ import annotations

import logging
from urllib.parse import urlparse

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_API_URL, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)


def _is_valid_http_url(value: str) -> bool:
    """Validate that the URL is a valid HTTP/HTTPS URL."""
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


async def _async_can_reach_api(hass: HomeAssistant, api_url: str) -> bool:
    """Optional: quick connectivity check to avoid bad URLs."""
    session = async_get_clientsession(hass)
    try:
        async with session.get(api_url, timeout=10) as resp:
            # Accept any HTTP response as "reachable" (even 401/403),
            # because the endpoint might require auth.
            return resp.status > 0
    except Exception as err:
        _LOGGER.debug("API reachability check failed: %s", err)
        return False


class HANoServiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA No Service."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api_url = user_input[CONF_API_URL].strip()

            if not _is_valid_http_url(api_url):
                errors[CONF_API_URL] = "invalid_url"
            else:
                # Prevent duplicate entries for the same URL
                await self.async_set_unique_id(api_url.lower())
                self._abort_if_unique_id_configured()

                # Optional reachability check
                reachable = await _async_can_reach_api(self.hass, api_url)
                if not reachable:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=DEFAULT_NAME,
                        data={CONF_API_URL: api_url},
                    )

        schema = vol.Schema(
            {
                vol.Required(CONF_API_URL): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_import(self, user_input: dict) -> FlowResult:
        """Handle import from YAML configuration."""
        api_url = user_input.get(CONF_API_URL, "").strip()

        if not _is_valid_http_url(api_url):
            return self.async_abort(reason="invalid_url")

        # Prevent duplicate entries for the same URL
        await self.async_set_unique_id(api_url.lower())
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=DEFAULT_NAME,
            data={CONF_API_URL: api_url},
        )
