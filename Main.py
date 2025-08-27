import logging
import sys

from PyQt5 import QtCore, QtWidgets

import exam_iu.exam_iu_dp
import exam_iu.exam_iu_pe
import menu.mainform
import opc.opc
from exam_bp.exam_bp import ExamBp
from exam_bu.bu_ai_tune import BuAiTune, BuRtTune
from exam_bu.bu_dp import TuneBuDp
from exam_bu.exam_bu_prog import Exam_bu
from exam_iu.exam_iu import ExamIU
from exam_iu.exam_iu_2 import ExamIU2

logging.basicConfig(filename='log\\log.txt', filemode='w', level=logging.INFO)

com = None


class Communicate(QtCore.QObject):
    success = QtCore.pyqtSignal()
    fail = QtCore.pyqtSignal()
    opc = None
    form = None
    exam_bu = None


class Main(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        global com
        com = Communicate()

        self.opc = opc.opc.Server()
        com.opc = self.opc

        self.form = menu.mainform.MainForm(self.opc)
        com.form = self.form
        self.form.closeEvent = self.closeEvent
        self.form.mnu_main.btnQuit.clicked.connect(self.form.close)
        self.form.showMaximized()

        self.stm = QtCore.QStateMachine()

        self.init_menu = InitMenu(self.stm)
        self.menu_main = MenuMain(self.stm)
        self.menu_iu = MenuIU(self.stm)
        self.iu_pe_select = IuPeSelect(self.stm)
        self.iu_pe = exam_iu.exam_iu_pe.ExamIuPe(self.stm, self.opc, self.form)
        self.iu_dp_select = IuPeSelect(self.stm)
        self.iu_dp = exam_iu.exam_iu_dp.ExamIUDP(self.stm, self.opc, self.form)
        self.iu_auth = IuAuth(self.stm)
        self.iu_select = IuSelect(self.stm)
        self.exam_iu_old = ExamIU(self.stm, self.opc, self.form)
        self.exam_iu = ExamIU2(self.stm, self.opc, self.form)

        self.menu_bu = MenuBU(self.stm)
        self.bu_auth = BuAuth(self.stm)
        self.bu_select = BuSelect(self.stm)
        self.reset_check_bu = ResetCheckBu(self.stm)
        self.check_bu = CheckBU(self.stm)

        self.exam_bu = Exam_bu(self.stm, self.opc, self.form)
        com.exam_bu = self.exam_bu
        self.bu_ai_tune = BuAiTune(self.stm, self.opc, self.form)
        self.bu_select_2 = BuSelect(self.stm)
        self.bu_rt_tune = BuRtTune(self.stm)
        self.disconnect_bu = self.exam_bu.disconnect_bu

        self.bu_prepare = BuPrepare(self.stm)
        self.bu_prepare_r = BuPrepareR(self.stm)
        self.bu_di = BuDi(self.stm)
        self.bu_di_r = BuDiR(self.stm)
        self.bu_ai = BuAi(self.stm)
        self.bu_fi = BuFi(self.stm)
        self.bu_fi_r = BuFiR(self.stm)
        self.bu_rt = BuRt(self.stm)
        self.bu_shim = BuShim(self.stm)
        self.bu_shim_r = BuShimR(self.stm)
        self.bu_protocol = self.exam_bu.protocol

        self.exam_bp = ExamBp(self.stm, self.opc, self.form)

        self.state_close = QtCore.QFinalState(self.stm)

        self.stm.setInitialState(self.init_menu)

        self.init_menu.addTransition(self.init_menu.success, self.menu_main)
        self.menu_main.addTransition(self.form.mnu_main.btnIU.clicked, self.iu_auth)
        self.menu_main.addTransition(self.form.mnu_main.btnIUTune.clicked, self.menu_iu)
        self.menu_iu.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_main)
        self.menu_iu.addTransition(self.form.mnu_iu.btn_iu_pe_tune.clicked, self.iu_pe_select)
        self.iu_pe_select.addTransition(self.form.select_iu.btn_ok, self.iu_pe)
        self.iu_pe_select.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_iu)
        self.menu_iu.addTransition(self.form.mnu_iu.btn_iu_dp_tune.clicked, self.iu_dp_select)
        self.iu_dp_select.addTransition(self.form.select_iu.btn_ok, self.iu_dp)
        self.iu_dp_select.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_iu)
        self.iu_pe.addTransition(self.iu_pe.finished, self.menu_iu)
        self.iu_dp.addTransition(self.iu_dp.finished, self.menu_iu)
        self.iu_auth.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_main)
        self.iu_auth.addTransition(self.form.auth.btn_ok, self.iu_select)
        self.iu_select.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_main)
        self.iu_select.addTransition(self.form.select_iu.btn_ok, self.exam_iu)
        self.exam_iu.addTransition(self.exam_iu.finished, self.menu_main)

        self.menu_main.addTransition(self.form.mnu_main.btnBUTune.clicked, self.menu_bu)
        self.menu_bu.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_main)
        self.menu_main.addTransition(self.form.mnu_main.btnBU.clicked, self.bu_auth)
        self.bu_auth.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_main)
        self.bu_auth.addTransition(self.form.auth.btn_ok, self.bu_select)
        self.bu_select.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_main)
        self.bu_select.addTransition(self.form.select_bu.btn_ok, self.reset_check_bu)
        self.reset_check_bu.addTransition(self.check_bu)
        self.check_bu.addTransition(self.form.btnPanel.btnBack.clicked, self.disconnect_bu)
        self.disconnect_bu.addTransition(self.menu_main)
        self.exam_bu.addTransition(self.exam_bu.finished, self.check_bu)

        self.check_bu.addTransition(self.form.check_bu.btn_prepare.clicked, self.bu_prepare)
        self.bu_prepare.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_prepare_r.clicked, self.bu_prepare_r)
        self.bu_prepare_r.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_di.clicked, self.bu_di)
        self.bu_di.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_di_r.clicked, self.bu_di_r)
        self.bu_di_r.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_ai.clicked, self.bu_ai)
        self.bu_ai.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_fi.clicked, self.bu_fi)
        self.bu_fi.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_fi_r.clicked, self.bu_fi_r)
        self.bu_fi_r.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_rt.clicked, self.bu_rt)
        self.bu_rt.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_shim.clicked, self.bu_shim)
        self.bu_shim.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_shim_r.clicked, self.bu_shim_r)
        self.bu_shim_r.addTransition(self.exam_bu)
        self.check_bu.addTransition(self.form.check_bu.btn_protocol.clicked, self.bu_protocol)
        self.bu_protocol.addTransition(self.form.btnPanel.btnOk.clicked, self.disconnect_bu)
        self.bu_protocol.addTransition(self.form.btnPanel.btnBack.clicked, self.disconnect_bu)

        self.menu_bu.addTransition(self.form.mnu_bu.btn_bu_ai_tune.clicked, self.bu_select_2)
        self.bu_select_2.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_bu)
        self.bu_select_2.addTransition(self.form.select_bu.btn_ok, self.bu_ai_tune)
        self.bu_ai_tune.addTransition(self.bu_ai_tune.finished, self.menu_bu)

        self.menu_bu.addTransition(self.form.mnu_bu.btn_bu_ai_3_tune.clicked, self.bu_rt_tune)
        self.bu_rt_tune.addTransition(self.bu_rt_tune.finished, self.menu_bu)

        self.menu_main.addTransition(self.form.mnu_main.btnBP.clicked, self.exam_bp)
        self.exam_bp.addTransition(self.exam_bp.finished, self.menu_main)

        self.bu_dp_select_iu = IuSelect(self.stm)
        self.bu_dp_select_bu = BuSelect(self.stm)
        self.tune_bu_dp = TuneBuDp(self.stm, self.opc, self.form)

        self.menu_bu.addTransition(self.form.mnu_bu.btn_bu_dp.clicked, self.bu_dp_select_iu)
        self.bu_dp_select_iu.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_bu)
        self.bu_dp_select_iu.addTransition(self.form.select_iu.btn_ok, self.bu_dp_select_bu)
        self.bu_dp_select_bu.addTransition(self.form.btnPanel.btnBack.clicked, self.menu_bu)
        self.bu_dp_select_bu.addTransition(self.form.select_bu.btn_ok, self.tune_bu_dp)
        self.tune_bu_dp.addTransition(self.tune_bu_dp.finished, self.menu_bu)

        self.opc.started.connect(self.stm.start)
        self.opc.start()

    def closeEvent(self, QEvent):
        self.form.hide()
        main.stm.stop()
        self.opc.stop()
        QEvent.accept()


