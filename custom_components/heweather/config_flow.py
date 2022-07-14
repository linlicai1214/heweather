"""Config flow to configure HeWeather component."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.const import(
    CONF_LOCATION,
    CONF_NAME,
    CONF_API_KEY, 
    CONF_SCAN_INTERVAL,
)

from .heweather import HeWeather, ConnectError, InvalidApiKeyError, ApiParamError
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    CONF_FORECAST,
    CONF_CITY_SELECT
)


class HeWeatherFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HeWeather component."""

    VERSION = 1

    def __init__(self):
        """Init Initialize."""
        self._errors = {}
        self.name = DEFAULT_NAME
        self.key = None
        self.location = None
        self.citylist = dict()

    @callback
    def async_show_config_form(self):
        """Show the configuration form to edit location data."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY, default = self.key): str,
                vol.Required(CONF_LOCATION, default = self.location): str,
                vol.Required(CONF_NAME, default = self.name): str,
            }
        )
        if self.citylist:
            data_schema = data_schema.extend(
                {
                    vol.Required(CONF_CITY_SELECT, default = next(iter(self.citylist))): vol.In(self.citylist),
                }
            )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=self._errors)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""

        #当ha中有经度信息,则也会有纬度信息
        if self.location is None and self.hass.config.latitude:
            self.location = f'{round(self.hass.config.longitude, 4)},{round(self.hass.config.latitude, 4)}'
        
        if user_input is not None:
            self.name = user_input[CONF_NAME]

            # 若key和location未改变,且未提示错误,则提交表单
            if self.location ==  user_input[CONF_LOCATION] and self.key == user_input[CONF_API_KEY]:
                if not self._errors:
                    user_input[CONF_LOCATION] = user_input[CONF_CITY_SELECT]
                    del user_input[CONF_CITY_SELECT]
                    await self.async_set_unique_id(f"{user_input[CONF_LOCATION]}")
                    return self.async_create_entry(title = user_input[CONF_NAME], data=user_input)
            else:
                #否则重新获取城市列表
                self._errors = {}
                self.key = user_input[CONF_API_KEY]
                self.location = user_input[CONF_LOCATION]
                self.citylist = {}
                try:
                    self.citylist = await HeWeather.async_get_location(
                        self.location,
                        self.key
                    )
                except ConnectError:
                    self._errors["base"] = "cannot_connect"
                except InvalidApiKeyError:
                    self._errors[CONF_API_KEY] = "invalid_api_key"
                except ApiParamError:
                    self._errors["base"] = "request_error"

        return self.async_show_config_form()


    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry,) -> HeWeatherOptionsFlowHandler:
        """Options callback for HeWeather."""
        return HeWeatherOptionsFlowHandler(config_entry)


class HeWeatherOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options for HeWeather."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize HeWeather options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input = None):
        """Manage the options."""
        errors = {}
        forecast = {3:"3 days"}
        if user_input is not None:
            if not errors:
                return self.async_create_entry(title="", data=user_input)

        try:
            _flag = await HeWeather.async_get_key_permission(
                self.config_entry.data.get(CONF_LOCATION),
                self.config_entry.data.get(CONF_API_KEY)
            )
        except:
            pass
        else:
            if _flag:
                forecast[7] = "7 days"
                forecast[1] = "24 hours"

        settings_schema = vol.Schema(
            {
                vol.Required(
                    CONF_FORECAST,
                    default=self.config_entry.options.get(CONF_FORECAST, 3),
                ): vol.In(forecast),
                vol.Required(
                    CONF_SCAN_INTERVAL,  
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL, 30),
                ): vol.In([5,10,30,60]),
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=settings_schema, errors=errors
        )
