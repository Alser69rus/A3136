import unittest
import serial
from modbus_tk import modbus_rtu

try:
    from . import owenio
except Exception as exc:
    import owenio


class TestAO(unittest.TestCase):
    def setUp(self):
        self.master = modbus_rtu.RtuMaster(serial.Serial('COM1', 38400, timeout=0.3))
        self.ao = owenio.AO8I(self.master, 6)
        self.do5 = owenio.DO32(self.master, 5)


    def test_quality(self):
        for i in range(10):
            with self.subTest(i=i):
                self.ao.read()
                self.assertEqual(self.ao.quality, 10)



    def test_status2(self):
        self.ao.value = [1, 2, 3, 4, 5, 6, 7, 8]
        self.ao.write()
        self.ao.read()
        self.assertEqual(self.ao.value, [1, 2, 3, 4, 5, 6, 7, 8])

    def test_output(self):
        print('\nНаблюдайте показания PA3')
        
        self.do5.read()
        self.do5.value[4] = True
        self.do5.value[5] = True
        self.do5.value[15] = True
        self.do5.write()


        for i in range(512):
            with self.subTest(i=i):
                self.ao.value[2] = i
                self.ao.write()
                self.ao.read()
                self.assertEqual(self.ao.value[2], i)

        self.ao.value[2] = 0
        self.ao.write()
        self.do5.value = [0]*32

        self.do5.write()

    def test_pid(self):
        print('\nпроверка пида')

        self.do5.read()
        self.do5.value[4] = True
        self.do5.value[5] = True
        self.do5.value[15] = True
        self.do5.write()


        for i in range(512):
            with self.subTest(i=i):
                self.ao.value[2] = i
                self.ao.write()
                self.ao.read()
                self.assertEqual(self.ao.value[2], i)

        self.ao.value[2] = 0
        self.ao.write()
        self.do5.value = [0] * 32

        self.do5.write()

    def tearDown(self):
        self.master.close()


if __name__ == '__main__':
    unittest.main()
