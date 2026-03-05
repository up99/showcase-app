from PySide6.QtWidgets import (
    QWidget,QVBoxLayout, QPushButton,
    QColorDialog, QFileDialog, QLabel, QFrame, QSizePolicy
)
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap, QIcon
from PySide6.QtCore import Qt, QPoint, QSize

from apps.base.theme import (
    TEAL_PRIMARY, TEAL_LIGHT,
    TEXT_BODY, BORDER_COLOR
)

from apps.base.base import make_card

class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 380)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.color = QColor(TEAL_PRIMARY)
        self.brush_size = 3

    def set_color(self, color):
        self.color = color

    def set_brush(self, size):
        self.brush_size = size

    def clear(self):
        self.pixmap.fill(Qt.white)
        self.update()

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG (*.jpg)")
        if file_path:
            self.pixmap.save(file_path, "JPEG")

    def resizeEvent(self, event):
        new_pixmap = QPixmap(self.size())
        new_pixmap.fill(Qt.white)
        painter = QPainter(new_pixmap)
        painter.drawPixmap(0, 0, self.pixmap)
        self.pixmap = new_pixmap

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.pixmap)
            pen = QPen(self.color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # White rounded canvas
        p.setBrush(QColor("#FFFFFF"))
        p.setPen(QPen(QColor(BORDER_COLOR), 1))
        p.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 12, 12)
        p.drawPixmap(0, 0, self.pixmap)

class PaintTab(QWidget):
    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(0)

        # Title
        title = QLabel("Drawing Canvas")
        title.setObjectName("section_title")
        outer.addWidget(title)
        outer.addSpacing(4)
        sub = QLabel("Freehand drawing — click and drag to paint")
        sub.setObjectName("section_sub")
        outer.addWidget(sub)
        outer.addSpacing(16)

        # Toolbar card
        toolbar_card, tb_lay = make_card("h", (12, 12, 12, 12), 10)
        tb_lay.setAlignment(Qt.AlignLeft)

        # Color swatches
        for hex_color in [TEAL_PRIMARY, "#EF4444", "#F59E0B", "#8B5CF6", "#0F172A"]:
            swatch = QPushButton()
            swatch.setFixedSize(32, 32)
            swatch.setStyleSheet(f"""
                QPushButton {{
                    background-color: {hex_color};
                    border-radius: 8px;
                    border: 2px solid transparent;
                }}
                QPushButton:hover {{
                    border: 2px solid white;
                    outline: 2px solid {hex_color};
                }}
            """)
            swatch.clicked.connect(lambda checked, c=hex_color: self.set_quick_color(c))
            tb_lay.addWidget(swatch)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet(f"color: {BORDER_COLOR};")
        tb_lay.addWidget(sep)

        # Brush size buttons
        for size, label in [(2, "S"), (5, "M"), (10, "L")]:
            btn = QPushButton(label)
            btn.setFixedSize(36, 32)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: white;
                    border: 1.5px solid {BORDER_COLOR};
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 11px;
                    color: {TEXT_BODY};
                }}
                QPushButton:hover {{
                    background: {TEAL_LIGHT};
                    color: {TEAL_PRIMARY};
                    border-color: {TEAL_PRIMARY};
                }}
            """)
            btn.clicked.connect(lambda checked, s=size: self.canvas.set_brush(s))
            tb_lay.addWidget(btn)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setStyleSheet(f"color: {BORDER_COLOR};")
        tb_lay.addWidget(sep2)

        btn_color = QPushButton("Color Picker")
        btn_color.setIcon(QIcon("icons/Color_picker.svg"))
        btn_color.setIconSize(QSize(20, 20))
        btn_color.setObjectName("secondary")
        btn_color.setFixedHeight(36)
        btn_color.setStyleSheet(f"""
            QPushButton {{
                padding: 0 16px;
                font-weight: 600;
            }}
        """)    
        btn_color.clicked.connect(self.choose_color)
        tb_lay.addWidget(btn_color)

        tb_lay.addStretch()

        btn_save = QPushButton("Save JPEG")
        btn_save.setIcon(QIcon("icons/Save.svg"))
        btn_save.setIconSize(QSize(20, 20))
        btn_save.setObjectName("secondary")
        btn_save.setFixedHeight(36)
        btn_save.setStyleSheet(f"""
            QPushButton {{
                padding: 0 16px;
                font-weight: 600;
            }}
        """)
        btn_save.clicked.connect(lambda: self.canvas.save())
        tb_lay.addWidget(btn_save)

        btn_clear = QPushButton("Clear")
        btn_clear.setIcon(QIcon("icons/Clear.svg"))
        btn_clear.setIconSize(QSize(20, 20))
        btn_clear.setFixedHeight(36)
        btn_clear.setStyleSheet(f"""
            QPushButton {{
                background: #FEF2F2;
                color: #EF4444;
                border: 1.5px solid #FECACA;
                border-radius: 10px;
                padding: 0 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: #EF4444;
                color: white;
            }}
        """)
        btn_clear.clicked.connect(lambda: self.canvas.clear())
        tb_lay.addWidget(btn_clear)

        outer.addWidget(toolbar_card)
        outer.addSpacing(12)

        # Canvas
        self.canvas = PaintWidget()
        outer.addWidget(self.canvas, stretch=1)

    def set_quick_color(self, hex_color):
        self.canvas.set_color(QColor(hex_color))

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_color(color)