import logging
from typing import List

from PyQt5 import QtCore
from pymodbus.client.sync import ModbusSerialClient as Client

import opc.bitwise as bitwise

SOFTWARE_CLEAR: bool = True


def to_signed32(n: int) -> float:
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))


class M7084(QtCore.QObject):
    """частотомер icp das M7084"""

    updated = QtCore.pyqtSignal()
    warning = QtCore.pyqtSignal(str)
    changed = QtCore.pyqtSignal()
    active_change = QtCore.pyqtSignal(bool)
    enabled = QtCore.pyqtSignal()
    cleared = QtCore.pyqtSignal()

    def __init__(self, port=None, dev: int = 1, name: str = 'Частотомер', parent=None):
        super().__init__(parent)
        self.name = name
        self.port: Client = port
        self.dev = dev
        self.value: List[float] = [0.0] * 8
        self.raw_value: List[float] = [0.0] * 8
        self.data: List[int] = [0] * 16
        self.zero: List[float] = [0] * 8
        self.k: List[float] = [1.0] * 8
        self.off: List[float] = [0] * 8
        self.eps: List[float] = [1] * 8
        self.error = None
        self.active: bool = False
        self._clear_cmd: bool = False
        self._clear_ch: int = 0
        self._enable_cmd: bool = False
        self._enable_ch: int = 0
        self._enable_value: bool = True

    def read_data(self):
        return self.port.read_input_registers(0, 16, unit=self.dev)

    def unpack_data(self) -> List[float]:
        value: list = [0] * 8
        for i in range(8):
            value[i] = self.data[i * 2] + 65536 * self.data[i * 2 + 1]
            value[i] = to_signed32(value[i])
            value[i] = value[i] * self.k[i] + self.off[i]
        return value

    def unpack_value(self) -> List[float]:
        return [self.raw_value[i] - self.zero[i] for i in range(8)]

    def clear(self) -> bool:
        req = self.port.write_coil(512 + self._clear_ch, True, unit=self.dev)
        if not req.isError():
            self._clear_cmd = False
            self.active = True
            self.cleared.emit()
            return True
        else:
            self.warning.emit(f'{self.name} warning clear {self._clear_ch} err: {req}')
            logging.warning(f'{self.name} warning clear {self._clear_ch} err: {req}')
            return False

    def enable(self) -> bool:
        req = self.port.read_input_registers(489, 1, unit=self.dev)
        if not req.isError():
            data = req.registers
            value = bitwise.override(data, self._enable_ch, self._enable_value)
        else:
            self.warning.emit(f'{self.name} warning enable {self._enable_ch} err: {req}')
            logging.warning(f'{self.name} warning read enable {self._enable_ch} err: {req}')
            return False

        req = self.port.write_register(489, value, unit=self.dev)
        if not req.isError():
            self._enable_cmd = False
            self.enabled.emit()
        else:
            self.warning.emit(f'{self.name} warning write enable {self._enable_ch} err: {req}')
            logging.warning(f'{self.name} warning write enable {self._enable_ch} err: {req}')
            return False
        return True

    def update(self):
        if self._clear_cmd:
            self.clear()

        if self._enable_cmd:
            self.enable()

        if not self.active: return
        req = self.read_data()
        if req.isError():
            self.warning.emit(f'{self.name} warning read err: {req}')
            logging.warning(f'{self.name} warning read err: {req}')
            return False
        self.data = req.registers
        self.raw_value = self.unpack_data()
        value = self.unpack_value()
        if value != self.value:
            self.changed.emit()
        self.value = value
        self.updated.emit()
        return True

    @QtCore.pyqtSlot(bool)
    def setActive(self, value=True):
        if self.active != value:
            self.active = value
            self.active_change.emit(value)

    @QtCore.pyqtSlot(int, bool)
    def setEnable(self, n: int, value: bool):
        self._enable_ch = n
        self._enable_value = value
        self._enable_cmd = True

    @QtCore.pyqtSlot(int)
    def setClear(self, n: int) -> None:
        if SOFTWARE_CLEAR:
            self.zero[n] = self.raw_value[n]
            self.value[n] = 0
            self.cleared.emit()
        else:
            self._clear_ch = n
            self._clear_cmd = True
