import unittest
import serial
from modbus_tk import modbus_rtu

try:
    from . import owenio
    from . import icpdas
    from . import ddsgenerator
except Exception as exc:
    import owenio
    import icpdas
    import ddsgenerator


class TestM7084(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.master2 = modbus_rtu.RtuMaster(serial.Serial('COM7', 38400, timeout=0.3))
        self.master3 = modbus_rtu.RtuMaster(serial.Serial('COM3', 115200, timeout=0.3))

        self.di = owenio.DI16(self.master, 9)
        self.do = owenio.DO32(self.master, 5)
        self.m7084 = icpdas.M7084(self.master2, 3)
        self.gen = ddsgenerator.Generator(self.master3, 100)

    def tearDown(self):
        self.master.close()
        self.master2.close()
        self.master3.close()

    def test_quality_read(self):
        for i in range(10):
            with self.subTest(i=i):
                self.gen.read()
                self.assertEqual(self.gen.quality, 10)

    def test_quality_write(self):
        for i in range(10):
            with self.subTest(i=i):
                self.gen.value = [0, 0, 0]
                self.gen.write()
                self.assertEqual(self.gen.quality, 10)

    def test_manual(self):
        print('проверка генератора. нажмите кнопку для выхода')
        self.do.value = [0] * 9 + [1] * 6 + [0] * 17
        self.do.write()
        self.di.read()
        self.v = 0
        self.f = 5
        while not sum(self.di.value):
            self.di.read()
            self.m7084.read()
            if self.v != self.m7084.value[2]:
                self.v = self.m7084.value[2]
                self.gen.value = [self.v, self.v + 1000, self.v + 10000]
                self.gen.write()

            self.m7084.read()
            if self.f != self.m7084.value[5]:
                self.f = self.m7084.value[5]
                print(self.m7084.value, self.gen.quality, self.m7084.quality)


if __name__ == '__main__':
    unittest.main(exit=False)
