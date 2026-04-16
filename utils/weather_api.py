# ==============================================================
# utils/weather_api.py — OpenWeatherMap Integration
# ==============================================================

import json
import threading
from urllib.request import urlopen, Request
from urllib.error import URLError


WEATHER_EMOJIS = {
    "Clear":        "☀️",
    "Clouds":       "☁️",
    "Rain":         "🌧️",
    "Drizzle":      "🌦️",
    "Thunderstorm": "⛈️",
    "Snow":         "❄️",
    "Mist":         "🌫️",
    "Fog":          "🌫️",
    "Haze":         "🌫️",
    "Smoke":        "🌫️",
    "Dust":         "🌪️",
    "Sand":         "🌪️",
    "Ash":          "🌋",
    "Squall":       "💨",
    "Tornado":      "🌀",
}


def get_weather_sync(city: str, api_key: str) -> dict:
    """
    Fetch weather from OpenWeatherMap.
    Returns dict with weather data or error message.
    api_key: Your OpenWeatherMap API key (free at openweathermap.org)
    """
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return _demo_weather(city)

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    try:
        req = Request(url, headers={"User-Agent": "SmartAgriApp/1.0"})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        main       = data.get("main", {})
        weather    = data.get("weather", [{}])[0]
        wind       = data.get("wind", {})
        clouds     = data.get("clouds", {})
        rain       = data.get("rain", {})
        condition  = weather.get("main", "Clear")

        result = {
            "success":     True,
            "city":        data.get("name", city),
            "country":     data.get("sys", {}).get("country", ""),
            "temperature": round(main.get("temp", 0)),
            "feels_like":  round(main.get("feels_like", 0)),
            "humidity":    main.get("humidity", 0),
            "pressure":    main.get("pressure", 0),
            "wind_speed":  round(wind.get("speed", 0) * 3.6, 1),  # m/s → km/h
            "clouds":      clouds.get("all", 0),
            "rain_1h":     rain.get("1h", 0),
            "condition":   condition,
            "description": weather.get("description", "").capitalize(),
            "emoji":       WEATHER_EMOJIS.get(condition, "🌡️"),
            "farming_advice": _get_farming_advice(condition, main.get("temp", 25),
                                                   main.get("humidity", 50)),
        }
        return result

    except URLError as e:
        return {"success": False, "error": f"Network error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_weather_async(city: str, api_key: str, callback):
    """Fetch weather in background thread. Calls callback(result) when done."""
    def _fetch():
        result = get_weather_sync(city, api_key)
        callback(result)
    threading.Thread(target=_fetch, daemon=True).start()


def _get_farming_advice(condition: str, temp: float, humidity: int) -> str:
    """Generate simple farming advice based on weather conditions."""
    advice = []

    if condition in ("Rain", "Drizzle", "Thunderstorm"):
        advice.append("🌧️ Rain expected — do NOT spray pesticides or fungicides today.")
        advice.append("✅ Good time to plant or transplant seedlings.")
        advice.append("⚠️ Check field drainage to prevent waterlogging.")
    elif condition == "Clear":
        if temp > 35:
            advice.append("🌡️ Very hot — water crops in early morning or evening only.")
            advice.append("☀️ Good day for drying harvested grain/pulses.")
        elif 20 <= temp <= 35:
            advice.append("✅ Excellent day for spraying fertilisers or pesticides.")
            advice.append("🌾 Good conditions for field work and harvesting.")
        else:
            advice.append("❄️ Cool weather — monitor for fungal diseases in crops.")
    elif condition == "Clouds":
        advice.append("☁️ Cloudy — suitable for transplanting and field work.")
        advice.append("💧 Low evaporation — reduce irrigation if soil is moist.")

    if humidity > 80:
        advice.append("🍄 High humidity — risk of fungal diseases (blight, mildew). Scout fields.")
    elif humidity < 30:
        advice.append("💨 Low humidity — increase irrigation frequency.")

    return "\n".join(advice) if advice else "🌿 Normal conditions. Regular farming activities can continue."


def _demo_weather(city: str) -> dict:
    """Return demo weather data when API key is not set."""
    return {
        "success":        True,
        "city":           city or "Demo City",
        "country":        "IN",
        "temperature":    28,
        "feels_like":     31,
        "humidity":       65,
        "pressure":       1012,
        "wind_speed":     14.4,
        "clouds":         40,
        "rain_1h":        0,
        "condition":      "Clouds",
        "description":    "Partly cloudy (Demo Mode)",
        "emoji":          "⛅",
        "farming_advice": (
            "☁️ Partly cloudy — suitable for field work and spraying.\n"
            "💡 Add your OpenWeatherMap API key in Settings for real weather data.\n"
            "🌾 Demo mode: Data is not real."
        ),
        "demo": True,
    }
