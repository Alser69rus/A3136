from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot, QSettings

import menu.btnPanel as btnPanel
import menu.mnuMain as mnumain
from menu.auth import Auth
from menu.mnuSelectIU import SelectIU
import menu.mnuIU as mnuiu
import exam_iu.frm_iu
from menu.mnuBU import MnuBU
from menu.mnuSelectBU import SelectBU
from menu.mnuBUCheck import CheckBU


class MainForm(QtWidgets.QWidget):
    br3_changed = QtCore.pyqtSignal(float)

    def __init__(self, server=None, parent=None):
        super().__init__(parent)
        self.opc = server

        self.vbox = QtWidgets.QVBoxLayout()
        self.setWindowTitle('А3136. Стенд проверки и регулировки ЭРЧМ')
        self.resize(1024, 768)

        self.table = QtWidgets.QWidget()
        self.btnPanel = btnPanel.BtnPanel()
        self.statusbar = QtWidgets.QStatusBar()
        self.btnPanel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.statusbar.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.opc.error.connect(self.statusbar.showMessage)
        self.opc.warning.connect(self.on_warning)
        self.vbox.addWidget(self.table)
        self.vbox.addWidget(self.btnPanel)
        self.vbox.addWidget(self.statusbar)
        self.setLayout(self.vbox)

        self.mnu_main = mnumain.MainMenu()
        self.mnu_iu = mnuiu.mnuIU()
        self.mnu_iu.btn_iu_back.clicked.connect(self.btnPanel.btnBack.clicked)
        self.mnu_bu = MnuBU()
        self.mnu_bu.btn_bu_back.clicked.connect(self.btnPanel.btnBack.clicked)
        self.auth = Auth()
        self.auth.btn_back.connect(self.btnPanel.btnBack.clicked)
        self.select_iu = SelectIU()
        self.select_iu.btn_back.connect(self.btnPanel.btnBack.clicked)
        self.select_bu = SelectBU()
        self.select_bu.btn_bu_back.clicked.connect(self.btnPanel.btnBack.clicked)
        self.check_bu = CheckBU()

        self.exam_iu_pe_set_pe = exam_iu.frm_iu.Form_iu_set_pe()
        self.exam_iu_pe_set_dp = exam_iu.frm_iu.Form_iu_set_dp()
        self.exam_iu_pe_inst1 = exam_iu.frm_iu.Form_iu_inst1()
        self.exam_iu_pe_inst2 = exam_iu.frm_iu.Form_iu_inst2()
        self.exam_iu_pe_inst3 = exam_iu.frm_iu.Form_iu_inst3()
        self.exam_iu_pe_inst4 = exam_iu.frm_iu.Form_iu_inst4()
        self.exam_iu_pe_check = exam_iu.frm_iu.Form_iu_pe_check()
        self.exam_iu_dp_check = exam_iu.frm_iu.Form_iu_dp_check()
        self.exam_iu_pressure = exam_iu.frm_iu.FormIUPressureCheck()
        self.frm_print = exam_iu.frm_iu.FormPrint()

        self.stl = QtWidgets.QStackedLayout()
        self.stl.addWidget(self.auth)
        self.stl.addWidget(self.select_iu)
        self.stl.addWidget(self.mnu_main)
        self.stl.addWidget(self.mnu_iu)
        self.stl.addWidget(self.exam_iu_pe_set_pe)
        self.stl.addWidget(self.exam_iu_pe_set_dp)
        self.stl.addWidget(self.exam_iu_pe_inst1)
        self.stl.addWidget(self.exam_iu_pe_inst2)
        self.stl.addWidget(self.exam_iu_pe_inst3)
        self.stl.addWidget(self.exam_iu_pe_inst4)
        self.stl.addWidget(self.exam_iu_pe_check)
        self.stl.addWidget(self.exam_iu_dp_check)
        self.stl.addWidget(self.exam_iu_pressure)
        self.stl.addWidget(self.mnu_bu)
        self.stl.addWidget(self.select_bu)
        self.stl.addWidget(self.check_bu)

        self.stl.addWidget(self.frm_print)

        self.table.setLayout(self.stl)
        self._currentmenu = None
        self.br3 = self.opc.freq.value[2]

        self.button: dict = self.read_button_code()
        self.opc.di.changed.connect(self.on_di_change, QtCore.Qt.QueuedConnection)
        self.opc.freq.changed.connect(self.on_freq_change, QtCore.Qt.QueuedConnection)

    @pyqtSlot(str)
    def on_statusbar_update(self, msg):
        self.statusbar.showMessage(msg)

    @property
    def currentmenu(self):
        return self._currentmenu

    @currentmenu.setter
    def currentmenu(self, value):
        if self.currentmenu:
            self.disconnectmenu()
        self._currentmenu = value
        self.stl.setCurrentWidget(value)
        self._currentmenu.encoder_value = self.opc.freq.value[2]
        self.connectmenu()

    def connectmenu(self):
        self.currentmenu.encoder_value = self.br3
        self.br3_changed.connect(self.currentmenu.on_encoder, QtCore.Qt.QueuedConnection)
        self.btnPanel.btnUp.clicked.connect(self.currentmenu.on_btn_up_clicked)
        self.btnPanel.btnDown.clicked.connect(self.currentmenu.on_btn_down_clicked)
        self.btnPanel.btnBack.clicked.connect(self.currentmenu.on_btn_back_clicked)
        self.btnPanel.btnOk.clicked.connect(self.currentmenu.on_btn_ok_clicked)
        self.btnPanel.btnNo.clicked.connect(self.currentmenu.on_btn_no_clicked)

    def disconnectmenu(self):
        self.btnPanel.btnUp.clicked.disconnect(self.currentmenu.on_btn_up_clicked)
        self.btnPanel.btnDown.clicked.disconnect(self.currentmenu.on_btn_down_clicked)
        self.btnPanel.btnBack.clicked.disconnect(self.currentmenu.on_btn_back_clicked)
        self.btnPanel.btnOk.clicked.disconnect(self.currentmenu.on_btn_ok_clicked)
        self.btnPanel.btnNo.clicked.disconnect(self.currentmenu.on_btn_no_clicked)
        self.br3_changed.disconnect()

    @QtCore.pyqtSlot()
    def on_freq_change(self):
        br3 = self.opc.freq.value[2]
        if self.br3 != br3:
            self.br3 = br3
            self.br3_changed.emit(br3)

    @QtCore.pyqtSlot()
    def on_di_change(self):
        if self.opc.di.value[self.button['back']]:
            self.btnPanel.on_back_clicked()
        if self.opc.di.value[self.button['up']]:
            self.btnPanel.on_up_clicked()
        if self.opc.di.value[self.button['down']]:
            self.btnPanel.on_down_clicked()
        if self.opc.di.value[self.button['yes']]:
            self.btnPanel.on_ok_clicked()
        if self.opc.di.value[self.button['no']]:
            self.btnPanel.on_no_clicked()

    @staticmethod
    def read_button_code() -> dict:
        settings = QSettings('settings.ini', QtCore.QSettings.IniFormat)
        settings.setIniCodec('UTF-8')
        buttons = {
            'no': int(settings.value('buttons/no', 4)),
            'yes': int(settings.value('buttons/yes', 5)),
            'up': int(settings.value('buttons/up', 6)),
            'down': int(settings.value('buttons/down', 7)),
            'back': int(settings.value('buttons/back', 15)),
        }

        return buttons

    def on_warning(self, msg):
        self.statusbar.showMessage(msg, 500)
