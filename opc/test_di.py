import unittest
import serial
from modbus_tk import modbus_rtu

try:
    from . import owenio
except Exception as exc:
    import owenio


class TestDI(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.di = owenio.DI16(self.master, 9)

    def test_quality(self):
        for i in range(10):
            with self.subTest(i=i):
                self.di.read()
                self.assertEqual(self.di.quality, 10)

    def test_status(self):
        self.di.read()
        self.assertEqual(self.di.value, [0] * 16)

    def test_btn(self):
        self.di.read()
        self.v = self.di.value
        print('\nЖмите клавиши, для выхода две сразу')

        while True:
            if sum(self.v) > 1: break
            self.di.read()
            if self.v != self.di.value:
                self.v = self.di.value
                if self.v != [0] * 16 and self.v:
                    print(self.v,self.di.quality)

        self.assertEqual(len(self.v), 16)

        while self.di.value != [0] * 16 and self.di.value:
            self.di.read()

    def tearDown(self):
        self.master.close()


if __name__ == '__main__':
    unittest.main(exit=False)
