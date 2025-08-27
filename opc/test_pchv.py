import unittest
import serial
import time
from modbus_tk import modbus_rtu
import modbus_tk.defines as cst

try:
    from . import owenio
    from . import owenpchv
except Exception as exc:
    import owenio
    import owenpchv


class TestPCHV(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.master2 = modbus_rtu.RtuMaster(serial.Serial('COM2', 38400, timeout=0.3))

        self.di = owenio.DI16(self.master, 9)
        self.do = owenio.DO32(self.master, 5)
        self.pchv = owenpchv.Pchv(self.master2, 2, 1565, 1.333, verbose=True)

    def tearDown(self):
        self.master.close()
        self.master2.close()

    def test1(self):

        print('Включаем КМ1 и КМ2')
        self.do.value[0] = True
        self.do.value[1] = True
        self.do.write()

        print('Ждем готовности привода')
        self.pchv.wait_ready()

        print('Разгоняем до 500')
        self.pchv.speed = 500
        self.pchv.start()
        self.pchv.write()

        while not self.pchv.on_task:
            self.pchv.read()
        print('speed: {:.0f} feedback: {:.0f} current: {:.0f} quality: {:d}'.format(self.pchv.speed,
                                                                                    self.pchv.feedback_speed,
                                                                                    self.pchv.current_speed,
                                                                                    self.pchv.quality))

        print('Крутим')
        for i in range(5):
            self.pchv.read()
            print(self.pchv.speed)

        print('Разгоняем до 1000')
        self.pchv.speed = 1000
        self.pchv.write()

        while not self.pchv.on_task:
            self.pchv.read()

        print('Крутим')
        for i in range(5):
            self.pchv.read()
            print(self.pchv.speed)

        print('останавливаем')
        self.pchv.stop()
        self.pchv.write()

        while self.pchv.working:
            self.pchv.read()

        print('Отключаем КМ1 и КМ2')
        self.do.value[0] = False
        self.do.value[1] = False
        self.do.update()
