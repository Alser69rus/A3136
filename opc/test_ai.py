import unittest
import serial
from modbus_tk import modbus_rtu

try:
    from . import owenio
except Exception as exc:
    import owenio


class TestAI(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.ai = owenio.AI8(self.master, 8)

    def test_quality(self):
        for i in range(10):
            with self.subTest(i=i):
                self.ai.read()
                self.assertEqual(self.ai.quality, 10)


    def test_status(self):
        v = self.ai.read()
        print('Чтение AI8', v, self.ai.quality)
        self.assertIsNotNone(v)

    def tearDown(self):
        self.master.close()


if __name__ == '__main__':
    unittest.main()
