# ==============================================================
# Smart Agriculture Assistant App
# main.py — Entry point, ScreenManager, KV layout
#
# Run:   python main.py
# Deps:  pip install kivy pyttsx3 (tensorflow for real model)
# ==============================================================

import os
import sys
import json
import threading

# ── Kivy config (must happen before any kivy import) ──────────
os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")
os.environ.setdefault("KIVY_LOG_LEVEL", "warning")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock, mainthread
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window

# ── Project modules ───────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from data.disease_info import get_disease_info, get_severity_color
from data.languages   import t, SUPPORTED_LANGUAGES
from data.schemes     import GOVT_SCHEMES, CROP_RECOMMENDATIONS, get_crop_recommendation, SOIL_TYPES, SEASONS
from utils.helpers import (
    get_weather_sync, get_weather_async,
    save_prediction, load_history, clear_history,
    load_model, predict as model_predict,
    speak, stop as tts_stop, is_speaking, CLASS_NAMES
)

# ── Global App State ──────────────────────────────────────────
APP_STATE = {
    "language":       "English",
    "voice_speed":    150,
    "dark_mode":      False,
    "weather_api_key":"YOUR_API_KEY_HERE",
    "model_loaded":   False,
    "selected_image": None,
    "last_result":    None,
}
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "data", "settings.json")


def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE) as f:
                APP_STATE.update(json.load(f))
    except Exception:
        pass


def save_settings():
    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump({k: v for k, v in APP_STATE.items()
                       if k not in ("model_loaded", "selected_image", "last_result")}, f)
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════
#  COLOURS & THEME
# ══════════════════════════════════════════════════════════════
C = {
    "bg":       [0.06, 0.11, 0.08, 1],    # Dark green-black bg
    "surface":  [0.11, 0.18, 0.13, 1],    # Card surface
    "surface2": [0.15, 0.24, 0.17, 1],    # Lighter card
    "primary":  [0.15, 0.68, 0.38, 1],    # Vibrant green
    "primary2": [0.1,  0.5,  0.28, 1],    # Darker green
    "accent":   [0.95, 0.72, 0.1,  1],    # Yellow/amber
    "accent2":  [0.9,  0.45, 0.1,  1],    # Orange
    "text":     [0.92, 0.97, 0.93, 1],    # Off-white
    "text_dim": [0.6,  0.75, 0.63, 1],    # Dimmed text
    "danger":   [0.85, 0.2,  0.2,  1],    # Red
    "white":    [1,    1,    1,    1],
}

Window.clearcolor = C["bg"]


# ══════════════════════════════════════════════════════════════
#  HELPER WIDGETS
# ══════════════════════════════════════════════════════════════

def make_card(padding=dp(16), spacing=dp(10), orientation="vertical",
              color=None, radius=dp(14)):
    """Create a styled card BoxLayout."""
    box = BoxLayout(orientation=orientation, padding=padding,
                    spacing=spacing, size_hint_y=None)
    box.bind(minimum_height=box.setter("height"))
    color = color or C["surface"]
    with box.canvas.before:
        Color(*color)
        box._rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[radius])
    box.bind(pos=lambda i, v: setattr(i._rect, "pos", v),
             size=lambda i, v: setattr(i._rect, "size", v))
    return box


def make_btn(text, color=None, text_color=None, font_size=dp(15),
             height=dp(52), radius=dp(12), bold=True, **kwargs):
    """Create a styled rounded button."""
    color      = color or C["primary"]
    text_color = text_color or C["white"]
    btn = Button(
        text=text, size_hint_y=None, height=height,
        font_size=font_size, bold=bold, color=text_color,
        background_color=[0, 0, 0, 0], background_normal="",
        **kwargs
    )
    with btn.canvas.before:
        Color(*color)
        btn._rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[radius])
    btn.bind(pos=lambda i, v: setattr(i._rect, "pos", v),
             size=lambda i, v: setattr(i._rect, "size", v))
    return btn


def make_label(text, font_size=dp(14), color=None, bold=False,
               halign="left", height=None, **kwargs):
    """Create a styled label."""
    color = color or C["text"]
    lbl = Label(
        text=text, font_size=font_size, color=color, bold=bold,
        halign=halign, text_size=(None, None), markup=True,
        size_hint_y=None, **kwargs
    )
    if height:
        lbl.height = height
    else:
        lbl.bind(texture_size=lambda i, v: setattr(i, "height", v[1] + dp(6)))
    lbl.bind(size=lambda i, v: setattr(i, "text_size", (v[0], None)))
    return lbl


def screen_header(sm, title, lang, show_back=True):
    """Create a top header bar for a screen."""
    header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60),
                       padding=[dp(10), dp(8)])
    with header.canvas.before:
        Color(*C["surface"])
        header._rect = Rectangle(pos=header.pos, size=header.size)
    header.bind(pos=lambda i, v: setattr(i._rect, "pos", v),
                size=lambda i, v: setattr(i._rect, "size", v))

    if show_back:
        back_btn = Button(
            text=t("back", lang), size_hint=(None, 1), width=dp(90),
            font_size=dp(14), color=C["primary"],
            background_color=[0, 0, 0, 0], background_normal=""
        )
        back_btn.bind(on_press=lambda x: setattr(sm, "current", "home"))
        header.add_widget(back_btn)

    lbl = Label(text=title, font_size=dp(18), bold=True,
                color=C["text"], halign="center")
    header.add_widget(lbl)

    if show_back:
        spacer = Label(size_hint=(None, 1), width=dp(90))
        header.add_widget(spacer)

    return header


