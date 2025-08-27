from PyQt5 import QtCore
import modbus_tk.defines as cst
import opc.bitwise as bitwise
from opc.monad import Maybe
from typing import List, Tuple, Any

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
        self.port = port
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

        try:
            self.reset_watchdog()
            print('M-7084 reset ok')
        except Exception as e:
            print('reset m-7084 watchdog fail')
            print(e)

    def reset_watchdog(self):
        delay=50
        self.port.execute(self.dev, cst.WRITE_SINGLE_REGISTER, 488, output_value=delay)
        self.thread().msleep(5)
        self.port.execute(self.dev, cst.WRITE_SINGLE_REGISTER, 491, output_value=0)
        self.thread().msleep(5)
        self.port.execute(self.dev, cst.WRITE_SINGLE_REGISTER, 269, output_value=1)
        self.thread().msleep(5)
        self.port.execute(self.dev, cst.WRITE_SINGLE_REGISTER, 260, output_value=1)
        self.thread().msleep(5)

    def _read_data(self) -> Tuple[int]:
        v = self.port.execute(self.dev, cst.READ_INPUT_REGISTERS, 0, 16)
        self.thread().msleep(2)
        return v

    def _unpack_data(self) -> List[float]:
        value: list = [0] * 8
        for i in range(8):
            value[i] = self.data[i * 2] + 65536 * self.data[i * 2 + 1]
            value[i] = to_signed32(value[i])
            value[i] = value[i] * self.k[i] + self.off[i]
        return value

    def _unpack_value(self) -> List[float]:
        return [self.raw_value[i] - self.zero[i] for i in range(8)]

    def _clear(self) -> bool:
        try:
            self.thread().msleep(5)
            self.port.execute(self.dev, cst.WRITE_SINGLE_COIL, 512 + self._clear_ch, output_value=1)
            self.thread().msleep(5)
            self._clear_cmd = False
            self.active = True
            self.cleared.emit()
            return True
        except Exception as e:
            self.error = e
            self.warning.emit(f'{self.name} warning clear err: {self.error}')
            self.thread().msleep(20)
            return False

    def _enable(self) -> bool:
        try:
            v = self.port.execute(self.dev, cst.READ_INPUT_REGISTERS, 489, 1)
            self.thread().msleep(5)
            data = bitwise.override(v, self._enable_ch, self._enable_value)
            self.port.execute(self.dev, cst.WRITE_SINGLE_REGISTER, 489, output_value=data)
            self.thread().msleep(5)
            self._enable_cmd = False
            self.enabled.emit()
            return True
        except Exception as e:
            self.error = e
            self.warning.emit(f'{self.name} warning enable err: {self.error}')
            self.thread().msleep(20)
            return False

    def update(self):
        if self._clear_cmd:
            self._clear()

        if self._enable_cmd:
            self._enable()

        if self.active:
            try:
                self.data = self._read_data()
                self.raw_value = self._unpack_data()
                value = self._unpack_value()
                if value != self.value:
                    self.changed.emit()
                self.value = value
                self.port.execute(self.dev, cst.WRITE_SINGLE_REGISTER, 491, output_value=0)
                self.thread().msleep(2)
                self.updated.emit()
            except Exception as e:
                self.error = e
                self.warning.emit(f'{self.name} warning read err: {self.error}')
                self.thread().msleep(20)
                self.port._serial.flushInput()
                self.port._serial.flushOutput()
                self.thread().msleep(20)
                # self.port._serial.close()
                # self.thread().msleep(20)
                # self.port._serial.open()
                # self.thread().msleep(20)

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
