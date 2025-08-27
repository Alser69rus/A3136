from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class BtnPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._stl = 'QPushButton{border:2px;border-radius:8px;border-color:black;text-align:center;padding: 4px;' + \
                    'background-color:rgba(10,10,10,10%);border-style:none;font:20px "Segoi UI";' + \
                    'min-width:80px;icon-size: 32px 32px}' + ' QPushButton:pressed{background-color:rgba(30,0,0,30%)}'

        self.setStyleSheet(self._stl)

        self.hbox = QtWidgets.QHBoxLayout()
        self.btnBack = QtWidgets.QPushButton('Назад')
        self.btnUp = QtWidgets.QPushButton('Вверх')
        self.btnDown = QtWidgets.QPushButton('Вниз')
        self.btnOk = QtWidgets.QPushButton('Да')
        self.btnNo = QtWidgets.QPushButton('Нет')
        self.btnBack.setIcon(QtGui.QIcon('menu\\back.png'))
        self.btnUp.setIcon(QtGui.QIcon('menu\\up.png'))
        self.btnDown.setIcon(QtGui.QIcon('menu\\down.png'))
        self.btnOk.setIcon(QtGui.QIcon('menu\\ok.png'))
        self.btnNo.setIcon(QtGui.QIcon('menu\\no.png'))

        self.hbox.addWidget(self.btnBack)
        self.hbox.addWidget(self.btnUp)
        self.hbox.addWidget(self.btnDown)
        self.hbox.addWidget(self.btnOk)
        self.hbox.addWidget(self.btnNo)

        self.setLayout(self.hbox)

    @pyqtSlot()
    def on_ok_clicked(self):
        if self.btnOk.isVisible():
            self.btnOk.animateClick()

    @pyqtSlot()
    def on_no_clicked(self):
        if self.btnNo.isVisible():
            self.btnNo.animateClick()

    @pyqtSlot()
    def on_back_clicked(self):
        if self.btnBack.isVisible():
            self.btnBack.animateClick()

    @pyqtSlot()
    def on_up_clicked(self):
        if self.btnUp.isVisible():
            self.btnUp.animateClick()

    @pyqtSlot()
    def on_down_clicked(self):
        if self.btnDown.isVisible():
            self.btnDown.animateClick()
