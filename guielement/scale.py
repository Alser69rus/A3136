from PyQt5 import QtWidgets, QtCore, QtGui


class Scale:
    """отрисовка шкал приборов x,y - центр шкалы, r-радиус до внутренней границе меток,
    startA, finishA - углы начала и окончания шкалы, startV и finishV - подписи начала и конца диапазона
    prim, sec,ter - количество главных, второстепенных и третичных штрихов, f_str - строка формоматирования подписей"""

    def __init__(self, x, y, r, startA=180, finishA=0, startV=0, finishV=1, prim=10, sec=2, ter=1, f_str='{}'):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.startA = startA
        self.startV = startV
        self.finishA = finishA
        self.finishV = finishV
        self.prim = prim
        self.linewidth = 1
        self.sec = sec
        self.ter = ter
        self.f_str = f_str

    def drawScale(self, painter: QtGui.QPainter):
        count = self.prim * self.sec * self.ter
        da = (self.finishA - self.startA) / count

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.translate(self.x, self.y)
        painter.rotate(-self.startA)

        for i in range(count + 1):
            if not i % (self.sec * self.ter):
                self.drawPrimary(painter)
            elif not i % (self.ter):
                self.drawSecondary(painter)
            else:
                self.drawTertiary(painter)

            painter.rotate(-da)
        painter.restore()

    def drawPrimary(self, painter: QtGui.QPainter):
        h = QtGui.QFontMetrics(painter.font()).height()
        pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), self.linewidth)
        pen2 = QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 3 * self.linewidth)
        painter.setPen(pen)
        painter.drawLine(self.r, 0, self.r + h, 0)
        painter.setPen(pen2)
        painter.drawLine(self.r + h * 0.67, 0, self.r + h, 0)

    def drawSecondary(self, painter: QtGui.QPainter):
        h = QtGui.QFontMetrics(painter.font()).height()
        pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), self.linewidth)
        painter.setPen(pen)
        painter.drawLine(self.r, 0, self.r + h * 0.67, 0)

    def drawTertiary(self, painter: QtGui.QPainter):
        h = QtGui.QFontMetrics(painter.font()).height()
        pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), self.linewidth)
        painter.setPen(pen)
        painter.drawLine(self.r, 0, self.r + h * 0.33, 0)

    def drawVal(self, painter: QtGui.QPainter):
        count = self.prim
        da = (self.finishA - self.startA) / count
        dv = (self.finishV - self.startV) / count
        w = QtGui.QFontMetrics(painter.font()).width(self.f_str.format(self.finishV))
        for i in range(count + 1):
            v = self.startV + i * dv
            w = max(w, QtGui.QFontMetrics(painter.font()).width(self.f_str.format(v)))

        h = QtGui.QFontMetrics(painter.font()).height()

        for i in range(count + 1):
            painter.save()
            painter.translate(self.x, self.y)
            a = -self.startA - da * i
            painter.rotate(a)
            v = self.startV + i * dv
            l = self.r + self.linewidth + h + 4 + w / 2
            painter.translate(l, 0)
            painter.rotate(-a)
            painter.drawText(-w / 2, -h / 2, w, h, QtCore.Qt.AlignCenter, self.f_str.format(v))
            painter.restore()


class Arrow:
    """отрисовка стрелки x,y - центр, r-радиус, l-длина видимой части, w- ширина"""

    def __init__(self, x, y, r, l, w=4):
        self.x = x
        self.y = y
        self.r = r
        self.l = l
        self.w = w

    def drawArrow(self, painter: QtGui.QPainter, angle):
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.x, self.y)
        painter.rotate(-angle)
        painter.drawPolygon(QtCore.QPointF(self.r - self.l, self.w), QtCore.QPointF(self.r, 0),
                            QtCore.QPointF(self.r - self.l, -self.w))
        if self.r == self.l:
            painter.drawEllipse(-self.w, -self.w, self.w * 2, self.w * 2)

        painter.restore()


