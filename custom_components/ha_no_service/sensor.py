"""Sensor platform for HA No Service."""
from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .api import NoAsAServiceAPI
from .const import DOMAIN, CONF_API_URL

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

SERVICE_GET_NO = "get_no"

PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_URL): cv.url,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the HA No Service sensor platform."""
    api_url = config[CONF_API_URL]
    session = async_get_clientsession(hass)
    api = NoAsAServiceAPI(session, api_url)

    async_add_entities([NoAsAServiceSensor(api)], True)

    # Register service to manually refresh the "no"
    if not hass.services.has_service(DOMAIN, SERVICE_GET_NO):
        async def handle_get_no(call):
            """Handle the get_no service call."""
            # Find the sensor and force update
            for component in hass.data.get("entity_components", {}).values():
                if hasattr(component, "entities"):
                    for entity in component.entities:
                        if isinstance(entity, NoAsAServiceSensor):
                            await entity.async_update()
                            await entity.async_update_ha_state(force_refresh=True)
                            _LOGGER.info("Manual 'no' update triggered")
                            return

        hass.services.async_register(
            DOMAIN,
            SERVICE_GET_NO,
            handle_get_no,
            schema=vol.Schema({}),
        )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HA No Service sensor from a config entry."""
    api_url = entry.data[CONF_API_URL]
    session = async_get_clientsession(hass)
    api = NoAsAServiceAPI(session, api_url)

    async_add_entities([NoAsAServiceSensor(api)], True)

    # Register service to manually refresh the "no"
    if not hass.services.has_service(DOMAIN, SERVICE_GET_NO):
        async def handle_get_no(call):
            """Handle the get_no service call."""
            # Find the sensor and force update
            for component in hass.data.get("entity_components", {}).values():
                if hasattr(component, "entities"):
                    for entity in component.entities:
                        if isinstance(entity, NoAsAServiceSensor):
                            await entity.async_update()
                            await entity.async_update_ha_state(force_refresh=True)
                            _LOGGER.info("Manual 'no' update triggered")
                            return

        hass.services.async_register(
            DOMAIN,
            SERVICE_GET_NO,
            handle_get_no,
            schema=vol.Schema({}),
        )


class NoAsAServiceSensor(SensorEntity):
    """Representation of a HA No Service sensor."""

    _attr_name = "HA No Service"
    _attr_icon = "mdi:cancel"

    def __init__(self, api: NoAsAServiceAPI) -> None:
        """Initialize the sensor."""
        self._api = api
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        data = await self._api.get_no()

        if data:
            reason = data.get("reason", "No")
            self._attr_native_value = reason
            self._attr_extra_state_attributes = {
                "reason": reason,
            }
            _LOGGER.debug("Updated HA No Service: %s", reason)
        else:
            _LOGGER.warning("Failed to fetch data from HA No Service API")
