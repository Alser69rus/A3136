import logging

from PyQt5 import QtCore
from pymodbus.client.sync import ModbusSerialClient as Client


class ElMultimeter(QtCore.QObject):
    changed = QtCore.pyqtSignal(float)
    updated = QtCore.pyqtSignal()
    warning = QtCore.pyqtSignal(str)
    active_change = QtCore.pyqtSignal(bool)
    '''амперметры и вольтметры Электроприбор'''

    def __init__(self, port=None, dev=1, k=1, offset=0, eps=1, name='PX', parent=None):
        super().__init__(parent)
        self.name = name
        self.port: Client = port
        self.dev = dev
        self.value = 0
        self.error = None
        self.active = False
        self.k = k
        self.off = offset
        self.eps = eps

    def read_data(self):
        return self.port.read_input_registers(4, 1, unit=self.dev)

    def unpack_data(self, data):
        value = data[0]
        if value == 32768:
            raise Exception('{}. Выход за пределы диапазона'.format(self.name))
        if value > 32768:
            value = 65536 - value
        value = value * self.k - self.off
        return value

    def update(self):
        if not self.active: return
        req = self.read_data()
        if not req.isError():
            data = req.registers
            value = self.unpack_data(data)
            if abs(value - self.value) > self.eps:
                self.value = value
                self.changed.emit(value)
            self.updated.emit()
        else:
            self.warning.emit(f'{self.name} warning: {req}')
            logging.warning(f'{self.name} warning: {req}')

    @QtCore.pyqtSlot(bool)
    def setActive(self, value=True):
        if self.active != value:
            self.active = value
            self.active_change.emit(value)
