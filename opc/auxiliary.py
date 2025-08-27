from PyQt5 import QtCore
import time


class Btn(QtCore.QObject):
    clicked = QtCore.pyqtSignal()

    def __init__(self, dev, pin, parent=None):
        super().__init__(parent)
        self.dev = dev
        self.pin = pin
        self.old = 0
        self.value = 0

    @property
    def down(self):
        return self.value

    @property
    def up(self):
        return not self.down

    @property
    def change(self):
        return self.old != self.value

    @property
    def click(self):

        return self.change and self.down

    def read(self):

        if not self.dev.value: return None
        self.old = self.value
        self.value = self.dev.value[self.pin]
        if self.click:
            self.clicked.emit()
        return self.value


class Encoder(QtCore.QObject):
    updated = QtCore.pyqtSignal(float, float)

    def __init__(self, dev, pin, k=1, offset=0, parent=None):
        super().__init__(parent)
        self.dev = dev
        self.pin = pin
        self.value = 0
        self.old = 0
        self.offset = offset
        self.k = k

    def read(self):
        if not self.dev.value: return None
        self.old = self.value
        self.value = self.dev.value[self.pin]
        self.value = self.value * self.k + self.offset
        self.updated.emit(self.value, self.value - self.old)
        return self.value

    def setZero(self):
        self.offset = self.offset - self.value

    def setK(self, value):
        self.k = (value - self.offset) * self.k / (self.value - self.offset)


class Pid(QtCore.QObject):
    """пид-регулятор для установки тока в силовой цепи"""
    value_changed = QtCore.pyqtSignal(float)

    def __init__(self, p, i, d, dev_in, dev_out, pin_out, parent=None):
        super().__init__(parent)
        self.p = -p
        self.i = -i
        self.d = -d
        self.u = 0
        self.e1 = 0
        self.e2 = 0
        self._value = 0
        self.devi = dev_in
        self.devo = dev_out
        self.pino = pin_out
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.e = 0

    def write(self):
        self.e = self._value - self.devi.value

        self.kp = self.p * (self.e - self.e1)
        self.ki = self.i * self.p * self.e
        self.kd = self.d * self.p * (self.e - 2 * self.e1 + self.e2)

        self.u = self.u + self.kp + self.ki - self.kd

        if self.u < 0: self.u = 0
        if self.u > 1000: self.u = 1000

        self.e2 = self.e1
        self.e1 = self.e

        self.devo.value[self.pino] = int(self.u)

    def reset(self):
        self.u = self.devo.value[self.pino]
        self._value = self.devi.value
        self.e = 0
        self.e1 = 0
        self.e2 = 0
        self.kp = 0
        self.kd = 0
        self.ki = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value
        self.value_changed.emit(value)
