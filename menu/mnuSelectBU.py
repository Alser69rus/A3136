from PyQt5 import QtCore, QtWidgets
from menu.template import Menu
from menu.btn import Btn


class SelectBU(Menu):
    btn_back = QtCore.pyqtSignal()
    btn_ok = QtCore.pyqtSignal()

    def __init__(self, parent=None, form=None):
        super().__init__('Выбор типа блока управления', parent, col=3)
        self.dev_type = ''
        self.form = form

        self.btn_bu_3_06 = Btn('ЭРЧМ30Т3-06')
        self.btn_bu_3_07 = Btn('ЭРЧМ30Т3-07')
        self.btn_bu_3_04 = Btn('ЭРЧМ30Т3-04')
        self.btn_bu_3_08 = Btn('ЭРЧМ30Т3-08')
        self.btn_bu_3_08_01 = Btn('ЭРЧМ30Т3-08-01')
        self.btn_bu_3_02 = Btn('ЭРЧМ30Т3-02')
        self.btn_bu_3_05 = Btn('ЭРЧМ30Т3-05')
        self.btn_bu_3_10 = Btn('ЭРЧМ30Т3-10')
        self.btn_bu_3_10_01 = Btn('ЭРЧМ30Т3-10-01')
        self.btn_bu_3_12 = Btn('ЭРЧМ30Т3-12')
        self.btn_bu_3_12_01 = Btn('ЭРЧМ30Т3-12-01')
        self.btn_bu_3_12_02 = Btn('ЭРЧМ30Т3-12-02')
        self.btn_bu_3_12_03 = Btn('ЭРЧМ30Т3-12-03')
        self.btn_bu_4_01 = Btn('ЭРЧМ30Т4-01')
        self.btn_bu_4_02 = Btn('ЭРЧМ30Т4-02')
        self.btn_bu_4_02_01 = Btn('ЭРЧМ30Т4-02-01')
        self.btn_bu_4_02_02 = Btn('ЭРЧМ30Т4-02-02')
        self.btn_bu_4_03 = Btn('ЭРЧМ30Т4-03')

        self.btn_bu_back = Btn('Назад')

        lst = [self.btn_bu_3_02, self.btn_bu_3_04, self.btn_bu_3_05, self.btn_bu_3_06, self.btn_bu_3_07,
               self.btn_bu_3_08, self.btn_bu_3_08_01, self.btn_bu_3_10, self.btn_bu_3_10_01, self.btn_bu_3_12,
               self.btn_bu_3_12_01, self.btn_bu_3_12_02, self.btn_bu_3_12_03, self.btn_bu_4_01, self.btn_bu_4_02,
               self.btn_bu_4_02_01, self.btn_bu_4_02_02, self.btn_bu_4_03]
        for dev in lst:
            dev.clicked.connect(self.on_select)
        lst.append(self.btn_bu_back)
        self.set_lst(lst)

        self.btn_bu_back.clicked.connect(self.btn_back)

    @QtCore.pyqtSlot()
    def on_select(self):
        self.dev_type = self.sender().text()
        self.btn_ok.emit()
