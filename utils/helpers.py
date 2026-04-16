# ==============================================================
# utils/helpers.py — ALL utilities in one file
# TTS + History + Model Loader + Weather
# ==============================================================

import os
import json
import threading
import numpy as np
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

# ══════════════════════════════════════════════════════════════
#  MODEL — Class Names
# ══════════════════════════════════════════════════════════════

CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# ══════════════════════════════════════════════════════════════
#  MODEL LOADER
# ══════════════════════════════════════════════════════════════

_model        = None
_model_loaded = False


def load_model(model_path: str = None) -> bool:
    global _model, _model_loaded

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base, "model.h5"),
        os.path.join(base, "model", "model.h5"),
        os.path.join(base, "plant_disease_model.h5"),
        os.path.join(base, "model.keras"),
        "model.h5",
    ]

    if model_path:
        candidates.insert(0, model_path)

    found_path = None
    for path in candidates:
        if os.path.exists(path):
            found_path = path
            print(f"[Model] Found: {path}")
            break

    if not found_path:
        print("[Model] No model.h5 found — running in DEMO mode")
        return False

    try:
        import tensorflow as tf
        print("[Model] Loading... please wait")
        _model        = tf.keras.models.load_model(found_path)
        _model_loaded = True
        print("[Model] Loaded successfully!")
        return True
    except ImportError:
        print("[Model] TensorFlow not installed: pip install tensorflow")
        return False
    except Exception as e:
        print(f"[Model] Load error: {e}")
        return False


def predict(image_path: str) -> tuple:
    global _model, _model_loaded

    if not _model_loaded or _model is None:
        return _demo_predict(image_path)

    try:
        import tensorflow as tf
        img   = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        arr   = tf.keras.preprocessing.image.img_to_array(img)
        arr   = arr / 255.0
        arr   = np.expand_dims(arr, axis=0)
        preds = _model.predict(arr, verbose=0)
        idx   = int(np.argmax(preds[0]))
        conf  = float(preds[0][idx])
        class_name = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else "Unknown"
        return class_name, conf
    except Exception as e:
        print(f"[Model] Prediction error: {e}")
        return "Unknown", 0.0


def _demo_predict(image_path: str) -> tuple:
    import random
    demos = [
        ("Tomato___Early_blight",        0.92),
        ("Potato___Late_blight",         0.87),
        ("Corn_(maize)___Common_rust_",  0.79),
        ("Apple___Apple_scab",           0.84),
        ("Tomato___healthy",             0.96),
        ("Grape___Black_rot",            0.81),
    ]
    return random.choice(demos)


# ══════════════════════════════════════════════════════════════
#  HISTORY MANAGER
# ══════════════════════════════════════════════════════════════

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "history.json"
)


def save_prediction(disease_class: str, display_name: str,
                    confidence: float, image_path: str = ""):
    history = load_history()
    entry = {
        "id":            len(history) + 1,
        "date":          datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "timestamp":     datetime.now().isoformat(),
        "disease_class": display_name,
        "confidence":    round(confidence * 100, 1),
        "image_path":    image_path,
        "plant":         _extract_plant(disease_class),
        "disease":       _extract_disease(display_name),
    }
    history.insert(0, entry)
    history = history[:50]
    _write_history(history)
    return entry


def load_history() -> list:
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"[History] Load error: {e}")
    return []


def clear_history():
    _write_history([])


def _write_history(data: list):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[History] Write error: {e}")


def _extract_plant(class_name: str) -> str:
    parts = class_name.split("___")
    if parts:
        return parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
    return "Unknown"


def _extract_disease(display_name: str) -> str:
    if "–" in display_name:
        return display_name.split("–", 1)[1].replace("✅", "").strip()
    return display_name


# ══════════════════════════════════════════════════════════════
#  TEXT TO SPEECH
# ══════════════════════════════════════════════════════════════

_tts_engine = None
_speaking   = False


def _get_tts_engine():
    global _tts_engine
    if _tts_engine is None:
        try:
            import pyttsx3
            _tts_engine = pyttsx3.init()
            _tts_engine.setProperty("rate",   150)
            _tts_engine.setProperty("volume", 1.0)
        except Exception:
            _tts_engine = None
    return _tts_engine


