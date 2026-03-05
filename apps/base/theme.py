import json
from pathlib import Path

def load_theme(path: str = "apps\\base\\theme.json") -> dict:
    with open(Path(path)) as f:
        return json.load(f)

theme = load_theme()

c  = theme["colors"]
f  = theme["fonts"]
r  = theme["radii"]
b  = theme["borders"]
s  = theme["spacing"]
co = theme["components"]

TEAL_PRIMARY  = c["teal_primary"]
TEAL_DARK     = c["teal_dark"]
TEAL_LIGHT    = c["teal_light"]
BG_APP        = c["bg_app"]
BG_PANEL      = c["bg_panel"]
BG_SIDEBAR    = c["bg_sidebar"]
BG_INPUT      = c["bg_input"]
TEXT_HEADING  = c["text_heading"]
TEXT_BODY     = c["text_body"]
TEXT_MUTED    = c["text_muted"]
BORDER_COLOR  = c["border"]
SHADOW_COLOR  = c["shadow"]

GLOBAL_STYLE = f"""
/* ── App shell ─────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {BG_APP};
    font-family: {f['family']};
    font-size: {f['size_md']}px;
    color: {TEXT_BODY};
}}

/* ── Tab widget ─────────────────────────────── */
QTabWidget::pane {{
    border: none;
    background: transparent;
}}
QTabWidget::tab-bar {{
    alignment: left;
}}
QTabBar {{
    background: transparent;
}}
QTabBar::tab {{
    background: {BG_SIDEBAR};
    color: {TEXT_MUTED};
    border: none;
    border-radius: {r['button']}px;
    padding: 12px 20px;
    margin: 4px 8px;
    font-size: {f['size_md']}px;
    font-weight: 500;
    min-width: 150px;
    text-align: left;
}}
QTabBar::tab:selected {{
    background: {TEAL_PRIMARY};
    color: #FFFFFF;
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    background: {TEAL_LIGHT};
    color: {TEAL_PRIMARY};
}}

/* ── Cards / panels ─────────────────────────── */
QFrame#card {{
    background: {BG_PANEL};
    border-radius: {r['card']}px;
    border: {b['thin']} solid {BORDER_COLOR};
}}

/* ── Primary button ─────────────────────────── */
QPushButton#primary {{
    background-color: {TEAL_PRIMARY};
    color: #FFFFFF;
    border: none;
    border-radius: {r['button']}px;
    padding: {s['button_padding_v']}px {s['button_padding_h']}px;
    font-size: {f['size_md']}px;
    font-weight: {co['button_primary']['font_weight']};
    min-height: {co['button_primary']['min_height']}px;
}}
QPushButton#primary:hover {{
    background-color: {TEAL_DARK};
}}
QPushButton#primary:pressed {{
    background-color: #0C5E58;
}}

/* ── Secondary button ───────────────────────── */
QPushButton#secondary {{
    background-color: {BG_PANEL};
    color: {TEAL_PRIMARY};
    border: {b['medium']} solid {BORDER_COLOR};
    border-radius: {r['button']}px;
    padding: {s['button_padding_v']}px {s['button_padding_h']}px;
    font-size: {f['size_md']}px;
    font-weight: {co['button_secondary']['font_weight']};
    min-height: {co['button_secondary']['min_height']}px;
}}
QPushButton#secondary:hover {{
    background-color: {TEAL_LIGHT};
    border-color: {TEAL_PRIMARY};
}}

/* ── Calculator digit buttons ───────────────── */
QPushButton#calc_num {{
    background-color: {BG_PANEL};
    color: {TEXT_HEADING};
    border: {b['medium']} solid {BORDER_COLOR};
    border-radius: {r['button']}px;
    font-size: {co['calc_num']['font_size']}px;
    font-weight: {co['calc_num']['font_weight']};
    min-height: {co['calc_num']['min_height']}px;
    min-width: {co['calc_num']['min_width']}px;
}}
QPushButton#calc_num:hover {{
    background-color: {TEAL_LIGHT};
    border-color: {TEAL_PRIMARY};
    color: {TEAL_PRIMARY};
}}
QPushButton#calc_num:pressed {{
    background-color: {TEAL_PRIMARY};
    color: white;
}}

/* ── Calculator operator buttons ────────────── */
QPushButton#calc_op {{
    background-color: {TEAL_LIGHT};
    color: {TEAL_PRIMARY};
    border: {b['medium']} solid transparent;
    border-radius: {r['button']}px;
    font-size: {co['calc_op']['font_size']}px;
    font-weight: {co['calc_op']['font_weight']};
    min-height: {co['calc_op']['min_height']}px;
    min-width: {co['calc_op']['min_width']}px;
}}
QPushButton#calc_op:hover {{
    background-color: {TEAL_PRIMARY};
    color: white;
}}

/* ── Calculator equals button ───────────────── */
QPushButton#calc_eq {{
    background-color: {TEAL_PRIMARY};
    color: white;
    border: none;
    border-radius: {r['button']}px;
    font-size: {co['calc_eq']['font_size']}px;
    font-weight: {co['calc_eq']['font_weight']};
    min-height: {co['calc_eq']['min_height']}px;
    min-width: {co['calc_eq']['min_width']}px;
}}
QPushButton#calc_eq:hover {{
    background-color: {TEAL_DARK};
}}

/* ── Calculator clear button ────────────────── */
QPushButton#calc_clear {{
    background-color: {c['danger_bg']};
    color: {c['danger_fg']};
    border: {b['medium']} solid {c['danger_border']};
    border-radius: {r['button']}px;
    font-size: {co['calc_clear']['font_size']}px;
    font-weight: {co['calc_clear']['font_weight']};
    min-height: {co['calc_clear']['min_height']}px;
    min-width: {co['calc_clear']['min_width']}px;
}}
QPushButton#calc_clear:hover {{
    background-color: {c['danger_fg']};
    color: white;
    border-color: {c['danger_fg']};
}}

/* ── Calculator display ──────────────────────── */
QLineEdit#calc_display {{
    background-color: {BG_INPUT};
    border: {b['thick']} solid {BORDER_COLOR};
    border-radius: {r['input']}px;
    color: {TEXT_HEADING};
    font-size: {co['calc_display']['font_size']}px;
    font-weight: {co['calc_display']['font_weight']};
    padding: {co['calc_display']['padding']};
    min-height: {co['calc_display']['min_height']}px;
}}
QLineEdit#calc_display:focus {{
    border-color: {TEAL_PRIMARY};
    background-color: {BG_INPUT};
}}

/* ── STL load button ────────────────────────── */
QPushButton#stl_load {{
    background-color: {TEAL_PRIMARY};
    color: white;
    border: none;
    border-radius: {r['button']}px;
    padding: {co['stl_load']['padding']};
    font-size: {co['stl_load']['font_size']}px;
    font-weight: {co['stl_load']['font_weight']};
    min-height: {co['stl_load']['min_height']}px;
}}
QPushButton#stl_load:hover {{
    background-color: {TEAL_DARK};
}}

/* ── Section labels ──────────────────────────── */
QLabel#section_title {{
    font-size: {co['section_title']['font_size']}px;
    font-weight: {co['section_title']['font_weight']};
    color: {TEXT_HEADING};
}}
QLabel#section_sub {{
    font-size: {co['section_sub']['font_size']}px;
    color: {TEXT_MUTED};
    font-weight: {co['section_sub']['font_weight']};
}}
QLabel#hint {{
    color: {TEXT_MUTED};
    font-size: {f['size_md']}px;
}}
"""

DIALOG_STYLE = f"""
    QDialog {{
        background: {BG_PANEL};
    }}
    QLabel {{
        color: {TEXT_BODY};
        font-size: {f['size_md']}px;
        background: transparent;
    }}
    QRadioButton {{
        color: {TEXT_BODY};
        font-size: {f['size_md']}px;
        spacing: 8px;
        background: transparent;
    }}
    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: {b['thick']} solid {BORDER_COLOR};
        background: white;
    }}
    QRadioButton::indicator:checked {{
        border: {b['thick']} solid {TEAL_PRIMARY};
        background: {TEAL_PRIMARY};
    }}
    QRadioButton::indicator:hover {{
        border-color: {TEAL_PRIMARY};
    }}
    QPushButton {{
        background: {TEAL_PRIMARY};
        color: white;
        border: none;
        border-radius: {r['dialog']}px;
        padding: 8px 24px;
        font-weight: 600;
        font-size: {f['size_md']}px;
    }}
    QPushButton:hover {{
        background: {TEAL_DARK};
    }}
    QFrame#divider {{
        background: {BORDER_COLOR};
        max-height: 1px;
        border: none;
    }}
"""