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

        self.gen = ddsgenerator.Generator(self.master3, 100)
        self.m7084 = icpdas.M7084(self.master2, 3)
        self.di = owenio.DI16(self.master, 9)
        self.do = owenio.DO32(self.master, 5)
        self.enable_first = True
        self.enable_second = True

    def tearDown(self):
        self.master.close()
        self.master2.close()
        self.master3.close()

    def test_quality(self):
        for i in range(30):
            with self.subTest(i=i):
                self.m7084.read()
                self.assertEqual(self.m7084.quality, 10)

    def test_data(self):
        print('\nПроверка частотомера. Нажать кнопку для выхода\n')
        self.gen.value = [1000, 1500, 2000]
        self.gen.write()
        self.assertEqual(self.gen.quality, 10)
        self.m7084.read()
        self.assertEqual(self.m7084.quality, 10)
        self.m7084.clear(0)
        self.assertEqual(self.m7084.quality, 10)
        self.m7084.clear(2)
        self.assertEqual(self.m7084.quality, 10)
        self.di.read()
        self.v = self.m7084.value[0:3]
        self.do.value = [0] * 9 + [1] * 6 + [0] * 17
        self.do.write()

        while not sum(self.di.value):
            self.di.read()
            self.m7084.read()

            if self.v and self.v != self.m7084.value[0:3]:
                self.v = self.m7084.value[0:3]
                print(self.m7084.value)

        self.m7084.clear(0)
        self.m7084.clear(2)
        self.gen.value = [0, 0, 0]
        self.gen.write()
        self.m7084.read()
        self.assertEqual(self.m7084.value[0:4], [0] * 4)

        self.do.value = [0] * 32
        self.do.write()


if __name__ == '__main__':
    unittest.main(exit=False)
