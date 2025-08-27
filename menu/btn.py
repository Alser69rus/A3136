from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class Btn(QtWidgets.QPushButton):
    mouse_entry = pyqtSignal()

    def __init__(self, text='', parent=None):
        super().__init__(parent)
        self.setFlat(True)
        self.setFont(QtGui.QFont('Segoi Ui', 16))
        self.setMouseTracking(True)
        self.setText(text)

        self._color = {'normal': 'rgba(10,10,10,0%)', 'ok': 'rgba(0,200,0,10%)', 'fail': 'rgba(200,0,0,10%)',
                       'pressed': 'rgba(30,0,0,30%)'}

        self._stl = 'QPushButton{{border:2px;border-radius:8px;border-color:black;text-align:left;padding: 8px;' + \
                    'background-color:{};border-style:{}}}' + \
                    ' QPushButton:pressed{{background-color:{}}}'
        self._state = 'normal'
        self._selected = False
        self._icon = {'ok': QtGui.QIcon('menu\\ok.png'), 'fail': QtGui.QIcon('menu\\fail.png'),
                      'normal': QtGui.QIcon('menu\\empty.png')}

        self.set_stl()

    def set_stl(self):
        bg_color = self._color.get(self.state, 'rgba(10,10,10,10%)')
        border = 'solid' if self.selected else 'none'
        bg_pressed = self._color['pressed']
        icon = self._icon.get(self.state, self._icon['normal'])

        self.setStyleSheet(self._stl.format(bg_color, border, bg_pressed))
        self.setIconSize(QtCore.QSize(32, 32))
        self.setIcon(icon)

    def enterEvent(self, *args, **kwargs):
        self.mouse_entry.emit()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.set_stl()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.set_stl()
