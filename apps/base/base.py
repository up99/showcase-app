from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,  QPushButton, 
    QLabel, QFrame, QDialog, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QTimer, QDateTime

from apps.base.theme import (
    TEAL_PRIMARY, TEAL_LIGHT,
    BG_PANEL, TEXT_HEADING, TEXT_BODY, TEXT_MUTED,
    BORDER_COLOR, DIALOG_STYLE
)


def make_card(layout_type="v", margins=(20, 20, 20, 20), spacing=12):
    frame = QFrame()
    frame.setObjectName("card")
    if layout_type == "v":
        lay = QVBoxLayout(frame)
    else:
        lay = QHBoxLayout(frame)
    lay.setContentsMargins(*margins)
    lay.setSpacing(spacing)
    return frame, lay

class SettingsDialog(QDialog):
    def __init__(self, clock_widget, parent=None):
        super().__init__(parent)
        self.clock = clock_widget
        self.setWindowTitle("Settings")
        self.setFixedSize(340, 290)
        self.setStyleSheet(DIALOG_STYLE)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(0)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {TEXT_HEADING};"
        )
        lay.addWidget(title)
        lay.addSpacing(20)

        # Time format section
        lbl_time = QLabel("Time Format")
        lbl_time.setStyleSheet(f"font-weight: 600; color: {TEXT_BODY}; font-size: 13px;")
        lay.addWidget(lbl_time)
        lay.addSpacing(10)

        self.time_group = QButtonGroup(self)
        time_row = QHBoxLayout()
        time_row.setSpacing(20)

        self.rb_12h = QRadioButton("12-hour (08:53 PM)")
        self.rb_24h = QRadioButton("24-hour (20:53)")
        self.time_group.addButton(self.rb_12h, 12)
        self.time_group.addButton(self.rb_24h, 24)
        time_row.addWidget(self.rb_12h)
        time_row.addWidget(self.rb_24h)
        time_row.addStretch()
        lay.addLayout(time_row)

        lay.addSpacing(20)

        # Divider
        div = QFrame()
        div.setObjectName("divider")
        div.setFrameShape(QFrame.HLine)
        lay.addWidget(div)
        lay.addSpacing(20)

        # Date format section
        lbl_date = QLabel("Date Format")
        lbl_date.setStyleSheet(f"font-weight: 600; color: {TEXT_BODY}; font-size: 13px;")
        lay.addWidget(lbl_date)
        lay.addSpacing(10)

        self.date_group = QButtonGroup(self)
        date_row = QHBoxLayout()
        date_row.setSpacing(20)

        self.rb_ymd = QRadioButton("yyyy/mm/dd")
        self.rb_dmy = QRadioButton("dd.mm.yyyy")
        self.date_group.addButton(self.rb_ymd, 0)
        self.date_group.addButton(self.rb_dmy, 1)
        date_row.addWidget(self.rb_ymd)
        date_row.addWidget(self.rb_dmy)
        date_row.addStretch()
        lay.addLayout(date_row)

        lay.addStretch()

        # Close button
        btn = QPushButton("Done")
        btn.setFixedHeight(38)
        btn.clicked.connect(self.accept)
        lay.addWidget(btn, alignment=Qt.AlignRight)

        # Init to current clock state
        if self.clock.time_fmt == 12:
            self.rb_12h.setChecked(True)
        else:
            self.rb_24h.setChecked(True)

        if self.clock.date_fmt == "ymd":
            self.rb_ymd.setChecked(True)
        else:
            self.rb_dmy.setChecked(True)

        # Connect — apply immediately on toggle
        self.rb_12h.toggled.connect(self._apply)
        self.rb_24h.toggled.connect(self._apply)
        self.rb_ymd.toggled.connect(self._apply)
        self.rb_dmy.toggled.connect(self._apply)

    def _apply(self):
        self.clock.time_fmt = 12 if self.rb_12h.isChecked() else 24
        self.clock.date_fmt = "ymd" if self.rb_ymd.isChecked() else "dmy"
        self.clock._update()


class ClockWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {BG_PANEL};
                border-radius: 12px;
                border: 1px solid {BORDER_COLOR};
            }}
        """)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(12)

        # Time
        self.time_lbl = QLabel()
        self.time_lbl.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 700;
            color: {TEXT_HEADING};
            background: transparent;
            border: none;
        """)
        lay.addWidget(self.time_lbl)

        # Divider
        div = QLabel("|")
        div.setStyleSheet(f"color: {BORDER_COLOR}; font-size: 16px; background: transparent; border: none;")
        lay.addWidget(div)

        # Date
        self.date_lbl = QLabel()
        self.date_lbl.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 500;
            color: {TEXT_MUTED};
            background: transparent;
            border: none;
        """)
        lay.addWidget(self.date_lbl)

        # Tick every second
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        self._timer.start(1000)
        # Default formats
        self.time_fmt = 12   # 12 or 24
        self.date_fmt = "ymd"  # "ymd" or "dmy"
        self._update()

    def _update(self):
        now = QDateTime.currentDateTime()
        time_str = now.toString("hh:mm AP") if self.time_fmt == 12 else now.toString("HH:mm")
        date_str = (now.toString("yyyy / MM / dd") if self.date_fmt == "ymd"
                    else now.toString("dd.MM.yyyy"))
        self.time_lbl.setText(time_str)
        self.date_lbl.setText(date_str)


class SidebarButton(QPushButton):
    def __init__(self, label, active=False):
        super().__init__()
        self.setText(label)
        self.setFixedHeight(48)
        self._active = active
        self._apply_style()

    def set_active(self, val):
        self._active = val
        self._apply_style()

    def _apply_style(self):
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {TEAL_PRIMARY};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 16px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {TEXT_MUTED};
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 16px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: {TEAL_LIGHT};
                    color: {TEAL_PRIMARY};
                }}
            """)