def speak(text: str, lang: str = "English", speed: float = 150.0):
    global _speaking
    if _speaking:
        stop()

    def _run():
        global _speaking
        engine = _get_tts_engine()
        if engine is None:
            print("[TTS] pyttsx3 not available. pip install pyttsx3")
            return
        try:
            _speaking = True
            engine.setProperty("rate", int(speed))
            _set_voice(engine, lang)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS] Error: {e}")
        finally:
            _speaking = False

    threading.Thread(target=_run, daemon=True).start()


def stop():
    global _tts_engine, _speaking
    if _tts_engine:
        try:
            _tts_engine.stop()
        except Exception:
            pass
    _speaking = False


def is_speaking() -> bool:
    return _speaking


def _set_voice(engine, lang: str):
    try:
        voices   = engine.getProperty("voices")
        lang_map = {
            "Hindi":   ["hi", "hindi"],
            "Marathi": ["mr", "marathi"],
            "English": ["en", "english"],
        }
        keywords = lang_map.get(lang, ["en"])
        for voice in voices:
            for kw in keywords:
                if kw in voice.id.lower() or kw in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    return
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════
#  WEATHER API
# ══════════════════════════════════════════════════════════════

WEATHER_EMOJIS = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
    "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
    "Mist": "🌫️", "Fog": "🌫️", "Haze": "🌫️",
}


def get_weather_sync(city: str, api_key: str) -> dict:
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
        main      = data.get("main",    {})
        weather   = data.get("weather", [{}])[0]
        wind      = data.get("wind",    {})
        clouds    = data.get("clouds",  {})
        rain      = data.get("rain",    {})
        condition = weather.get("main", "Clear")
        return {
            "success":        True,
            "city":           data.get("name", city),
            "country":        data.get("sys", {}).get("country", ""),
            "temperature":    round(main.get("temp",       0)),
            "feels_like":     round(main.get("feels_like", 0)),
            "humidity":       main.get("humidity", 0),
            "pressure":       main.get("pressure", 0),
            "wind_speed":     round(wind.get("speed", 0) * 3.6, 1),
            "clouds":         clouds.get("all", 0),
            "rain_1h":        rain.get("1h", 0),
            "condition":      condition,
            "description":    weather.get("description", "").capitalize(),
            "emoji":          WEATHER_EMOJIS.get(condition, "🌡️"),
            "farming_advice": _get_farming_advice(
                                  condition,
                                  main.get("temp",     25),
                                  main.get("humidity", 50)
                              ),
        }
    except URLError as e:
        return {"success": False, "error": f"Network error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_weather_async(city: str, api_key: str, callback):
    def _fetch():
        result = get_weather_sync(city, api_key)
        callback(result)
    threading.Thread(target=_fetch, daemon=True).start()


def _get_farming_advice(condition: str, temp: float, humidity: int) -> str:
    advice = []
    if condition in ("Rain", "Drizzle", "Thunderstorm"):
        advice.append("🌧️ Rain expected — do NOT spray pesticides today.")
        advice.append("✅ Good time to plant or transplant seedlings.")
        advice.append("⚠️ Check field drainage to prevent waterlogging.")
    elif condition == "Clear":
        if temp > 35:
            advice.append("🌡️ Very hot — water crops in early morning or evening only.")
            advice.append("☀️ Good day for drying harvested grain/pulses.")
        else:
            advice.append("✅ Excellent day for spraying fertilisers or pesticides.")
            advice.append("🌾 Good conditions for field work and harvesting.")
    elif condition == "Clouds":
        advice.append("☁️ Cloudy — suitable for transplanting and field work.")
        advice.append("💧 Low evaporation — reduce irrigation if soil is moist.")
    if humidity > 80:
        advice.append("🍄 High humidity — risk of fungal diseases. Scout fields.")
    elif humidity < 30:
        advice.append("💨 Low humidity — increase irrigation frequency.")
    return "\n".join(advice) if advice else "🌿 Normal conditions. Regular farming activities can continue."


def _demo_weather(city: str) -> dict:
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
            "☁️ Partly cloudy — suitable for field work.\n"
            "💡 Add your OpenWeatherMap API key in Settings for real weather.\n"
            "🌾 Demo mode: Data is not real."
        ),
        "demo": True,
    }
