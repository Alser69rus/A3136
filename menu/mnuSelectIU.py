from PyQt5 import QtCore, QtWidgets
from menu.template import Menu
from menu.btn import Btn


class SelectIU(Menu):
    btn_back = QtCore.pyqtSignal(bool)
    btn_ok = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__('Выбор типа исполнительного устройства', parent, col=3)
        self.dev_type = ''
        self.dir = (False, False)
        self.speed = (300, 500, 1000, 500, 500)
        self.pressure = (0.6, 1.0)
        self.current = (1.15, 1.35, 1.95, 2.15)
        self.freq = (20.0, 24.0)
        self.encoder_invert=False

        self.btn_iu_104 = Btn('ЭГУ104')
        self.btn_iu_104R = Btn('ЭГУ104П')
        self.btn_iu_104L = Btn('ЭГУ104Л')
        self.btn_iu_104_01R = Btn('ЭГУ104 - 01П')
        self.btn_iu_102 = Btn('ЭГУ102')
        # self.btn_iu_106M = Btn('ЭГУ106М')
        self.btn_iu_110 = Btn('ЭГУ110')
        self.btn_iu_114 = Btn('ЭГУ114')
        self.btn_iu_116 = Btn('ЭГУ116')

        self.btn_iu_back = Btn('Назад')

        self.set_lst([self.btn_iu_102, self.btn_iu_104, self.btn_iu_104R, self.btn_iu_104L, self.btn_iu_104_01R,
                      self.btn_iu_110, self.btn_iu_114, self.btn_iu_116, self.btn_iu_back])

        self.btn_iu_102.clicked.connect(self.on_select)
        self.btn_iu_104.clicked.connect(self.on_select)
        self.btn_iu_104R.clicked.connect(self.on_select)
        self.btn_iu_104L.clicked.connect(self.on_select)
        self.btn_iu_104_01R.clicked.connect(self.on_select)
        # self.btn_iu_106M.clicked.connect(self.on_select)
        self.btn_iu_110.clicked.connect(self.on_select)
        self.btn_iu_114.clicked.connect(self.on_select)
        self.btn_iu_116.clicked.connect(self.on_select)

        self.btn_iu_back.clicked.connect(self.btn_back)

    @QtCore.pyqtSlot()
    def on_select(self):

        self.dev_type = self.sender().text()
        self.encoder_invert=False
        if self.dev_type == 'ЭГУ104':
            self.dir = (False, True)
            self.speed = (300, 300, 1000, 500, 500)
            self.pressure = (0.8, 1.0)
            self.current = (1.15, 1.35, 1.95, 2.15)
            self.freq = (20.0, 24.0)
        if self.dev_type == 'ЭГУ104П':
            self.dir = (False, False)
            self.speed = (300, 300, 1000, 500, 500)
            self.pressure = (0.8, 1.0)
            self.current = (1.15, 1.35, 1.95, 2.15)
            self.freq = (20.0, 24.0)
        if self.dev_type == 'ЭГУ104Л':
            self.dir = (True, True)
            self.speed = (300, 300, 1000, 500, 500)
            self.pressure = (0.8, 1.0)
            self.current = (1.15, 1.35, 1.95, 2.15)
            self.freq = (20.0, 24.0)
        if self.dev_type == 'ЭГУ104 - 01П':
            self.dir = (True, True)
            self.speed = (300, 300, 1000, 500, 500)
            self.pressure = (0.8, 1.0)
            self.current = (1.15, 1.35, 1.95, 2.15)
            self.freq = (20.0, 24.0)
        if self.dev_type == 'ЭГУ102':
            self.dir = (True, True)
            self.speed = (300, 300, 750, 500, 500)
            self.pressure = (0.6, 0.8)
            self.current = (1.1, 1.4, 1.9, 2.3)
            self.freq = None
        if self.dev_type == 'ЭГУ106М':
            self.dir = (True, True)
            self.speed = (300, 300, 750, 500, 500)
            self.pressure = (0.6, 0.8)
            self.current = (1.1, 1.4, 1.9, 2.3)
            self.freq = None
        if self.dev_type == 'ЭГУ110':
            self.dir = (True, False)
            self.speed = (300, 300, 1400, 500, 700)
            self.pressure = (0.6, 0.7)
            self.current = (1.1, 1.4, 1.9, 2.3)
            self.freq = (20.0, 24.0)
            self.encoder_invert=True
        if self.dev_type == 'ЭГУ114':
            self.dir = (True, True)
            self.speed = (300, 300, 1400, 500, 500)
            self.pressure = (0.6, 0.8)
            self.current = (1.1, 1.4, 1.9, 2.3)
            self.freq = None
        if self.dev_type == 'ЭГУ116':
            self.dir = (True, True)
            self.speed = (300, 300, 1400, 500, 500)
            self.pressure = (0.6, 0.8)
            self.current = (1.1, 1.4, 1.9, 2.3)
            self.freq = None

        self.btn_ok.emit()