class ScaledDevice(QtWidgets.QWidget):
    def __init__(self, width, height, arr_x, arr_y, arr_r, min_a=0, max_a=180, min_v=0, max_v=10, mark_prim=10,
                 mark_sec=2, mark_ter=1, f_mark='{}', f_text='{}', arr_length=0, arrow_width=4, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.caption = QtWidgets.QLabel()
        self.caption.setFont(QtGui.QFont('Segoi UI', 20))
        self.text = QtWidgets.QLabel()
        self.vbox.addWidget(self.caption)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.text)
        self.setLayout(self.vbox)
        self.text.setFont(QtGui.QFont('Segoi UI', 24))
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.scale = Scale(arr_x, arr_y, arr_r, min_a, max_a, min_v, max_v, mark_prim, mark_sec, mark_ter, f_mark)
        if arr_length == 0:
            arr_length = arr_r - 2
        self.arrow = Arrow(arr_x, arr_y, arr_r - 2, arr_length, arrow_width)
        self.arrow_green = Arrow(arr_x, arr_y, arr_r - 2, 20, arrow_width)
        self.red_pen = QtGui.QPen(QtCore.Qt.red)
        self.red_brush = QtGui.QBrush(QtCore.Qt.red)
        self.green_pen = QtGui.QPen(QtCore.Qt.green)
        self.green_brush = QtGui.QBrush(QtCore.Qt.transparent)
        self.setFont(QtGui.QFont('Segoi UI', 16))

        self.task_value = min_v
        self.value = min_v
        self.angle = min_a
        self.task_angle = min_a
        self.min_a = min_a
        self.max_a = max_a
        self.min_v = min_v
        self.max_v = max_v
        self.red_visible = True
        self.green_visible = True
        self.f_text = f_text

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.resize(width, height)
        self.setMinimumSize(width, height)
        self.alarm = False
        self.alarm_state = False

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 8, 8)
        self.scale.drawScale(painter)
        self.scale.drawVal(painter)
        if self.green_visible:
            painter.setPen(self.green_pen)
            painter.setBrush(self.green_brush)
            self.arrow_green.drawArrow(painter, self.task_angle)
        if self.red_visible:
            painter.setPen(self.red_pen)
            painter.setBrush(self.red_brush)
            self.arrow.drawArrow(painter, self.angle)

        # if self.alarm:
        #     painter.setPen(self.red_pen)
        #     painter.setBrush(self.red_brush)
        #     painter.drawEllipse(self.width() - 30, 10, 20, 20)

    @QtCore.pyqtSlot(float)
    def setValue(self, value):

        self.alarm = not (self.min_v <= value <= self.max_v)
        v = value
        if v > self.max_v:
            v = self.max_v
        if v < self.min_v:
            v = self.min_v
        self.value = value

        self.angle = self.min_a - (self.min_a - self.max_a) * (v - self.min_v) / (self.max_v - self.min_v)
        self.text.setText(self.f_text.format(value))
        self.update()

    @QtCore.pyqtSlot(float)
    def setTask(self, value):
        self.alarm = not (self.min_v <= value <= self.max_v)
        v = value
        if v > self.max_v:
            v = self.max_v
        if v < self.min_v:
            v = self.min_v
        self.task_value = value
        self.task_angle = self.min_a - (self.min_a - self.max_a) * (v - self.min_v) / (self.max_v - self.min_v)
        self.update()

    def setArrowVisible(self, red=True, green=True):
        self.red_visible = red
        self.green_visible = green
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = ScaledDevice(width=280, height=320, arr_x=250, arr_y=250, arr_r=180, min_a=180, max_a=90, min_v=0, max_v=600,
                       mark_prim=6, mark_sec=2, mark_ter=5, f_mark='{:3.0f}', f_text='{:>3.0f} об/мин')
    win.caption.setText('Тахометр')
    win.setValue(100)
    win.setTask(200)

    win2 = ScaledDevice(width=380, height=320, arr_x=180, arr_y=155, arr_r=90, min_a=270, max_a=-22.5, min_v=0,
                        max_v=2.6,
                        mark_prim=13, mark_sec=2, mark_ter=5, f_mark='{: >.1f}', f_text='{:>5.3f} А')
    win2.caption.setText('PA3')
    win2.text.setAlignment(QtCore.Qt.AlignRight)
    win2.setValue(1.3)
    win2.setTask(1.8)
    win2.setArrowVisible(True, False)

    win3 = ScaledDevice(width=280, height=320, arr_x=130, arr_y=500, arr_r=350, arr_length=40, min_a=106, max_a=74,
                        min_v=0, max_v=10,
                        mark_prim=10, mark_sec=2, mark_ter=1, f_mark='{:.0f}', f_text='Позиция: {:>3.1f}')
    win3.caption.setText('Указатель\nсилового вала')
    win3.setValue(2)
    win3.setTask(8)

    win.show()
    win2.show()
    win3.show()
    app.exec_()
