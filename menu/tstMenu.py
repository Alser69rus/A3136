from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
import unittest

import menu.btn as btn
import menu.caption as caption
import menu.template as template
import menu.mnuMain as mnuMain
import menu.mnuIU as mnuUI
import menu.btnPanel as btnPanel
import menu.mainform as mainform


@unittest.skip
class TestBtn(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = QtWidgets.QWidget()
        win.resize(300, 200)
        win.setWindowTitle('button')
        win.l = QtWidgets.QVBoxLayout()
        win.b1 = btn.Btn('Кнопка1')
        win.b2 = btn.Btn('Кнопка 2')
        win.b3 = btn.Btn('Кнопка 3')
        win.b1.state = 'normal'
        win.b2.state = 'ok'
        win.b3.state = 'fail'
        win.b3.selected = True
        win.l.addWidget(win.b1)
        win.l.addWidget(win.b2)
        win.l.addWidget(win.b3)
        win.setLayout(win.l)
        win.show()
        self.assertEqual(app.exec_(), 0)


@unittest.skip
class TestCaption(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = QtWidgets.QWidget()
        win.resize(300, 200)
        win.setWindowTitle('caption')
        win.vbox = QtWidgets.QVBoxLayout()
        win.caption = caption.Caption('Меню')
        win.vbox.addWidget(win.caption)
        win.vbox.addStretch()
        win.setLayout(win.vbox)
        win.show()
        app.exec_()


@unittest.skip
class TestMenu(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = template.Menu('меню')
        win.b1 = btn.Btn('Кнопка1')
        win.b2 = btn.Btn('Кнопка2')
        win.resize(640, 480)
        win.setWindowTitle('win')
        win.set_lst([win.b1, win.b2])
        win.reset()
        win.show()
        app.exec_()


@unittest.skip
class TestMainMenu(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = mnuMain.MainMenu()
        win.setWindowTitle('Главное меню')
        win.btnQuit.clicked.connect(win.close)
        win.show()
        app.exec_()


@unittest.skip
class TestUIMenu(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = mnuUI.mnuUI()
        win.setWindowTitle('меню ИУ')
        win.show()
        app.exec_()


@unittest.skip
class TestBtnPanel(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = btnPanel.BtnPanel()
        win.show()
        app.exec_()


# @unittest.skip
class TestMainForm(unittest.TestCase):
    def test_1(self):
        app = QtWidgets.QApplication([])
        win = mainform.MainForm()
        win.resize(1024, 700)
        win.show()
        win.stl.setCurrentWidget(win.exam_iu_pe_inst3)
        # win.btnPanel.btnUp.clicked.connect(win.mnu_main.on_btn_up_clicked)
        # win.btnPanel.btnDown.clicked.connect(win.mnu_main.on_btn_down_clicked)
        # win.btnPanel.btnOk.clicked.connect(win.mnu_main.on_btn_ok_clicked)
        # win.btnPanel.btnBack.clicked.connect(win.mnu_main.on_btn_back_clicked)

        # win.mnu_main.btnQuit.clicked.connect(win.close)
        print(win.width(), win.height())
        app.exec_()
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
