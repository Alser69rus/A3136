from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial


class Keypad(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Клавиатура')
        self.setFixedWidth(800)
        self.setFixedHeight(320)
        self.setFont(QtGui.QFont('Segoi UI', 20))

        self.grid = QtWidgets.QGridLayout(self)

        self.label = QtWidgets.QLabel('')
        self.label.setFont(QtGui.QFont('Segoi UI', 26))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.label, 0, 0, 1, 50)

        self._shift = False
        self._caps = False

        keys = ['1234567890-+_',
                'йцукенгшщзхъ',
                'фывапролджэ',
                'ячсмитьбю.,',
                ]
        self.btns = []
        for j, row in enumerate(keys):
            self.grid.setRowMinimumHeight(j, 50)
            for i, k in enumerate(row):
                btn = QtWidgets.QPushButton(k)
                self.btns.append(btn)
                btn.setFlat(True)
                btn.setFixedSize(50, 50)
                btn.clicked.connect(partial(self.on_key_press, btn))
                self.grid.addWidget(btn, j + 1, 5 + j + i * 3, 1, 3)

        self.backspace = QtWidgets.QPushButton('\u25c4')
        self.backspace.setFixedHeight(50)
        self.backspace.setFlat(True)
        self.backspace.clicked.connect(self.on_backspace)
        self.grid.addWidget(self.backspace, 1, 46, 1, 5)

        self.shift = QtWidgets.QPushButton('\u2191Shift')
        self.shift.setFixedHeight(50)
        self.shift.setFlat(True)
        self.shift.clicked.connect(self.on_shift)
        self.grid.addWidget(self.shift, 5, 0, 1, 8)

        self.space = QtWidgets.QPushButton('Пробел')
        self.space.setFixedHeight(50)
        self.space.setFlat(True)
        self.space.clicked.connect(self.on_space)
        self.grid.addWidget(self.space, 5, 10, 1, 25)

        self.enter = QtWidgets.QPushButton('Принять')
        self.enter.setFixedHeight(50)
        self.enter.setFlat(True)
        self.enter.clicked.connect(self.accept)
        self.grid.addWidget(self.enter, 3, 42, 1, 10)

        self.cancel = QtWidgets.QPushButton('Отмена')
        self.cancel.setFixedHeight(50)
        self.cancel.setFlat(True)
        self.cancel.clicked.connect(self.reject)
        self.grid.addWidget(self.cancel, 5, 42, 1, 10)

    def on_key_press(self, btn):
        self.label.setText(self.label.text() + btn.text())

    def on_backspace(self):
        self.label.setText(self.label.text()[:-1])

    def on_shift(self):
        self._shift = not self._shift

        for btn in self.btns:
            if self._shift:
                btn.setText(btn.text().upper())
            else:
                btn.setText(btn.text().lower())

    def on_space(self):
        self.label.setText(self.label.text() + ' ')

    def textValue(self) -> str:
        return self.label.text()

    def setText(self, value: str) -> None:
        self.label.setText(value)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([])
    win = QtWidgets.QPushButton('keypad')
    key = Keypad()
    win.clicked.connect(key.exec)
    win.show()
    sys.exit(app.exec())
