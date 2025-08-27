import unittest
import serial
import time
from modbus_tk import modbus_rtu

try:
    from . import owenio
except Exception as exc:
    import owenio


class TestDO(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.do1 = owenio.DO32(self.master, 1)
        self.do5 = owenio.DO32(self.master, 5)

    def test_quality_do1(self):
        for i in range(10):
            with self.subTest(i=i):
                self.do1.read()
                self.assertEqual(self.do1.quality, 10, 'качество связи do1')
    

    def test_quality_do5(self):
        for i in range(10):
            with self.subTest(i=i):
                self.do5.read()
                self.assertEqual(self.do5.quality, 10, 'качество связи do5')

    def test_status_do1(self):
        self.do1.read()
        self.assertEqual(self.do1.value, [0] * 32, 'чтение статуса do1')

    def test_status_do5(self):
        self.do5.read()
        self.assertEqual(self.do5.value, [0] * 32, 'чтение статуса do5')

    def test_output_do1(self):
        print('Начинается тестирование DO1')
        time.sleep(5)
        for i in range(32):
            with self.subTest(i=i):
                self.do1.value = [0] * 32
                self.do1.value[i] = True
                self.do1.write()
                time.sleep(0.5)

        self.do1.value = [0] * 32
        self.do1.write()

    def test_output_do5(self):
        print('Начинается тестирование DO5')
        time.sleep(5)
        for i in range(32):
            with self.subTest(i=i):
                self.do5.value = [0] * 32
                self.do5.value[i] = True
                self.do5.write()
                time.sleep(0.5)

        self.do5.value = [0] * 32
        self.do5.write()

    def tearDown(self):
        self.master.close()


if __name__ == '__main__':
    unittest.main()
