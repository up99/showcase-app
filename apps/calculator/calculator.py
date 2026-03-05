from PySide6.QtWidgets import ( QWidget, QVBoxLayout, 
     QGridLayout, QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Qt
from apps.base.base import make_card
import re

class CalcLineEdit(QLineEdit):
    """Only allows chars that appear on the calculator buttons."""
    ALLOWED = set("0123456789()+-/*.=")

    # def keyPressEvent(self, event):
    #     # Always allow control keys: backspace, delete, arrows, home, end
    #     if event.key() in (
    #         Qt.Key_Backspace, Qt.Key_Delete,
    #         Qt.Key_Left, Qt.Key_Right,
    #         Qt.Key_Home, Qt.Key_End,
    #     ):
    #         super().keyPressEvent(event)
    #         return
    #     # Allow Enter / Return → trigger equals
    #     if event.key() in (Qt.Key_Return, Qt.Key_Enter):
    #         # bubble up to parent for = handling
    #         self.returnPressed.emit()
    #         return
    #     # Filter: only pass through allowed characters
    #     if event.text() and event.text() in self.ALLOWED:
    #         super().keyPressEvent(event)
    #     # else: silently swallow the key

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Backspace, Qt.Key_Delete,
                           Qt.Key_Left, Qt.Key_Right,
                           Qt.Key_Home, Qt.Key_End):
            super().keyPressEvent(event)
            return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.returnPressed.emit()
            return
        if event.text() and event.text() in self.ALLOWED:
            # Find parent CalculatorTab and check the flag
            parent = self.parent()
            while parent and not isinstance(parent, CalculatorTab):
                parent = parent.parent()
            if parent and parent._just_evaluated:
                if event.text() not in "+-*/()":
                    self.clear()
                parent._just_evaluated = False
            super().keyPressEvent(event)


class CalculatorTab(QWidget):
    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(0)
        outer.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Title row
        title = QLabel("Calculator")
        title.setObjectName("section_title")
        outer.addWidget(title)
        outer.addSpacing(4)
        sub = QLabel("Standard arithmetic operations")
        sub.setObjectName("section_sub")
        outer.addWidget(sub)
        outer.addSpacing(20)

        # Card container
        card, card_lay = make_card("v", (28, 28, 28, 28), 16)
        card.setMaximumWidth(360)
        outer.addWidget(card)
        outer.addStretch()
        

        # Display — filtered input (only calc-button chars allowed)
        self.display = CalcLineEdit()
        self.display.setObjectName("calc_display")
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setPlaceholderText("0")
        self.display.returnPressed.connect(self._evaluate)
        card_lay.addWidget(self.display)

        # History label
        self._just_evaluated = False
        self.history = QLabel("")
        self.history.setObjectName("hint")
        self.history.setAlignment(Qt.AlignRight)
        card_lay.addWidget(self.history)

        card_lay.addSpacing(8)

        # Button grid
        grid = QGridLayout()
        grid.setSpacing(10)

        # Row 0 — C, (, ), /
        self._make_btn(grid, "C",   0, 0, "calc_clear")
        self._make_btn(grid, "(",   0, 1, "calc_op")
        self._make_btn(grid, ")",   0, 2, "calc_op")
        self._make_btn(grid, "/",   0, 3, "calc_op")

        # Row 1 — 7 8 9 *
        self._make_btn(grid, "7",   1, 0, "calc_num")
        self._make_btn(grid, "8",   1, 1, "calc_num")
        self._make_btn(grid, "9",   1, 2, "calc_num")
        self._make_btn(grid, "×",   1, 3, "calc_op")

        # Row 2 — 4 5 6 -
        self._make_btn(grid, "4",   2, 0, "calc_num")
        self._make_btn(grid, "5",   2, 1, "calc_num")
        self._make_btn(grid, "6",   2, 2, "calc_num")
        self._make_btn(grid, "−",   2, 3, "calc_op")

        # Row 3 — 1 2 3 +
        self._make_btn(grid, "1",   3, 0, "calc_num")
        self._make_btn(grid, "2",   3, 1, "calc_num")
        self._make_btn(grid, "3",   3, 2, "calc_num")
        self._make_btn(grid, "+",   3, 3, "calc_op")

        # Row 4 — 0 (span 2) . =
        self._make_btn(grid, "0",   4, 0, "calc_num", col_span=2)
        self._make_btn(grid, ".",   4, 2, "calc_num")
        self._make_btn(grid, "=",   4, 3, "calc_eq")

        card_lay.addLayout(grid)

    def _make_btn(self, grid, text, row, col, obj_name, col_span=1):
        btn = QPushButton(text)
        btn.setObjectName(obj_name)
        btn.clicked.connect(self.on_clicked)
        grid.addWidget(btn, row, col, 1, col_span)
        return btn

    # def on_clicked(self):
    #     text = self.sender().text()
    #     if text == "C":
    #         self.history.setText("")
    #         self.display.clear()
    #     elif text == "=":
    #         self._evaluate()
    #     else:
    #         self.display.insert(text)

    def on_clicked(self):
        text = self.sender().text()
        if text == "C":
            self.history.setText("")
            self.display.clear()
            self._just_evaluated = False
        elif text == "=":
            self._evaluate()
        else:
            if self._just_evaluated and text not in ("+", "-", "*", "/", "×", "−", "(", ")"):
                self.display.clear()
            self._just_evaluated = False
            self.display.insert(text)

    def _evaluate(self):
        expr = self.display.text()
        expr_eval = expr.replace("×", "*").replace("−", "-")
        expr_eval = re.sub(r'\b0+(\d)', r'\1', expr_eval)
        try:
            result = str(round(eval(expr_eval), 3))
            # result = str(eval(expr_eval))
            self.history.setText(expr + " =")
            self.display.setText(result)
            self._just_evaluated = True
        except Exception:
            self.display.setText("Error")
            self._just_evaluated = False