def show_toast(parent, message, duration=2.5):
    """Show a small popup message."""
    popup = Popup(
        title="", content=Label(text=message, color=C["white"], font_size=dp(14)),
        size_hint=(0.75, None), height=dp(80),
        background_color=[*C["primary2"][:3], 0.9]
    )
    popup.open()
    Clock.schedule_once(lambda dt: popup.dismiss(), duration)


# ══════════════════════════════════════════════════════════════
#  SCREENS
# ══════════════════════════════════════════════════════════════

class HomeScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)

        # ── Header ───────────────────────────────────────────
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(180),
                           padding=[dp(20), dp(20)])
        with header.canvas.before:
            Color(*C["primary2"])
            header._rect = RoundedRectangle(pos=header.pos, size=header.size,
                                             radius=[0, 0, dp(30), dp(30)])
        header.bind(pos=lambda i, v: setattr(i._rect, "pos", v),
                    size=lambda i, v: setattr(i._rect, "size", v))

        title_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
        title_row.add_widget(Label(text="🌱", font_size=dp(28), size_hint=(None, 1), width=dp(40)))
        title_row.add_widget(Label(text=t("app_title", lang), font_size=dp(20),
                                   bold=True, color=C["white"], halign="left"))
        header.add_widget(title_row)

        header.add_widget(Label(text=t("welcome", lang), font_size=dp(17),
                                bold=True, color=C["white"], halign="left"))
        header.add_widget(Label(text=t("subtitle", lang), font_size=dp(12),
                                color=[0.85, 0.95, 0.85, 1], halign="left",
                                text_size=(Window.width - dp(40), None)))
        root.add_widget(header)

        # ── Scroll Body ───────────────────────────────────────
        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(16), dp(16)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))


        # ── Feature grid (2 columns) ──────────────────────────
        buttons_data = [
            (t("btn_predict", lang), C["primary"],  "predict"),
            (t("btn_help",    lang), C["primary2"], "farmer_help"),
            (t("btn_weather", lang), [0.1, 0.5, 0.75, 1], "weather"),
            (t("btn_crop",    lang), [0.55, 0.35, 0.1, 1], "crop"),
            (t("btn_history", lang), [0.25, 0.4, 0.6, 1],  "history"),
            (t("btn_schemes", lang), [0.55, 0.2, 0.6, 1],  "schemes"),
        ]

        row = None
        for i, (label, color, target) in enumerate(buttons_data):
            if i % 2 == 0:
                row = BoxLayout(orientation="horizontal", spacing=dp(12),
                                size_hint_y=None, height=dp(80))
                body.add_widget(row)
            btn = make_btn(label, color=color, height=dp(80), font_size=dp(14))
            btn.target_screen = target
            btn.bind(on_press=lambda x: setattr(sm, "current", x.target_screen))
            row.add_widget(btn)

        # ── Settings button ───────────────────────────────────
        settings_btn = make_btn(f"⚙  {t('settings', lang)}", color=C["surface2"],
                                text_color=C["text_dim"], height=dp(44), font_size=dp(13))
        settings_btn.bind(on_press=lambda x: setattr(sm, "current", "settings"))
        body.add_widget(settings_btn)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)


class PredictionScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("predict", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(16),
                           padding=[dp(16), dp(16)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        # ── Image preview card ───────────────────────────────
        self.preview_card = make_card(color=C["surface"])
        self.img_widget = Image(size_hint_y=None, height=dp(240), allow_stretch=True,
                                keep_ratio=True)
        if APP_STATE.get("selected_image"):
            self.img_widget.source = APP_STATE["selected_image"]
        else:
            self.img_widget.source = ""

        self.img_label = make_label(t("no_image", lang), font_size=dp(13),
                                    color=C["text_dim"], halign="center")
        self.preview_card.add_widget(self.img_widget)
        self.preview_card.add_widget(self.img_label)
        body.add_widget(self.preview_card)

        # ── Buttons ──────────────────────────────────────────
        gallery_btn = make_btn(t("gallery", lang))
        gallery_btn.bind(on_press=self.open_file_chooser)
        body.add_widget(gallery_btn)

        or_lbl = make_label(t("or", lang), halign="center", color=C["text_dim"])
        body.add_widget(or_lbl)

        # Camera button (placeholder — requires platform-specific implementation)
        camera_btn = make_btn(t("camera", lang), color=C["surface2"], text_color=C["text"])
        camera_btn.bind(on_press=lambda x: show_toast(self, "Camera: connect to platform camera API"))
        body.add_widget(camera_btn)

        # ── Predict button ────────────────────────────────────
        self.predict_btn = make_btn(t("predict_btn", lang), color=C["accent"],
                                    text_color=C["bg"], height=dp(58), font_size=dp(16))
        self.predict_btn.bind(on_press=self.run_prediction)
        body.add_widget(self.predict_btn)

        # Progress bar (hidden until predicting)
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(8))
        self.progress.opacity = 0
        body.add_widget(self.progress)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

    def open_file_chooser(self, *args):
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(12))
        fc = FileChooserListView(
            filters=["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"],
            path=os.path.expanduser("~"),
        )
        content.add_widget(fc)

        btn_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        select_btn = make_btn("✅ Select", height=dp(44))
        cancel_btn = make_btn("✖ Cancel", color=C["surface2"], text_color=C["text"], height=dp(44))
        btn_row.add_widget(select_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)

        popup = Popup(title="Choose Leaf Image", content=content,
                      size_hint=(0.95, 0.85))
        select_btn.bind(on_press=lambda x: self._on_file_selected(fc.selection, popup))
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _on_file_selected(self, selection, popup):
        if selection:
            APP_STATE["selected_image"] = selection[0]
            self.img_widget.source = selection[0]
            self.img_label.text    = os.path.basename(selection[0])
        popup.dismiss()

    def run_prediction(self, *args):
        if not APP_STATE.get("selected_image"):
            show_toast(self, "Please select a leaf image first!")
            return

        self.predict_btn.text = "⏳  Analysing..."
        self.predict_btn.disabled = True
        self.progress.opacity = 1

        def _animate(dt):
            if self.progress.value < 85:
                self.progress.value += 15

        Clock.schedule_interval(_animate, 0.15)

        def _predict():
            class_name, confidence = model_predict(APP_STATE["selected_image"])
            info = get_disease_info(class_name)
            Clock.schedule_once(lambda dt: self._show_result(class_name, confidence, info), 0)

        threading.Thread(target=_predict, daemon=True).start()

    @mainthread
    def _show_result(self, class_name, confidence, info):
        self.progress.value = 100
        self.progress.opacity = 0
        self.predict_btn.text = t("predict_btn", APP_STATE["language"])
        self.predict_btn.disabled = False

        APP_STATE["last_result"] = {
            "class_name":   class_name,
            "confidence":   confidence,
            "info":         info,
            "image_path":   APP_STATE.get("selected_image", ""),
        }
        self.manager.current = "result"


class ResultScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang    = APP_STATE["language"]
        sm      = self.manager
        result  = APP_STATE.get("last_result", {})
        info    = result.get("info", {})
        conf    = result.get("confidence", 0)
        cls     = result.get("class_name", "Unknown")

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("result_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        # ── Disease name + severity ───────────────────────────
        top_card = make_card(color=C["surface"])
        disease_name = info.get("display_name", cls.replace("_", " ").replace("___", " – "))
        top_card.add_widget(make_label(
            f"[b]{info.get('emoji','🌿')}  {disease_name}[/b]",
            font_size=dp(19), color=C["accent"]
        ))

        lang_name = info.get("marathi" if lang == "Marathi" else "hindi" if lang == "Hindi" else "display_name",
                              disease_name)
        top_card.add_widget(make_label(f"{lang_name}", font_size=dp(13), color=C["text_dim"]))

        sev_color = get_severity_color(info.get("severity", "Unknown"))
        top_card.add_widget(make_label(
            f"{t('severity', lang)}: [b]{info.get('severity','Unknown')}[/b]  |  "
            f"{t('confidence', lang)}: [b]{round(conf*100, 1)}%[/b]",
            font_size=dp(14), color=sev_color
        ))

        conf_bar = ProgressBar(max=100, value=conf * 100, size_hint_y=None, height=dp(10))
        top_card.add_widget(conf_bar)
        body.add_widget(top_card)

        # ── Image preview ─────────────────────────────────────
        img_path = result.get("image_path", "")
        if img_path and os.path.exists(img_path):
            img = Image(source=img_path, size_hint_y=None, height=dp(180),
                        allow_stretch=True, keep_ratio=True)
            body.add_widget(img)

        # ── Info sections ─────────────────────────────────────
        sections = [
            ("cause",     "🔬", info.get("cause",      "")),
            ("symptoms",  "🩺", info.get("symptoms",   "")),
            ("treatment", "💊", info.get("treatment",  "")),
            ("pesticide", "🧴", info.get("pesticide",  "")),
            ("prevention","🛡", info.get("prevention", "")),
        ]

        for key, emoji, content in sections:
            if not content:
                continue
            card = make_card(color=C["surface"])
            card.add_widget(make_label(
                f"[b]{emoji}  {t(key, lang)}[/b]",
                font_size=dp(14), color=C["primary"]
            ))
            card.add_widget(make_label(content, font_size=dp(13), color=C["text"]))
            body.add_widget(card)

        # ── Action buttons ────────────────────────────────────
        save_btn  = make_btn(t("save_result", lang), color=C["primary2"])
        speak_btn = make_btn(t("speak_result", lang), color=[0.2, 0.4, 0.65, 1])
        self._speaking = False

        def _save(x):
            entry = save_prediction(cls, disease_name, conf, img_path)
            show_toast(self, t("saved", lang))

        def _speak(x):
            if self._speaking:
                tts_stop()
                speak_btn.text = t("speak_result", lang)
                self._speaking = False
            else:
                text = (f"{disease_name}. "
                        f"{t('cause', lang)}: {info.get('cause','')}. "
                        f"{t('treatment', lang)}: {info.get('treatment','')}")
                speak(text, lang=lang, speed=APP_STATE["voice_speed"])
                speak_btn.text = t("speak_stop", lang)
                self._speaking = True

        save_btn.bind(on_press=_save)
        speak_btn.bind(on_press=_speak)

        btn_row = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        btn_row.add_widget(save_btn)
        btn_row.add_widget(speak_btn)
        body.add_widget(btn_row)

        # ── Scan again button ─────────────────────────────────
        again_btn = make_btn("🔄  Scan Another Leaf", color=C["surface2"],
                             text_color=C["text"], height=dp(44), font_size=dp(13))
        again_btn.bind(on_press=lambda x: setattr(sm, "current", "predict"))
        body.add_widget(again_btn)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)


class FarmerHelpScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("help_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        # Hero banner
        banner = make_card(color=C["primary2"])
        banner.add_widget(make_label(
            "[b]🌱 Farmer Help Center[/b]", font_size=dp(18), color=C["white"]
        ))
        banner.add_widget(make_label(
            "Your complete farming companion — disease guides, weather, schemes & more.",
            font_size=dp(12), color=[0.85, 0.95, 0.85, 1]
        ))
        body.add_widget(banner)

        menu_items = [
            (t("disease_guide", lang), C["primary"],               "disease_guide"),
            (t("weather_info",  lang), [0.1, 0.5, 0.75, 1],       "weather"),
            (t("crop_recommend",lang), [0.55, 0.35, 0.1, 1],      "crop"),
            (t("govt_schemes",  lang), [0.55, 0.2, 0.6, 1],       "schemes"),
            (t("nearby_centers",lang), [0.15, 0.45, 0.55, 1],     "nearby"),
        ]

        for label, color, target in menu_items:
            card = make_card(color=C["surface"], padding=dp(4), spacing=dp(4))
            btn  = make_btn(label, color=color, height=dp(58), font_size=dp(15))
            btn.target_screen = target
            btn.bind(on_press=lambda x: setattr(sm, "current", x.target_screen))
            card.add_widget(btn)
            body.add_widget(card)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)


class DiseaseGuideScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        from data.disease_info import DISEASE_DB

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, "📖 Disease Guide", lang))

        # Search bar
        search_row = BoxLayout(size_hint_y=None, height=dp(52), padding=[dp(10), dp(6)],
                               spacing=dp(8))
        with search_row.canvas.before:
            Color(*C["surface"])
            search_row._rect = Rectangle(pos=search_row.pos, size=search_row.size)
        search_row.bind(pos=lambda i, v: setattr(i._rect, "pos", v),
                        size=lambda i, v: setattr(i._rect, "size", v))

        self.search_input = TextInput(
            hint_text="🔍 Search disease or plant...",
            size_hint_y=None, height=dp(40),
            foreground_color=C["text"], background_color=C["surface2"],
            hint_text_color=C["text_dim"], cursor_color=C["primary"],
            multiline=False, font_size=dp(14),
        )
        self.search_input.bind(text=lambda i, v: self._filter(v))
        search_row.add_widget(self.search_input)
        root.add_widget(search_row)

        self.scroll = ScrollView()
        self.list_box = BoxLayout(orientation="vertical", spacing=dp(10),
                                  padding=[dp(12), dp(12)], size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        self._all_diseases = list(DISEASE_DB.items())
        self._render_list(self._all_diseases, lang, sm)
        self.scroll.add_widget(self.list_box)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def _filter(self, query):
        from data.disease_info import DISEASE_DB
        lang = APP_STATE["language"]
        sm   = self.manager
        query = query.lower()
        filtered = [(k, v) for k, v in DISEASE_DB.items()
                    if query in v["display_name"].lower()
                    or query in k.lower()
                    or query in v.get("hindi","").lower()
                    or query in v.get("marathi","").lower()]
        self.list_box.clear_widgets()
        self._render_list(filtered, lang, sm)

    def _render_list(self, diseases, lang, sm):
        for class_name, info in diseases:
            sev_color = get_severity_color(info.get("severity","Unknown"))
            card = make_card(color=C["surface"], padding=dp(12), spacing=dp(6))

            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44))
            row.add_widget(make_label(
                f"[b]{info.get('emoji','🌿')}  {info['display_name']}[/b]",
                font_size=dp(14), color=C["text"]
            ))
            row.add_widget(make_label(
                info.get("severity",""),
                font_size=dp(12), color=sev_color,
                halign="right", size_hint=(None, 1), width=dp(70)
            ))
            card.add_widget(row)
            card.add_widget(make_label(
                info.get("cause","")[:100] + ("…" if len(info.get("cause","")) > 100 else ""),
                font_size=dp(12), color=C["text_dim"]
            ))

            detail_btn = make_btn("View Details →", height=dp(38), font_size=dp(12),
                                  color=C["primary2"])
            detail_btn.disease_class = class_name
            detail_btn.bind(on_press=lambda x: self._open_detail(x.disease_class))
            card.add_widget(detail_btn)
            self.list_box.add_widget(card)

    def _open_detail(self, class_name):
        info = get_disease_info(class_name)
        lang = APP_STATE["language"]
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(14))
        sv = ScrollView()
        inner = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))

        for key, emoji, data_key in [
            ("cause",     "🔬", "cause"),
            ("symptoms",  "🩺", "symptoms"),
            ("treatment", "💊", "treatment"),
            ("pesticide", "🧴", "pesticide"),
            ("prevention","🛡", "prevention"),
        ]:
            text = info.get(data_key, "")
            if text:
                inner.add_widget(make_label(f"[b]{emoji} {t(key,lang)}[/b]",
                                            font_size=dp(13), color=C["primary"]))
                inner.add_widget(make_label(text, font_size=dp(12), color=C["text"]))

        sv.add_widget(inner)
        content.add_widget(Label(
            text=f"{info.get('emoji','')} {info.get('display_name','')}",
            font_size=dp(16), bold=True, color=C["accent"],
            size_hint_y=None, height=dp(36)
        ))
        content.add_widget(sv)

        popup = Popup(title="", content=content, size_hint=(0.95, 0.9),
                      background_color=[*C["surface"][:3], 1])
        popup.open()


class WeatherScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("weather_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        # City input
        input_card = make_card(color=C["surface"])
        input_card.add_widget(make_label(t("enter_city", lang), font_size=dp(14),
                                         color=C["text_dim"]))
        self.city_input = TextInput(
            text="Nagpur", hint_text=t("enter_city", lang),
            size_hint_y=None, height=dp(46),
            foreground_color=C["text"], background_color=C["surface2"],
            hint_text_color=C["text_dim"], cursor_color=C["primary"],
            multiline=False, font_size=dp(15)
        )
        input_card.add_widget(self.city_input)

        get_btn = make_btn(t("get_weather", lang), color=C["primary"])
        get_btn.bind(on_press=self._fetch_weather)
        input_card.add_widget(get_btn)
        body.add_widget(input_card)

        # Weather result area
        self.result_box = BoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None)
        self.result_box.bind(minimum_height=self.result_box.setter("height"))
        body.add_widget(self.result_box)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

        # Auto-load last city
        Clock.schedule_once(lambda dt: self._fetch_weather(), 0.3)

    def _fetch_weather(self, *args):
        self.result_box.clear_widgets()
        loading = make_label("⏳ " + t("loading", APP_STATE["language"]),
                             font_size=dp(14), color=C["text_dim"], halign="center")
        self.result_box.add_widget(loading)
        city = self.city_input.text.strip() or "Nagpur"

        def _callback(data):
            Clock.schedule_once(lambda dt: self._show_weather(data), 0)

        get_weather_async(city, APP_STATE["weather_api_key"], _callback)

    @mainthread
    def _show_weather(self, data):
        lang = APP_STATE["language"]
        self.result_box.clear_widgets()

        if not data.get("success"):
            self.result_box.add_widget(make_label(
                f"❌ {data.get('error','Error fetching weather')}",
                font_size=dp(14), color=C["danger"]
            ))
            return

        demo_note = " [Demo]" if data.get("demo") else ""

        # Main weather card
        main_card = make_card(color=C["surface"])
        main_card.add_widget(make_label(
            f"[b]{data['emoji']}  {data['city']}, {data['country']}{demo_note}[/b]",
            font_size=dp(20), color=C["accent"]
        ))
        main_card.add_widget(make_label(
            f"[b]{data['temperature']}°C[/b]  (Feels like {data['feels_like']}°C)",
            font_size=dp(28), color=C["white"]
        ))
        main_card.add_widget(make_label(
            data["description"], font_size=dp(14), color=C["text_dim"]
        ))

        # Stats row
        stats = [
            (t("humidity",    lang), f"{data['humidity']}%",    "💧"),
            (t("wind",        lang), f"{data['wind_speed']} km/h", "💨"),
            (t("rain_chance", lang), f"{data['rain_1h']} mm",    "🌧️"),
        ]
        stat_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(80),
                             spacing=dp(8))
        for label, value, emoji in stats:
            stat_box = make_card(color=C["surface2"], padding=dp(8), spacing=dp(2))
            stat_box.add_widget(make_label(emoji, font_size=dp(18), halign="center"))
            stat_box.add_widget(make_label(f"[b]{value}[/b]", font_size=dp(13),
                                            color=C["white"], halign="center"))
            stat_box.add_widget(make_label(label, font_size=dp(10),
                                            color=C["text_dim"], halign="center"))
            stat_row.add_widget(stat_box)
        main_card.add_widget(stat_row)
        self.result_box.add_widget(main_card)

        # Farming advice card
        advice_card = make_card(color=[0.1, 0.25, 0.15, 1])
        advice_card.add_widget(make_label(
            f"[b]🌾 {t('weather_advice', lang)}[/b]",
            font_size=dp(14), color=C["primary"]
        ))
        advice_card.add_widget(make_label(
            data["farming_advice"], font_size=dp(13), color=C["text"]
        ))
        self.result_box.add_widget(advice_card)

        if data.get("demo"):
            note_card = make_card(color=[0.2, 0.15, 0.05, 1])
            note_card.add_widget(make_label(
                "💡 Add your OpenWeatherMap API key in Settings → API Key field for real weather data. "
                "Free key available at openweathermap.org",
                font_size=dp(12), color=C["accent"]
            ))
            self.result_box.add_widget(note_card)


class CropScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("crop_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        # Input card
        input_card = make_card(color=C["surface"])
        input_card.add_widget(make_label(
            f"[b]🌍 {t('soil_type', lang)}[/b]", font_size=dp(14), color=C["text"]
        ))
        self.soil_spinner = Spinner(
            text=SOIL_TYPES[0], values=SOIL_TYPES,
            size_hint_y=None, height=dp(46), font_size=dp(14),
            color=C["text"], background_color=C["surface2"]
        )
        input_card.add_widget(self.soil_spinner)

        input_card.add_widget(make_label(
            f"[b]📅 {t('season', lang)}[/b]", font_size=dp(14), color=C["text"]
        ))
        self.season_spinner = Spinner(
            text=SEASONS[0], values=SEASONS,
            size_hint_y=None, height=dp(46), font_size=dp(14),
            color=C["text"], background_color=C["surface2"]
        )
        input_card.add_widget(self.season_spinner)

        get_btn = make_btn(t("get_recommendation", lang), color=C["accent"],
                           text_color=C["bg"])
        get_btn.bind(on_press=self._get_crops)
        input_card.add_widget(get_btn)
        body.add_widget(input_card)

        self.result_box = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        self.result_box.bind(minimum_height=self.result_box.setter("height"))
        body.add_widget(self.result_box)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

    def _get_crops(self, *args):
        lang   = APP_STATE["language"]
        soil   = self.soil_spinner.text
        season = self.season_spinner.text
        data   = get_crop_recommendation(soil, season)

        self.result_box.clear_widgets()

        # Crops card
        crops_card = make_card(color=C["surface"])
        crops_card.add_widget(make_label(
            f"[b]🌾 {t('recommended_crops', lang)}[/b]",
            font_size=dp(15), color=C["accent"]
        ))
        crops_card.add_widget(make_label(
            f"[b]{soil}[/b] soil  ·  [b]{season}[/b] season",
            font_size=dp(13), color=C["text_dim"]
        ))
        for i, crop in enumerate(data["crops"], 1):
            crops_card.add_widget(make_label(
                f"[b]{i}.[/b]  {crop}", font_size=dp(14), color=C["text"]
            ))
        self.result_box.add_widget(crops_card)

        # Why card
        why_card = make_card(color=C["surface"])
        why_card.add_widget(make_label(
            f"[b]💡 {t('why', lang)}[/b]", font_size=dp(14), color=C["primary"]
        ))
        why_card.add_widget(make_label(data["reason"], font_size=dp(13), color=C["text"]))
        why_card.add_widget(make_label(
            f"[b]Tips:[/b] {data['tips']}", font_size=dp(13), color=C["text_dim"]
        ))
        row_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48),
                            spacing=dp(10))
        row_box.add_widget(make_label(
            f"💧 Water: [b]{data['water_need']}[/b]", font_size=dp(12), color=C["text"]
        ))
        row_box.add_widget(make_label(
            f"💰 Investment: [b]{data['investment']}[/b]", font_size=dp(12), color=C["text"]
        ))
        why_card.add_widget(row_box)
        self.result_box.add_widget(why_card)


class SchemesScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("schemes_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        for scheme in GOVT_SCHEMES:
            card = make_card(color=C["surface"])

            # Header
            hdr = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48))
            with hdr.canvas.before:
                Color(*scheme.get("color", C["primary"]))
                hdr._rect = RoundedRectangle(pos=hdr.pos, size=hdr.size, radius=[dp(10)])
            hdr.bind(pos=lambda i, v: setattr(i._rect, "pos", v),
                     size=lambda i, v: setattr(i._rect, "size", v))
            hdr.add_widget(Label(
                text=f"{scheme['emoji']}  {scheme['name']}",
                font_size=dp(15), bold=True, color=C["white"]
            ))
            card.add_widget(hdr)

            card.add_widget(make_label(scheme["full_name"], font_size=dp(12),
                                        color=C["text_dim"]))
            card.add_widget(make_label(
                f"[b]✅ {t('benefit', lang)}:[/b] {scheme['benefit']}",
                font_size=dp(13), color=C["text"]
            ))
            card.add_widget(make_label(
                f"[b]👤 {t('eligibility', lang)}:[/b] {scheme['eligibility']}",
                font_size=dp(13), color=C["text"]
            ))

            detail_btn = make_btn(f"📋 {t('apply', lang)}", height=dp(40),
                                   font_size=dp(12), color=scheme.get("color", C["primary"]))
            detail_btn.scheme_data = scheme
            detail_btn.bind(on_press=lambda x: self._show_scheme_detail(x.scheme_data))
            card.add_widget(detail_btn)
            body.add_widget(card)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

    def _show_scheme_detail(self, scheme):
        lang    = APP_STATE["language"]
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(14))
        sv      = ScrollView()
        inner   = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))

        inner.add_widget(make_label(
            f"[b]{t('apply', lang)}:[/b]\n{scheme['how_to_apply']}",
            font_size=dp(13), color=C["text"]
        ))
        inner.add_widget(make_label(
            f"[b]📄 Documents Needed:[/b]\n{scheme['documents']}",
            font_size=dp(13), color=C["text"]
        ))
        inner.add_widget(make_label(
            f"[b]📞 {scheme['helpline']}[/b]",
            font_size=dp(13), color=C["primary"]
        ))
        inner.add_widget(make_label(
            f"[b]🌐 {scheme['website']}[/b]",
            font_size=dp(13), color=[0.4, 0.7, 1.0, 1]
        ))

        sv.add_widget(inner)
        content.add_widget(Label(
            text=f"{scheme['emoji']} {scheme['full_name']}",
            font_size=dp(15), bold=True, color=C["accent"],
            size_hint_y=None, height=dp(40)
        ))
        content.add_widget(sv)
        popup = Popup(title="", content=content, size_hint=(0.95, 0.85),
                      background_color=[*C["surface"][:3], 1])
        popup.open()


class NearbyScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, "📍 Nearby Help Centers", lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        info_card = make_card(color=C["surface"])
        info_card.add_widget(make_label(
            "[b]📍 Find Nearest Agriculture Center[/b]",
            font_size=dp(15), color=C["accent"]
        ))
        info_card.add_widget(make_label(
            "To find your nearest Krishi Vigyan Kendra (KVK), fertiliser shop, "
            "or government agriculture center, use the resources below:",
            font_size=dp(13), color=C["text"]
        ))
        body.add_widget(info_card)

        resources = [
            ("🏛️ Krishi Vigyan Kendra (KVK)", "icar.org.in/kvk", "National ICAR network of 731 KVKs. Find your nearest one by district."),
            ("🌾 State Agriculture Department", "State Govt Portal", "Contact your district agriculture office for local guidance."),
            ("💊 Pesticide/Fertiliser Shops", "Google Maps", "Search 'krishi kendra near me' or 'fertiliser shop near me'"),
            ("📞 Kisan Call Centre", "1800-180-1551 (Free)", "24x7 free helpline. Speak to agricultural experts in your language."),
            ("🌱 PM-KISAN Helpline", "155261 / 011-24300606", "For PM-KISAN scheme queries and registration issues."),
            ("🚜 ICAR Helpdesk", "icar.org.in", "Indian Council of Agricultural Research — research and guidance."),
        ]

        for name, source, desc in resources:
            card = make_card(color=C["surface"])
            card.add_widget(make_label(f"[b]{name}[/b]", font_size=dp(14), color=C["primary"]))
            card.add_widget(make_label(source, font_size=dp(12), color=[0.4, 0.7, 1, 1]))
            card.add_widget(make_label(desc, font_size=dp(12), color=C["text_dim"]))
            body.add_widget(card)

        google_btn = make_btn("🗺️  Search on Google Maps", color=[0.2, 0.5, 0.9, 1])
        google_btn.bind(on_press=lambda x: self._open_url("https://maps.google.com/?q=krishi+kendra+near+me"))
        body.add_widget(google_btn)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

    def _open_url(self, url):
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            show_toast(self, "Open your browser and search: krishi kendra near me")


class HistoryScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang    = APP_STATE["language"]
        sm      = self.manager
        history = load_history()

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("history_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(10),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        if not history:
            body.add_widget(make_label(
                t("no_history", lang), font_size=dp(15),
                color=C["text_dim"], halign="center"
            ))
        else:
            clear_btn = make_btn(t("clear_history", lang), color=C["danger"],
                                  height=dp(44), font_size=dp(13))

            def _clear(x):
                clear_history()
                self.on_enter()

            clear_btn.bind(on_press=_clear)
            body.add_widget(clear_btn)

            for entry in history:
                card = make_card(color=C["surface"], padding=dp(12), spacing=dp(6))
                row1 = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(32))
                row1.add_widget(make_label(f"[b]{entry.get('disease_class','')}[/b]",
                                            font_size=dp(13), color=C["accent"]))
                row1.add_widget(make_label(
                    f"{entry.get('confidence',0)}%",
                    font_size=dp(12), color=C["primary"],
                    halign="right", size_hint=(None, 1), width=dp(55)
                ))
                card.add_widget(row1)
                card.add_widget(make_label(
                    f"🌿 {entry.get('plant','')}  ·  📅 {entry.get('date','')}",
                    font_size=dp(11), color=C["text_dim"]
                ))
                body.add_widget(card)

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)


class SettingsScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        lang = APP_STATE["language"]
        sm   = self.manager

        root = BoxLayout(orientation="vertical", spacing=0)
        root.add_widget(screen_header(sm, t("settings_title", lang), lang))

        scroll = ScrollView()
        body   = BoxLayout(orientation="vertical", spacing=dp(14),
                           padding=[dp(14), dp(14)], size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))

        # Language
        lang_card = make_card(color=C["surface"])
        lang_card.add_widget(make_label(f"[b]🌐 {t('language', lang)}[/b]",
                                         font_size=dp(14), color=C["text"]))
        self.lang_spinner = Spinner(
            text=APP_STATE["language"], values=SUPPORTED_LANGUAGES,
            size_hint_y=None, height=dp(46), font_size=dp(14)
        )
        lang_card.add_widget(self.lang_spinner)
        body.add_widget(lang_card)

        # Voice speed
        voice_card = make_card(color=C["surface"])
        voice_card.add_widget(make_label(f"[b]🔊 {t('voice_speed', lang)}[/b]",
                                          font_size=dp(14), color=C["text"]))
        self.speed_label = make_label(
            f"Speed: {APP_STATE['voice_speed']} wpm",
            font_size=dp(12), color=C["text_dim"]
        )
        voice_card.add_widget(self.speed_label)
        self.speed_slider = Slider(
            min=80, max=250, value=APP_STATE["voice_speed"],
            size_hint_y=None, height=dp(40)
        )
        self.speed_slider.bind(value=lambda i, v: setattr(
            self.speed_label, "text", f"Speed: {int(v)} wpm"))
        voice_card.add_widget(self.speed_slider)
        body.add_widget(voice_card)

        # API key
        api_card = make_card(color=C["surface"])
        api_card.add_widget(make_label(
            "[b]🌤 OpenWeatherMap API Key[/b]\n"
            "[size=11]Get your free key at openweathermap.org[/size]",
            font_size=dp(14), color=C["text"]
        ))
        self.api_input = TextInput(
            text=APP_STATE["weather_api_key"],
            hint_text="Enter your API key here",
            size_hint_y=None, height=dp(46),
            foreground_color=C["text"], background_color=C["surface2"],
            hint_text_color=C["text_dim"], multiline=False, font_size=dp(13)
        )
        api_card.add_widget(self.api_input)
        body.add_widget(api_card)

        # Model status
        model_card = make_card(color=C["surface"])
        status = "✅ Model Loaded" if APP_STATE["model_loaded"] else "⚠️ Demo Mode (model.h5 not found)"
        color  = C["primary"] if APP_STATE["model_loaded"] else C["accent"]
        model_card.add_widget(make_label("[b]🤖 CNN Model Status[/b]",
                                          font_size=dp(14), color=C["text"]))
        model_card.add_widget(make_label(status, font_size=dp(13), color=color))
        model_card.add_widget(make_label(
            "Place your model.h5 (PlantVillage trained) in the project root folder.",
            font_size=dp(12), color=C["text_dim"]
        ))
        body.add_widget(model_card)

        # Save button
        save_btn = make_btn(t("save_settings", lang), color=C["primary"],
                             height=dp(54), font_size=dp(15))
        save_btn.bind(on_press=self._save)
        body.add_widget(save_btn)

        # Version
        body.add_widget(make_label(
            t("version", lang), font_size=dp(11), color=C["text_dim"], halign="center"
        ))

        scroll.add_widget(body)
        root.add_widget(scroll)
        self.add_widget(root)

    def _save(self, *args):
        APP_STATE["language"]       = self.lang_spinner.text
        APP_STATE["voice_speed"]    = int(self.speed_slider.value)
        APP_STATE["weather_api_key"]= self.api_input.text.strip()
        save_settings()
        show_toast(self, t("success", APP_STATE["language"]) + " Settings saved!")
        Clock.schedule_once(lambda dt: self.on_enter(), 0.3)


# ══════════════════════════════════════════════════════════════
#  APP CLASS
# ══════════════════════════════════════════════════════════════

class SmartAgriApp(App):
    def build(self):
        load_settings()
        APP_STATE["model_loaded"] = load_model()

        sm = ScreenManager(transition=SlideTransition(duration=0.2))
        screens = [
            HomeScreen(name="home"),
            PredictionScreen(name="predict"),
            ResultScreen(name="result"),
            FarmerHelpScreen(name="farmer_help"),
            DiseaseGuideScreen(name="disease_guide"),
            WeatherScreen(name="weather"),
            CropScreen(name="crop"),
            SchemesScreen(name="schemes"),
            NearbyScreen(name="nearby"),
            HistoryScreen(name="history"),
            SettingsScreen(name="settings"),
        ]
        for screen in screens:
            sm.add_widget(screen)
        return sm

    def get_application_name(self):
        return "Smart Agri Assistant"


if __name__ == "__main__":
    SmartAgriApp().run()
