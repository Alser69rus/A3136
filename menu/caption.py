from PyQt5 import QtWidgets, QtCore, QtGui


class Caption(QtWidgets.QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(parent)
        self.setFont(QtGui.QFont('Segoi Ui', 32))
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignHCenter)


