import unittest
import serial
from modbus_tk import modbus_rtu
import modbus_tk.defines as cst
import time


class Testport(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM3', 115200, timeout=0.5))
        self.master.set_timeout(0.5)


    def tearDown(self):
        self.master.close()

    def test_quality_read(self):
        for i in range(100):
            with self.subTest(i=i):
                v = self.master.execute(100, cst.READ_HOLDING_REGISTERS, 0, 6)
                time.sleep(0.01)
                #print(i,v)
                self.assertIsNotNone(v)
