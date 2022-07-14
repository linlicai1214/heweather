"""Support for HeWeather service."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.distance import convert as convert_distance
from homeassistant.util.pressure import convert as convert_pressure
from homeassistant.util.speed import convert as convert_speed

from homeassistant.components.weather import (
    ATTR_FORECAST,
    ATTR_FORECAST_CONDITION,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_SPEED,
    ATTR_WEATHER_VISIBILITY,
    Forecast,
    WeatherEntity,
)


from homeassistant.const import (
    CONF_LOCATION,
    CONF_NAME,

    LENGTH_MILLIMETERS,
    LENGTH_KILOMETERS,
    PRESSURE_HPA,
    SPEED_KILOMETERS_PER_HOUR,
    TEMP_CELSIUS,
    PRECISION_TENTHS,
)

from . import HeWeatherDataUpdateCoordinator
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    ATTRIBUTION
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    """Add a weather entity from a config_entry."""
    coordinator: HeWeatherDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            HeWeatherEntity(
                coordinator, 
                config_entry.data[CONF_LOCATION], 
                config_entry.data[CONF_NAME], 
                hass.config.units.is_metric
            )
        ]
    )


class HeWeatherEntity(CoordinatorEntity[HeWeatherDataUpdateCoordinator], WeatherEntity):
    """Implementation of a weather condition."""

    def __init__(
        self,
        coordinator: HeWeatherDataUpdateCoordinator,
        uid: str,
        name: str,
        is_metric: bool,
    ) -> None:
        """Initialise the platform with a data instance and site."""
        super().__init__(coordinator)
        self._attr_unique_id = uid
        self._attr_name = name if name is not None else DEFAULT_NAME
        self._attr_attribution = ATTRIBUTION

        self._attr_pressure_unit = PRESSURE_HPA
        self._attr_visibility_unit = LENGTH_KILOMETERS
        self._attr_precipitation_unit = LENGTH_MILLIMETERS
        self._attr_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_precision = PRECISION_TENTHS

        self._is_metric = is_metric

    # 天气状态
    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        return self.coordinator.data.get(ATTR_FORECAST_CONDITION)

    # 气温
    @property
    def temperature(self) -> float | None:
        """Return the temperature."""
        return self.coordinator.data.get(ATTR_WEATHER_TEMPERATURE)

    # 气压
    @property
    def pressure(self) -> float | None:
        """Return the pressure."""
        return self.coordinator.data.get(ATTR_WEATHER_PRESSURE)
        
    
    # 湿度
    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        return self.coordinator.data.get(ATTR_WEATHER_HUMIDITY)

    # 风速
    @property
    def wind_speed(self) -> float | None:
        """Return the wind speed."""
        return self.coordinator.data.get(ATTR_WEATHER_WIND_SPEED)

    # 风向
    @property
    def wind_bearing(self) -> float | str | None:
        """Return the wind direction."""
        return self.coordinator.data.get(ATTR_WEATHER_WIND_BEARING)

    # 可见度
    @property
    def visibility(self) -> float:
        """Return the visibility."""
        return self.coordinator.data.get(ATTR_WEATHER_VISIBILITY)

    # 预报数据
    @property
    def forecast(self) -> list[Forecast] | None:
        """Return the forecast array."""
        return self.coordinator.data[ATTR_FORECAST]

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            default_name="Forecast",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN,)},  # type: ignore[arg-type]
            manufacturer="HeWeather",
            configuration_url="https://www.qweather.com/",
        )
