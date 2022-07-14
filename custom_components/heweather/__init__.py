"""The HeWeather component."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_LOCATION,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
    Platform,
)

from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .heweather import HeWeather
from .const import (
    DOMAIN,
    CONF_FORECAST,
)

PLATFORMS = [Platform.WEATHER]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up HeWeather as config entry."""
    coordinator = HeWeatherDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    config_entry.async_on_unload(config_entry.add_update_listener(update_listener))

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(config_entry.entry_id)


class HeWeatherDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HeWeather data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize global HeWeather data updater."""
        self.weather = HeWeather(
            config_entry.data[CONF_LOCATION],
            config_entry.data[CONF_API_KEY],
            config_entry.options.get(CONF_FORECAST, 3)
        )

        update_interval = timedelta(minutes=config_entry.options.get(CONF_SCAN_INTERVAL, 30))

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self):
        """Fetch data from HeWeather."""
        try:
            await self.weather.async_fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err
        return self.weather.weather_data