import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtSvgWidgets import QSvgWidget


from apps.base.theme import (
    TEAL_PRIMARY, TEAL_LIGHT, BG_APP, 
    BG_PANEL, BG_INPUT, TEXT_MUTED,
    BORDER_COLOR, GLOBAL_STYLE
)

from apps.base.base import SidebarButton, ClockWidget, SettingsDialog
from apps.calculator.calculator import CalculatorTab
from apps.drawing.drawing import PaintTab
from apps.stl_viewer.stl_viewer import STLViewerTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Showcase-app")
        self.setMinimumSize(1000, 700)

        # Root widget
        root = QWidget()
        root.setStyleSheet(f"background: {BG_APP};")
        self.setCentralWidget(root)
        root_lay = QHBoxLayout(root)
        root_lay.setContentsMargins(16, 16, 16, 16)
        root_lay.setSpacing(12)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background: {BG_PANEL};
                border-radius: 16px;
                border: 1px solid {BORDER_COLOR};
            }}
        """)
        sb_lay = QVBoxLayout(sidebar)
        sb_lay.setContentsMargins(12, 20, 12, 20)
        sb_lay.setSpacing(6)

        # Logo
        logo_row = QHBoxLayout()
        
        logo_icon = QSvgWidget("icons/Logo.svg")
        logo_icon.setFixedSize(50, 50)

        logo_row.addWidget(logo_icon)
        logo_row.addSpacing(8)

        logo_text = QLabel("MENU")
        logo_text.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {TEXT_MUTED};
            letter-spacing: 1.5px;
        """)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        sb_lay.addLayout(logo_row)
        sb_lay.addSpacing(20)

        nav_items = [
            ("icons/Calculator.svg", "Calculator", 0),
            ("icons/Draw.svg",      "Drawing",    1),
            ("icons/3DSTL.svg",       "STL viewer",     2),
        ]

        self.nav_btns = []
        for icon, label, idx in nav_items:
            btn = SidebarButton(label, active=(idx == 0))
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(20, 20))
            btn.clicked.connect(lambda checked, i=idx: self.switch_tab(i))
            sb_lay.addWidget(btn)
            self.nav_btns.append(btn)

        sb_lay.addStretch()

        # Footer icons: Settings & Help 
        footer_row = QHBoxLayout()
        footer_btn_style = f"""
            QPushButton {{
                background: {BG_INPUT};
                color: {TEXT_MUTED};
                border: none;
                border-radius: 10px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {TEAL_LIGHT};
                color: {TEAL_PRIMARY};
            }}
        """

        btn_settings = QPushButton()
        btn_settings.setIcon(QIcon("icons/Setting.svg"))
        btn_settings.setIconSize(QSize(36, 36))
        btn_settings.setStyleSheet(footer_btn_style)
        btn_settings.setToolTip("Settings")
        btn_settings.clicked.connect(self.open_settings)
        footer_row.addWidget(btn_settings)



        btn_help = QPushButton()
        btn_help.setIcon(QIcon("icons/Question.svg"))
        btn_help.setIconSize(QSize(36, 36))
        btn_help.setStyleSheet(footer_btn_style)
        btn_help.setToolTip("Just native tooltip, nothing special")
        footer_row.addWidget(btn_help)

        footer_row.addStretch()
        sb_lay.addLayout(footer_row)

        root_lay.addWidget(sidebar)

        # Right column: top bar + tabs
        right_col = QVBoxLayout()
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.setSpacing(10)

        # Top bar with clock
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.clock = ClockWidget()
        top_bar.addWidget(self.clock)
        right_col.addLayout(top_bar)

        # Content area (stacked tabs)
        self.tab_widget = QTabWidget()
        self.tab_widget.tabBar().hide()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
        """)

        # Wrap each tab in a white rounded panel
        for TabClass in [CalculatorTab, PaintTab, STLViewerTab]:
            container = QFrame()
            container.setStyleSheet(f"""
                QFrame {{
                    background: {BG_PANEL};
                    border-radius: 16px;
                    border: 1px solid {BORDER_COLOR};
                }}
            """)
            c_lay = QVBoxLayout(container)
            c_lay.setContentsMargins(0, 0, 0, 0)
            c_lay.addWidget(TabClass())
            self.tab_widget.addTab(container, "")

        right_col.addWidget(self.tab_widget, stretch=1)
        root_lay.addLayout(right_col, stretch=1)

    def switch_tab(self, index):
        self.tab_widget.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_btns):
            btn.set_active(i == index)

    def open_settings(self):
        dlg = SettingsDialog(self.clock, self)
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_STYLE)
    window = MainWindow()
    window.resize(1100, 750)
    window.show()
    sys.exit(app.exec())