from PyQt5 import QtCore, QtWidgets, QtGui


class Graph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dp = []
        self.pe = []
        self.pa3 = []

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen_black = QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 1)
        pen_gray = QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.lightGray)), 1)
        painter.setPen(pen_black)

        painter.drawRect(0, 0, 750, 500)
        painter.translate(50, 450)
        painter.drawLine(0,10,0,-400)
        painter.drawLine(-10,0,625,0)
        for i in range(1,26):
            painter.setPen(pen_black)
            painter.drawLine(25*i,-5,25*i,5)
            if not i%2:
                painter.drawText(i*25-10, 10, 20, 20, QtCore.Qt.AlignCenter, '{:.1f}'.format(i/10))
            painter.setPen(pen_gray)
            painter.drawLine(25 * i, -5, 25 * i, -400)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Graph()
    win.resize(1000, 700)
    win.show()
    app.exec_()