class InitMenu(QtCore.QState):
    success = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        global com
        print('stm started')
        com.opc.ai.setActive(True)
        com.opc.di.setActive(True)
        com.opc.ao.setActive(False)
        com.opc.do1.setActive(False)
        com.opc.do1.setActive(False)
        com.opc.pv1.setActive(False)
        com.opc.pv2.setActive(False)
        com.opc.pa1.setActive(False)
        com.opc.pa2.setActive(False)
        com.opc.pa3.setActive(False)

        com.form.mnu_main.reset()
        com.form.mnu_iu.reset()
        self.success.emit()


class MenuMain(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.mnu_main


class MenuIU(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.mnu_iu
        com.form.mnu_iu.reset()


class MenuBU(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.mnu_bu
        com.form.mnu_bu.reset()


class IuPeSelect(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.select_iu
        com.form.currentmenu.reset()


class ExamIUDPSelect(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.select_iu
        com.form.currentmenu.reset()


class IuAuth(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.auth
        com.form.currentmenu.reset()


class BuAuth(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.auth
        com.form.currentmenu.reset()


class IuSelect(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.select_iu
        com.form.currentmenu.reset()


class BuSelect(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.select_bu
        # com.form.currentmenu.reset()


class ResetCheckBu(QtCore.QState):
    def onEntry(self, QEvent):
        com.form.check_bu.dev_type = com.form.select_bu.dev_type
        com.exam_bu.dev_type = com.form.select_bu.dev_type
        com.form.check_bu.reset()


class CheckBU(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.form.currentmenu = com.form.check_bu


class BuPrepare(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.prepare1)


class BuPrepareR(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.prepare_r)


class BuDi(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.di_check)


class BuDiR(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.di_check_r)


class BuAi(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.ai_check)


class BuFi(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.fi_check)


class BuFiR(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.fi_check_r)


class BuRt(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.rt_check)


class BuShim(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.shim_check)


class BuShimR(QtCore.QState):
    def onEntry(self, QEvent):
        com.exam_bu.setInitialState(com.exam_bu.shim_check_r)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    print(com.form.size())
    res=app.exec_()
    logging.warning(res)
    sys.exit(res)
