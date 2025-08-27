import logging

from PyQt5 import QtCore
from pymodbus.client.sync import ModbusSerialClient as Client


class Generator(QtCore.QObject):
    updated = QtCore.pyqtSignal()
    warning = QtCore.pyqtSignal(str)
    changed = QtCore.pyqtSignal()
    active_change = QtCore.pyqtSignal(bool)
    '''самодельный трехканальный генератор'''

    def __init__(self, port=None, dev=100, name='DDS Gen', parent=None):
        super().__init__(parent)
        self.name = name
        self.port: Client = port
        self.dev = dev
        self.value = [0] * 3
        self.error = None
        self.active = False

    def read_data(self):
        return self.port.read_holding_registers(0, 6, unit=self.dev)

    def unpack_data(self, data):
        value = [0] * 3
        for i in range(3):
            value[i] = data[i * 2] * 65536 + data[i * 2 + 1]
        return value

    def pack_data(self, value):
        data = [0] * 6
        for i in range(3):
            data[i * 2] = value[i] // 65536
            data[i * 2 + 1] = value[i] % 65536
        return data

    def write_data(self, data):
        return self.port.write_registers(0, data, unit=self.dev)

    @QtCore.pyqtSlot(bool)
    def setActive(self, value=True):
        if self.active != value:
            self.active = value
            self.active_change.emit(value)

    def setValue(self, value, n=-1):
        if n >= 0:
            self.value[n] = value
        else:
            self.value = value
        self.setActive()

    def update(self):
        if not self.active: return
        data = self.pack_data(self.value)
        req = self.write_data(data)
        if not req.isError():
            self.changed.emit()
            self.updated.emit()
            self.setActive(False)
        else:
            self.warning.emit(f'{self.name} warning: {req}')
            logging.warning(f'{self.name} warning: {req}')

