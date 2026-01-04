"""The HA No Service integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_no_service"
PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HA No Service component."""
    hass.data.setdefault(DOMAIN, {})

    # Only setup if configured
    if DOMAIN in config:
        # Forward setup to sensor platform
        hass.async_create_task(
            discovery.async_load_platform(
                hass, Platform.SENSOR, DOMAIN, {}, config
            )
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA No Service from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
