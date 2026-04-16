# 🌱 Smart Agriculture Assistant App

> A complete **Kivy-based mobile/desktop app** for plant disease prediction, farmer support, weather insights, crop recommendations, and government scheme information.

---

## 📱 Screenshots Overview

```
HomeScreen ──► PredictScreen ──► ResultScreen
     │
     ├──► FarmerHelpCenter ──► DiseaseGuide (searchable)
     │                    ──► WeatherScreen (OpenWeatherMap)
     │                    ──► CropRecommendation
     │                    ──► GovtSchemes
     │                    ──► NearbyHelp
     │
     ├──► HistoryScreen (save/view/clear past scans)
     └──► SettingsScreen (language, voice, API key)
```

---

## ✅ Features

| Feature | Description |
|---------|-------------|
| 🔍 Disease Detection | CNN model predicts 38+ plant diseases from leaf photos |
| 📖 Disease Guide | Full database: cause, symptoms, treatment, pesticide, prevention |
| 🌤 Weather | Real-time weather + farming advice (OpenWeatherMap API) |
| 🌾 Crop Recommender | Suggests best crops by soil type + season |
| 📄 Govt Schemes | PM-KISAN, PMFBY, KCC, Soil Health Card, e-NAM, PM Kusum, PKVY |
| 📍 Nearby Centers | KVK locator, Kisan Call Centre, Google Maps integration |
| 🔊 Voice Support | Read disease results aloud (English/Hindi/Marathi) using pyttsx3 |
| 🌐 3 Languages | English, Hindi (हिंदी), Marathi (मराठी) |
| 📊 History | Save, browse, and clear past prediction scans |
| ⚙️ Settings | API key, language, voice speed |

---

## 🚀 Quick Start

### 1. Clone / Download
```bash
git clone <your-repo-url>
cd smart_agri_app
```

### 2. Install Dependencies

**Minimal (Demo Mode — no real model):**
```bash
pip install kivy pyttsx3
```

**Full (with real AI prediction):**
```bash
pip install -r requirements.txt
```

### 3. Add Your CNN Model *(optional)*

Place your trained PlantVillage model as `model.h5` in the project root:
```
smart_agri_app/
├── model.h5          ← your trained model goes here
├── main.py
└── ...
```

**Compatible models:**
- Any Keras/TensorFlow model trained on PlantVillage dataset
- Input: 224×224 RGB images
- Output: 38-class softmax (standard PlantVillage classes)

### 4. Add Weather API Key *(optional)*

1. Get your free API key at [openweathermap.org](https://openweathermap.org/api)
2. Either edit `data/settings.json`, or go to **Settings → API Key** inside the app

### 5. Run the App
```bash
python main.py
```

---

## 📁 Project Structure

```
smart_agri_app/
│
├── main.py                    ← App entry point + all screens
│
├── data/
│   ├── disease_info.py        ← 25+ diseases: cause, treatment, pesticide
│   ├── languages.py           ← English / Hindi / Marathi translations
│   ├── schemes.py             ← 8 Govt schemes + Crop Recommendation engine
│   ├── history.json           ← Auto-generated scan history
│   └── settings.json          ← Auto-generated user settings
│
├── utils/
│   ├── helpers.py             ← Weather API, TTS, History, Model loader
│   └── weather_api.py         ← OpenWeatherMap integration (also in helpers)
│
├── assets/
│   └── icons/                 ← Optional: add your leaf/plant icons here
│
├── model.h5                   ← Your trained CNN model (not included)
├── requirements.txt
└── README.md
```

---

## 🌾 Crop Recommendation Engine

Covers **5 soil types × 3 seasons = 15 combinations:**

| Soil | Kharif | Rabi | Summer |
|------|--------|------|--------|
| Black/Cotton | Cotton, Soybean | Wheat, Gram | Sunflower |
| Red/Laterite | Groundnut, Ragi | Mustard, Barley | Sesame |
| Alluvial | Rice, Sugarcane | Wheat, Potato | Vegetables |
| Sandy/Loam | Bajra, Groundnut | Mustard, Cumin | Watermelon |
| Clay | Rice, Jute | Wheat, Lentil | Moong Bean |

---

## 📄 Government Schemes Covered

1. **PM-KISAN** — ₹6,000/year direct income support
2. **PMFBY** — Crop insurance at 1.5–2% premium
3. **Kisan Credit Card** — ₹3 lakh credit at 4% interest
4. **Soil Health Card** — Free soil testing & nutrient guide
5. **e-NAM** — Online mandi / price discovery
6. **NMSA** — Drip/sprinkler irrigation subsidy
7. **PM Kusum** — Solar pump up to 90% subsidy
8. **PKVY** — ₹50,000/ha for organic farming

---

## 🔊 Voice Support

Uses `pyttsx3` for **offline text-to-speech** (no internet needed):
- Works on Windows, macOS, Linux
- Language voice depends on OS-installed voices
- Speed adjustable in Settings (80–250 wpm)

**Install Hindi/Marathi voices:**
- Windows: Download from Microsoft Language Pack
- Linux: `sudo apt install espeak-ng-data`

---

## 🌤 Weather API

Uses **OpenWeatherMap** free tier:
- 60 calls/minute, 1,000,000 calls/month free
- Sign up at: https://openweathermap.org/api
- Enter key in Settings screen
- Without key: runs in demo mode with sample data

---

## 🤖 CNN Model Details

The app works with any PlantVillage-trained model. The original repo trains on:
- **Dataset:** PlantVillage (38 classes, 87,000 images)
- **Architecture:** Custom CNN or Transfer Learning (MobileNetV2, VGG16)
- **Input size:** 224×224 px
- **Accuracy:** ~95%+ on validation set

**To train your own model**, refer to the original Jupyter notebook in your repo.

---

## 📱 Mobile Deployment (Android/iOS)

Package with **Buildozer** (Android) or **Kivy-iOS** (iOS):

```bash
# Install buildozer
pip install buildozer

# Initialize (creates buildozer.spec)
buildozer init

# Build APK
buildozer android debug

# Deploy to connected device
buildozer android deploy run
```

---

## 📝 Resume Line

> **"Developed a Smart Plant Disease Prediction App using CNN and TensorFlow with a Kivy-based mobile interface, integrating farmer support features including a 25+ disease treatment database, real-time weather insights (OpenWeatherMap), ML-based crop recommendations across 15 soil-season combinations, 8 government scheme guides, and multi-language TTS support in English, Hindi, and Marathi."**

---

## 🙏 Credits

- **PlantVillage Dataset** — Penn State University
- **Kivy Framework** — kivy.org
- **OpenWeatherMap API** — openweathermap.org
- **Indian Government Schemes** — pmkisan.gov.in, pmfby.gov.in

---

*Made with ❤️ for Indian farmers | स्मार्ट कृषि सहायक | स्मार्ट शेती सहायक*
