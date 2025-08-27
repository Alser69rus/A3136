from unittest import TestCase
from unittest.mock import MagicMock, Mock
import opc
from opc.icpdas import M7084


class TestM7084(TestCase):
    def setUp(self):
        self.port = Mock()
        self.port.execute.return_value = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        self.freq = M7084(port=self.port, dev=1, name='Част.')

    def test_init(self):
        self.assertEqual(self.freq.dev, 1)
        self.assertEqual(self.freq.port, self.port)
        self.assertEqual(self.freq.name, 'Част.')
        self.assertEqual(self.freq.value, [0] * 8)
        self.assertEqual(self.freq.data, [0] * 16)
        self.assertEqual(self.freq.k, [1] * 8)
        self.assertEqual(self.freq.off, [0] * 8)
        self.assertEqual(self.freq.eps, [1] * 8)
        self.assertEqual(self.freq.active, False)
        self.assertEqual(self.freq._clear_cmd, False)
        self.assertEqual(self.freq._clear_ch, 0)
        self.assertEqual(self.freq._enable_cmd, False)
        self.assertEqual(self.freq._enable_ch, 0)
        self.assertEqual(self.freq._enable_value, True)
        self.assertEqual(self.freq.zero, [0] * 8)
        self.assertEqual(self.freq.raw_value, [0] * 8)
        self.assertIs(self.freq.error, None)

    def test_read_data(self):
        self.assertEqual(self.freq._read_data(), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))

    def test_unpack_data(self):
        self.freq.data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        self.freq.k = [i for i in range(1, 9)]
        self.freq.off = [i for i in range(8)]
        self.assertEqual(self.freq._unpack_data(), [65536, 393221, 983054, 1835035, 2949164, 4325441, 5963866, 7864439])

    def test_unpack_value(self):
        self.freq.zero = [i for i in range(8)]
        self.freq.raw_value = [65536, 393221, 983054, 1835035, 2949164, 4325441, 5963866, 7864439]
        self.assertEqual(self.freq._unpack_value(),
                         [65536, 393220, 983052, 1835032, 2949160, 4325436, 5963860, 7864432])

    def test_update1(self):
        self.freq.k = [i for i in range(1, 9)]
        self.freq.off = [i for i in range(8)]
        self.freq.zero = [i for i in range(8)]
        self.freq.update()
        self.assertEqual(self.freq.value, [0] * 8)

    def test_update2(self):
        self.freq.k = [i for i in range(1, 9)]
        self.freq.off = [i for i in range(8)]
        self.freq.zero = [i for i in range(8)]
        self.freq.active = True
        self.freq.update()
        self.assertEqual(self.freq.value, [65536, 393220, 983052, 1835032, 2949160, 4325436, 5963860, 7864432])

    def test_clear1(self):
        self.freq.k = [i for i in range(1, 9)]
        self.freq.off = [i for i in range(8)]
        self.freq.zero = [i for i in range(8)]
        self.freq.active = True
        self.freq.update()
        opc.icpdas.SOFTWARE_CLEAR = True
        for i in range(8):
            with self.subTest(i=i):
                self.freq.setClear(i)
                self.assertEqual(self.freq.zero[i], self.freq.raw_value[i])
                self.assertEqual(self.freq.value[i], 0)
