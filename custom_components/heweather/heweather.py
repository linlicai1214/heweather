import asyncio
import logging
import aiohttp
import async_timeout

from .const import (
    CONDITIONS_MAP,
    HEWEATHER_FORECAST,
    HEWEATHER_DATETIME,
    HEWEATHER_CONDITION,
    HEWEATHER_TEMPERATURE,
    HEWEATHER_TEMP_LOW,
    HEWEATHER_HUMIDITY,
    HEWEATHER_PRESSURE,
    HEWEATHER_PRECIPITATION,
    HEWEATHER_PRECIPITATION_PROBABILITY,
    HEWEATHER_VISIBILITY,
    HEWEATHER_WIND_BEARING,
    HEWEATHER_WIND_SPEED,
)

DEFAULT_LOCATION_API_URL = "https://geoapi.qweather.com/v2/city/lookup"
DEFAULT_WEATHER_API_URL = "https://devapi.qweather.com/v7/weather/"
DEFAULT_AIRQUALITY_API_URL = "https://devapi.qweather.com/v7/air/now"

TIMEOUT = 10

_LOGGER = logging.getLogger(__name__)


def format_condition(condition: str) -> str:
    """Return condition from dict CONDITIONS_MAP."""
    for key, value in CONDITIONS_MAP.items():
        if condition in value:
            return key
    return condition


class HeWeather:
    """Main class to perform HeWeather API requests"""
    def __init__(self, location: str, api_key: str, forcast: str):
        # 默认使用公制单位,对于weather实体单位也需设置一致
        self._urlparams = f'?location={location}&key={api_key}&lang=en'
        self._forcast_model = forcast
        
        self.weather_data: dict = {}

        self.now_sources: dict = {}
        self.forecast_sources: list[dict] = []


    # 连接获取数据
    @classmethod
    async def _async_get_data(cls, url):
        try:
            async with async_timeout.timeout(TIMEOUT):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        _data = await resp.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            _LOGGER.error("Access to %s error '%s'", url, type(err).__name__)
            raise ConnectError()
        else:
            _status_code = int(_data["code"])
            if _status_code != 200:
                _LOGGER.error("Access to %s returned status error '%s'", url, _status_code)
                if 401<=_status_code<=403:
                    raise InvalidApiKeyError(_status_code)
                else:
                    raise ApiParamError(_status_code)
            else:
                return _data

    
    # 获取城市信息
    @classmethod
    async def async_get_location(cls, location: str, api_key: str):
        """Retreive location data from HeWeather."""
        try:
            url = f'{DEFAULT_LOCATION_API_URL}?location={location}&key={api_key}'
            data = await cls._async_get_data(url)
        except Exception as e:
            raise e
        else:
            citylist = dict()
            for city in data["location"]:
                citylist[city["id"]] = f'{city["name"]}-{city["adm2"]}-{city["adm1"]}'
            return citylist


    # 获取使用的KEY权限
    @classmethod
    async def async_get_key_permission(cls, location: str, api_key: str):
        """Retreive key permission from HeWeather."""
        try:
            url = f'{DEFAULT_WEATHER_API_URL}24h?location={location}&key={api_key}'
            await cls._async_get_data(url)
        except:
            return False
        else:
            return True


    # 更新天气预报数据
    async def async_fetch_data(self):
        await self._async_get_now()
        if self._forcast_model == 1:
            await self._async_get_forecast24h()
        else:
            await self._async_get_forecast(self._forcast_model)


    # 获取当前天气
    async def _async_get_now(self):
        try:
            resp = await self._async_get_data(DEFAULT_WEATHER_API_URL + "now" + self._urlparams)
        except Exception as e:
            pass
        else:
            self.now_sources = resp['now']
            self.weather_data[HEWEATHER_TEMPERATURE] = float(self.now_sources.get("temp"))
            self.weather_data[HEWEATHER_HUMIDITY] = float(self.now_sources.get("humidity"))
            self.weather_data[HEWEATHER_PRESSURE] = float(self.now_sources.get("pressure"))
            self.weather_data[HEWEATHER_CONDITION] = format_condition(self.now_sources.get("text"))
            self.weather_data[HEWEATHER_VISIBILITY] = float(self.now_sources.get("vis"))
            self.weather_data[HEWEATHER_WIND_BEARING] = float(self.now_sources.get("wind360"))
            self.weather_data[HEWEATHER_WIND_SPEED] = float(self.now_sources.get("windSpeed"))



    # 获取24h天气预报
    async def _async_get_forecast24h(self):
        try:
            resp = await self._async_get_data(DEFAULT_WEATHER_API_URL +"24h"+ self._urlparams)
        except Exception:
            pass
        else:
            self.weather_data[HEWEATHER_FORECAST] = []
            self.forecast_sources = resp['hourly']
            for hourly_data in self.forecast_sources:
                timeseries = dict()
                timeseries[HEWEATHER_DATETIME] = hourly_data["fxTime"]
                timeseries[HEWEATHER_CONDITION] = format_condition(hourly_data["text"])
                timeseries[HEWEATHER_TEMPERATURE] = float(hourly_data["temp"])
                timeseries[HEWEATHER_PRESSURE] = float(hourly_data["pressure"])
                timeseries[HEWEATHER_PRECIPITATION] = float(hourly_data["precip"])
                timeseries[HEWEATHER_WIND_BEARING] = float(hourly_data["wind360"])
                timeseries[HEWEATHER_WIND_SPEED] = float(hourly_data["windSpeed"])
                if hourly_data.get("pop", None):
                    timeseries[HEWEATHER_PRECIPITATION_PROBABILITY] = int(hourly_data["pop"])

                self.weather_data[HEWEATHER_FORECAST].append(timeseries)


    # 获取未来天气预报
    async def _async_get_forecast(self, day:str):
        try:
            resp = await self._async_get_data(f'{DEFAULT_WEATHER_API_URL}{day}d{self._urlparams}')
        except Exception:
            pass
        else:
            self.weather_data[HEWEATHER_FORECAST] = []
            self.forecast_sources = resp['daily']
            for daily_data in self.forecast_sources:
                dateseries = dict()
                dateseries[HEWEATHER_DATETIME] = daily_data["fxDate"]
                dateseries[HEWEATHER_CONDITION] = format_condition(daily_data["textDay"])
                dateseries[HEWEATHER_TEMPERATURE] = float(daily_data["tempMax"])
                dateseries[HEWEATHER_TEMP_LOW] = float(daily_data["tempMin"])
                dateseries[HEWEATHER_PRESSURE] = float(daily_data["pressure"])
                dateseries[HEWEATHER_PRECIPITATION] = float(daily_data["precip"])
                dateseries[HEWEATHER_WIND_BEARING] = float(daily_data["wind360Day"])
                dateseries[HEWEATHER_WIND_SPEED] = float(daily_data["windSpeedDay"])

                self.weather_data[HEWEATHER_FORECAST].append(dateseries)

class ConnectError(Exception):
    """Raised when Http connect in error."""

    def __init__(self, status: str = None):
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidApiKeyError(Exception):
    """Raised when API Key is invalid."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.error_code = status


class ApiParamError(Exception):
    """Raised when coordinates are invalid."""

    def __init__(self, status: str):
        """Initialize."""
        super().__init__(status)
        self.error_code = status
