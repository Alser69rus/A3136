import unittest
import serial
import time
from modbus_tk import modbus_rtu

try:
    from . import electropribor
except Exception as exc:
    import electropribor


class TestMultimeter(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.pv1 = electropribor.ElMultimeter(self.master, 11)
        self.pv2 = electropribor.ElMultimeter(self.master, 12)
        self.pa1 = electropribor.ElMultimeter(self.master, 21)
        self.pa2 = electropribor.ElMultimeter(self.master, 22)
        self.pa3 = electropribor.ElMultimeter(self.master, 23)

    def tearDown(self):
        self.master.close()

    def test_quality(self):
        for i in range(10):
            with self.subTest(i=i):
                self.pv1.read()
                self.pv2.read()
                self.pa1.read()
                self.pa2.read()
                self.pa3.read()

                self.assertEqual(self.pv1.quality, 10)
                self.assertEqual(self.pv2.quality, 10)
                self.assertEqual(self.pa1.quality, 10)
                self.assertEqual(self.pa2.quality, 10)
                self.assertEqual(self.pa3.quality, 10)

    def test_value(self):
        v1 = self.pv1.read()
        v2 = self.pv2.read()
        v3 = self.pa1.read()
        v4 = self.pa2.read()
        v5 = self.pa3.read()

        print('pv1: {} pv2: {} pa1: {} pa2: {} pa3: {} '.format(v1, v2, v3, v4, v5))
        time.sleep(2)

        self.assertIsNotNone(v1)
        self.assertIsNotNone(v2)
        self.assertIsNotNone(v3)
        self.assertIsNotNone(v4)
        self.assertIsNotNone(v5)
