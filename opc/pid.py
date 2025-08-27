from PyQt5 import QtCore
import time


class PID(QtCore.QObject):
    task_changed = QtCore.pyqtSignal(float)
    updated = QtCore.pyqtSignal()
    changed = QtCore.pyqtSignal(float)
    task_reached = QtCore.pyqtSignal()
    active_change = QtCore.pyqtSignal(bool)
    timeout = QtCore.pyqtSignal()

    def __init__(self, kp, ki, kd, eps=0, parent=None):
        super().__init__(parent)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.e = 0
        self.e1 = 0
        self.e2 = 0
        self.t = time.perf_counter()
        self.active = False
        self.task = 0
        self.u = 0
        self.v_in = 0
        self.last_e = []
        self.eps = eps
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)

    def update(self):
        t = time.perf_counter()
        dt, self.t = t - self.t, t
        if self.active:
            e, e1, e2 = self.task - self.v_in, self.e, self.e1
        else:
            e, e1, e2 = 0, 0, 0
        self.e, self.e1, self.e2 = e, e1, e2
        kp, ki, kd = self.kp, self.ki, self.kd
        p = kp * (e - e1) / dt
        i = ki * e
        d = kd * (e - 2 * e1 + e2) / dt
        du = p + i + d
        if du:
            self.u = self.u + du
            self.changed.emit(self.u)
        self.updated.emit()

        if len(self.last_e) > 9:
            self.last_e = self.last_e[1:]
        self.last_e.append(e)
        if self.active and len(self.last_e) > 9 and all(abs(e) <= self.eps for e in self.last_e):
            self.setActive(False)
            self.task_reached.emit()

    @QtCore.pyqtSlot(float)
    def setVin(self, value):
        self.v_in = value

    @QtCore.pyqtSlot(float)
    def setVout(self, value):
        if not self.active:
            self.u = value

    @QtCore.pyqtSlot(float)
    def setTask(self, value):
        self.task = value
        self.setActive()
        self.last_e = []
        self.task_changed.emit(self.task)

    @QtCore.pyqtSlot(bool)
    def setActive(self, value=True):
        self.active = value
        self.active_change.emit(value)
        if value:
            # if self.timer.isActive():
            #     self.timer.stop()
            self.timer.start(60000)
        # else:
        #     self.timer.stop()
