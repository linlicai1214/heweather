"""Constants for HEWEATHER component."""
CONDITIONS_MAP = {
    "clear-night": {"Clear"},
    "cloudy": {"Overcast"},
    "fog": {
        "Mist",
        "Foggy",
        "Dense fog",
        "Strong fog",
        "Heavy fog",
        "Extra heavy fog",
    },
    "lightning-rainy": {
        "Thundershower",
        "Heavy Thunderstorm",
        "Thundershower with hail",
    },
    "partlycloudy": {
        "Few Clouds",
        "Partly Cloudy",
        "Cloudy"
    },
    "rainy": {
        "Shower Rain",
        "Light Rain",
        "Moderate Rain",
        "Drizzle Rain",
        "Light to moderate rain",
        "Moderate to heavy rain",
        "Rain",
    },
    "pouring": {
        "Heavy Rain",
        "Extreme Rain",
        "Storm",
        "Heavy Storm",
        "Severe Storm",
        "Freezing Rain",
        "Heavy rain to storm",
        "Storm to heavy storm",
        "Heavy to severe storm",
        "Heavy Shower Rain",
    },
    "snowy": {
        "Light Snow",
        "Moderate Snow",
        "Heavy Snow",
        "Snowstorm",
        "Snow Flurry",
        "Light to moderate snow",
        "Moderate to heavy snow",
        "Heavy snow to snowstorm",
        "Snow",
    },
    "snowy-rainy": {
        "Sleet",
        "Rain And Snow",
        "Shower Snow",
    },
    "exceptional": {
        "Haze",
        "Sand",
        "Dust",
        "Duststorm",
        "Sandstorm",
        "Moderate haze",
        "Heavy haze",
        "Severe haze",
        "Hot",
        "Cold",
        "Unknown",
    },
    "sunny": {"Sunny"},
}

HEWEATHER_DATETIME = "datetime"
HEWEATHER_CONDITION = "condition"
HEWEATHER_TEMPERATURE = "temperature"
HEWEATHER_TEMP_LOW = "templow"
HEWEATHER_HUMIDITY = "humidity"
HEWEATHER_PRESSURE = "pressure"
HEWEATHER_PRECIPITATION = "precipitation"
HEWEATHER_PRECIPITATION_PROBABILITY = "precipitation_probability"
HEWEATHER_VISIBILITY = "visibility"
HEWEATHER_WIND_BEARING = "wind_bearing"
HEWEATHER_WIND_SPEED = "wind_speed"
HEWEATHER_OZONE = "ozone"
HEWEATHER_CLOUD = "cloud"
HEWEATHER_FORECAST = "forecast"

CONF_FORECAST = "forecast"
CONF_CITY_SELECT = "city_select"

DEFAULT_NAME = "Home"

ATTRIBUTION = "来自和风天气的天气数据"
DOMAIN = "heweather"
