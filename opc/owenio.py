import logging

from PyQt5 import QtCore
from pymodbus.client.sync import ModbusSerialClient as Client

import opc.bitwise as bitwise


class OwenModule(QtCore.QObject):
    updated = QtCore.pyqtSignal()
    warning = QtCore.pyqtSignal(str)
    changed = QtCore.pyqtSignal()
    active_change = QtCore.pyqtSignal(bool)

    def __init__(self, port=None, dev=None, name=None, parent=None):
        super().__init__(parent)
        self.value = None
        self.error = None
        self.port: Client = port
        self.dev = dev
        self.active = False
        self.name = name

    @QtCore.pyqtSlot(bool)
    def setActive(self, value=True):
        if self.active != value:
            self.active = value
            self.active_change.emit(value)


class OwenInputModule(OwenModule):
    def __init__(self, port=None, dev=None, name=None, parent=None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)

    def update(self):
        if not self.active: return False
        req = self.read_data()
        if not req.isError():
            data = req.registers
            value = self.unpack_data(data)
        else:
            self.warning.emit(f'{self.name} read warning: {req}')
            logging.warning(f'{self.name} read warning: {req}')
            return False
        if value != self.value:
            self.value = value
            self.changed.emit()
        self.updated.emit()
        return True


class OwenOutputModule(OwenModule):
    def __init__(self, port=None, dev=None, name=None, parent=None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)

    def update(self):
        if not self.active: return False
        data = self.pack_data(self.value)
        req = self.write_data(data)
        if not req.isError():
            self.setActive(False)
            self.changed.emit()
            self.updated.emit()
        else:
            self.warning.emit(f'{self.name} write warning: {req}')
            logging.warning(f'{self.name} write warning: {req}')
            return False
        return True

    def setValue(self, value, n=-1):
        if n >= 0:
            self.value[n] = value
        else:
            self.value = value
        self.setActive()


class DI16(OwenInputModule):
    def __init__(self, port=None, dev=None, name='DI', parent=None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)
        self.value = [0] * 16

    def read_data(self):
        return self.port.read_input_registers(51, 1, unit=self.dev)

    def unpack_data(self, data):
        value = []
        for i in range(16):
            value.append(bitwise.get(data[0], i))
        return value


class AI8(OwenInputModule):
    def __init__(self, port=None, dev=None, name='AI', parent=None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)
        self.value = [0] * 8
        self.k = [1] * 8
        self.off = [0] * 8
        self.eps = [1] * 8

    def read_data(self):
        return self.port.read_input_registers(256, 8, unit=self.dev)

    def unpack_data(self, data):
        values = [i if i < 32768 else 655536 - i for i in data]
        values = [values[i] * self.k[i] + self.off[i] for i in range(8)]
        values = [i if i != 32768 else None for i in values]
        return values


class DO32(OwenOutputModule):

    def __init__(self, port=None, dev=None, name='DO', parent=None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)
        self.value = [0] * 32

    def pack_data(self, data):
        pack = [0, 0]
        for i in range(16):
            pack[0] = bitwise.override(pack[0], i, data[i + 16])
            pack[1] = bitwise.override(pack[1], i, data[i])
        return pack

    def write_data(self, data):
        return self.port.write_registers(97, data, unit=self.dev)


class AO8I(OwenOutputModule):

    def __init__(self, port=None, dev=None, name='AO', parent=None):
        super().__init__(port=port, dev=dev, name=name, parent=parent)
        self.value = [0] * 8

    def pack_data(self, data):
        return [int(i) for i in data]

    def write_data(self, data):
        return self.port.write_registers(0, data, unit=self.dev)
