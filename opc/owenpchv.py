import logging

from PyQt5 import QtCore #type: ignore
from pymodbus.client.sync import ModbusSerialClient as Client #type: ignore

import opc.bitwise as bitwise #type: ignore

#logging.basicConfig(filename='log\\pchv.txt', filemode='w', level=logging.WARNING)
logging.basicConfig(level=logging.WARNING)

class Response:
    def __init__(self) -> None:
        self.msg=''
        self.registers=[]

    def __str__(self) -> str:
        return f'{self.msg} {self.registers}'

    def isError(self):
        pass

class ResponseOk(Response):
    def __init__(self,reg=[]) -> None:
        super().__init__()
        self.registers=reg
        logging.info(reg)

    def isError(self):
        return False
    
class ResponseFail(Response):
    def __init__(self,msg='') -> None:
        super().__init__()
        self.msg=msg
        logging.info(msg)

    def isError(self):
        return True


class Pchv(QtCore.QObject):
    task_changed = QtCore.pyqtSignal(float)
    speed_changed = QtCore.pyqtSignal(float)
    warning = QtCore.pyqtSignal(str)
    updated = QtCore.pyqtSignal()
    alarmed = QtCore.pyqtSignal(str)
    get_ready = QtCore.pyqtSignal(bool)
    break_on = QtCore.pyqtSignal(bool)
    speed_reached = QtCore.pyqtSignal(bool)
    active_change = QtCore.pyqtSignal(bool)

    def __init__(self, port=None, dev=2, max_speed=1380, fb_k=1.33333333333, fb_off=0, eps=2, name='ПЧВ', parent=None,):
        super().__init__(parent)
        self.name = name
        self.port: Client = port
        self.dev = dev
        self.max_speed = max_speed
        self.fb_k = fb_k
        self.fb_off = fb_off
        self.eps = eps

        #пчв1м01
        self.freq_task=0 #reg 0x2000
        self.command=6 #reg 0x2001 (1 - start, 6 - stop)
        self.state=0 #reg 0x2002
        # bit0 - stop/work
        # bit1 - разгон
        # bit2 - торможение
        # bit 3 - вперед/назад
        # bit4 - исправность
        # bit7 - готовность
        self.freq_out=0 #reg 0x2101

        self.active = False
        self.send_cmd = False
        logging.info(self.port)

    @property
    def ready(self):
        return bitwise.get(self.state, 7)

    @property
    def breaking(self):
        return self.freq_out < 500

    @property
    def on_task(self):
        return self.freq_task - 50 <= self.freq_out <= self.freq_task + 50

    @property
    def working(self):
        return bitwise.get(self.state, 0)

    @property
    def task(self):
        return self.max_speed * self.freq_task / 5000

    @property
    def speed(self):
        return self.current_speed

    @speed.setter
    def speed(self, speed):
        self.set_speed(speed)

    @property
    def current_speed(self):
        return self.freq_out * self.max_speed / 5000

    @QtCore.pyqtSlot()
    def start(self):
        self.command = 1
        self.send_cmd = True

    @QtCore.pyqtSlot()
    def stop(self):
        self.command = 6
        self.send_cmd = True

    @QtCore.pyqtSlot(float)
    def set_speed(self, speed):
        if speed == 0:
            self.freq_task = 0
            self.stop()
        else:
            self.freq_task = int(5000 * speed / self.max_speed)
            self.start()

    @QtCore.pyqtSlot(bool)
    def setActive(self, value=True):
        if self.active != value:
            self.active = value
            self.active_change.emit(value)

    def emit_warning(self, txt, error):
        self.warning.emit(f'{self.name} {txt} warning: {error}')
        logging.info(f'{self.name} {txt} warning: {error}')


    def update(self):
        if not self.active:
            return False
        req_task = self.write_task()
        req_cmd = self.write_command()
        if req_task.isError():
            self.emit_warning("pchv task warning", req_task)
        elif req_cmd.isError():
            self.emit_warning("pchv command warning", req_cmd)  
        else:
            self.task_changed.emit(self.task) 
            logging.info(f'pchv write task {self.task}, command {self.command}') 

        req_state = self.read_state()
        req_err = self.read_err()
        req_freq_out = self.read_freq_out()


        if req_state.isError():
            self.emit_warning("pchv read state err", req_state)
        elif req_err.isError():
            self.emit_warning("pchv error read err", req_err)
        elif req_freq_out.isError():
            self.emit_warning("pchv freq out read err", req_freq_out)
        else:
            logging.info(f'pchv read out {req_freq_out.registers[0]}, state {req_state.registers[0]}')



        self.freq_out = req_freq_out.registers[0]
        self.state = req_state.registers[0]
        self.err = req_err.registers[0]

        self.get_ready.emit(self.ready)
        self.break_on.emit(self.breaking)
        self.speed_reached.emit(self.on_task)
        self.speed_changed.emit(self.speed)

        if self.err:
            self.warning.emit(f'udate err{self.err}')

        self.updated.emit()
        return True
      
    def write_command(self):
        try:
            logging.info('write command')
            resp=self.port.write_registers(0x2001, [self.command], unit=self.dev)
        except Exception as e:
            return ResponseFail(e)
        if resp.isError():
            return ResponseFail(resp)
        return ResponseOk([self.command])

    def write_task(self):
        try:
            logging.info('write task')
            resp=self.port.write_registers(0x2000, [self.freq_task], unit=self.dev)
        except Exception as e:
            return ResponseFail(e)
        if resp.isError():
            return ResponseFail(resp)
        return ResponseOk([self.freq_task])


    def read_state(self):
        try:
            logging.info('read state')
            resp=self.port.read_holding_registers(0x2002, 1, unit=self.dev)
        except Exception as e:
            return ResponseFail(e)
        if resp.isError():
            return ResponseFail(resp)
        return ResponseOk(resp.registers)


    def read_freq_task(self):
        try:
            logging.info('read task')
            resp=self.port.read_holding_registers(0x2100, 1, unit=self.dev)
        except Exception as e:
            return ResponseFail(e)
        if resp.isError():
            return ResponseFail(resp)
        return ResponseOk(resp.registers)


    def read_freq_out(self):
        try:
            logging.info('read out')
            resp=self.port.read_holding_registers(0x2101, 1, unit=self.dev)
        except Exception as e:
            return ResponseFail(e)
        if resp.isError():
            return ResponseFail(resp)
        return ResponseOk(resp.registers)


    def read_err(self):
        try:
            logging.info('read err')
            resp=self.port.read_holding_registers(0x2010, 1, unit=self.dev)
        except Exception as e:
            return ResponseFail(e)
        if resp.isError():
            return ResponseFail(resp)
        return ResponseOk(resp.registers)
