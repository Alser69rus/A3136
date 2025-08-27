from PyQt5 import QtWidgets, QtCore, QtGui

com = None
btnBack = None
btnOk = None
do1 = None
pv1 = None
pa1 = None
power = 20
u_ref = 21
r_stock = 22
r_load = 23
opc = None
frm = None
frm_main = None
text = None
img = None
msg = ''
msg2 = ''
u1 = 0
u2 = 0
count = 0
val = 0


class Form(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.img_bu = QtGui.QPixmap('exam_bu\\bu.png')
        self.img_prog = QtGui.QPixmap('exam_bu\\prog.png')
        self.img_prog2 = QtGui.QPixmap('exam_bu\\prog2.png')
        self.img_xp1 = QtGui.QPixmap('exam_bu\\xp1.jpg')
        self.img_bu_prog = QtGui.QPixmap('exam_bu\\bu-prog.png')
        self.img_empty = QtGui.QPixmap('exam_bu\\empty.png')
        self.img = QtWidgets.QLabel()

        self.text = QtWidgets.QLabel()
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.img)
        self.vbox.addWidget(self.text)
        self.vbox.addStretch(1)
        # self.img.setPixmap(self.img_empty)


class ExamBp(QtCore.QState):

    def __init__(self, parent=None, server=None, form=None):
        super().__init__(parent)
        global com, btnOk, btnBack, pv1, pa1, do1, opc, frm, frm_main, text, img
        com = self
        opc = server
        do1 = server.do1
        pv1 = opc.pv1
        pv1.setActive(True)
        pa1 = opc.pa1
        pa1.setActive()
        frm_main = form
        frm = Form()
        frm_main.stl.addWidget(frm)

        btnBack = frm_main.btnPanel.btnBack.clicked
        btnOk = frm_main.btnPanel.btnOk.clicked
        img = frm.img
        text = frm.text

        self.error = Error(self)
        self.finish = Finish(self)

        self.prepare = Prepare(self)
        self.config_power = ConfigPower(self)
        self.power_on = PowerOn(self)
        self.measure_u1 = MeasureU(self)
        self.check_u1 = CheckU1(self)
        self.connect_load = ConnectLoad(self)
        self.measure_u2 = MeasureU(self)
        self.check_u2 = CheckU2(self)
        self.power_off = PowerOff(self)
        self.result = Result(self)

        self.setInitialState(self.prepare)

        self.addTransition(opc.error, self.error)
        self.error.addTransition(self.finish)
        self.addTransition(btnBack, self.finish)

        self.prepare.addTransition(btnOk, self.config_power)
        self.config_power.addTransition(do1.updated, self.power_on)
        self.power_on.addTransition(do1.updated, self.measure_u1)
        self.measure_u1.addTransition(pv1.updated, self.measure_u1)
        self.measure_u1.addTransition(self.measure_u1.done, self.check_u1)
        self.check_u1.addTransition(self.connect_load)
        self.connect_load.addTransition(do1.updated, self.measure_u2)
        self.measure_u2.addTransition(pv1.updated, self.measure_u2)
        self.measure_u2.addTransition(self.measure_u2.done, self.check_u2)
        self.check_u2.addTransition(self.power_off)
        self.power_off.addTransition(do1.updated, self.result)
        self.result.addTransition(btnOk, self.finish)


class Error(QtCore.QState):
    def onEntry(self, e):
        print('bp_error')


class Finish(QtCore.QFinalState):
    def onEntry(self, e):
        global com
        do1.setValue([0] * 32)
        pv1.setActive(False)
        pa1.setActive(False)
        frm_main.stl.setCurrentWidget(frm_main.mnu_main)
        frm_main.connectmenu()


class Prepare(QtCore.QState):
    def onEntry(self, QEvent):
        frm_main.disconnectmenu()
        frm_main.stl.setCurrentWidget(frm)
        # img.setPixmap(frm.img_empty)
        pv1.setActive(True)
        pa1.setActive(True)
        text.setText('<p>Установите блок питания на кронштейн на боковой части пульта управления.</p>'
                     '<p>Подключите при помощи шлейфа разъем "X1" блока питания и "XS11 БП Х1" пульта. '
                     'Подключите разъем "Х2" блока питания и "XS12 БП Х2" пульта управления.</p>'
                     '<p><br>Нажмите "ПРИНЯТЬ" для продолжения.</p>')


class ConfigPower(QtCore.QState):
    def onEntry(self, QEvent):
        do1.setValue(0, u_ref)
        do1.setValue(1, r_stock)
        text.setText('Входное напряжение 110 В ... ок\n'
                     'Отключение защитного сопротивления .... ок\n')


class PowerOn(QtCore.QState):
    def onEntry(self, QEvent):
        global msg, u1, u2, count, val
        do1.setValue(1, power)
        text.setText(text.text() +
                     'Подключение блока питания ... ок\n')
        msg = text.text()
        val = []
        count = 0
        u1 = 0
        u2 = 0


class MeasureU(QtCore.QState):
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        global msg, val, count

        count += 1

        if count < 30:
            val.append(pv1.value)
            val = val[-10:]
            text.setText(f'{msg}Напряжение блока питания  {sum(val)/len(val):5.2f} В ...{count/30:3.1%}\n')
        if count == 30:
            val = sum(val) / len(val)
            self.done.emit()


class CheckU1(QtCore.QState):
    def onEntry(self, QEvent):
        global u1, val, count
        if 23.5 <= val <= 24.5:
            text.setText(f'{msg}Напряжение блока питания  {val:5.2f} В ... норма\n')
        else:
            text.setText(f'{msg}Напряжение блока питания  {val:5.2f} В ... НЕ НОРМА\n')
        u1 = val


class ConnectLoad(QtCore.QState):
    def onEntry(self, QEvent):
        global msg, count, val
        do1.setValue(1, r_load)
        text.setText(text.text() + f'Подключение нагрузки ... ок\n')
        msg = text.text()
        val = []
        count = 0


class CheckU2(QtCore.QState):
    def onEntry(self, QEvent):
        global u2, val
        if 23.5 <= val <= 24.5 and pa1.value > 2:
            text.setText(f'{msg}Напряжение блока питания  {val:5.2f} В ... норма\n')
        else:
            text.setText(f'{msg}Напряжение блока питания  {val:5.2f} В ... НЕ НОРМА\n')
        u2 = val


class PowerOff(QtCore.QState):
    def onEntry(self, QEvent):
        do1.setValue([0] * 32)
        text.setText(text.text() + f'Отключение питания ... ок\n')


class Result(QtCore.QState):
    def onEntry(self, QEvent):
        res1 = 'норма' if 23.5 <= u1 <= 24.5 else 'НЕ НОРМА'
        res2 = 'норма' if 23.5 <= u2 <= 24.5 else 'НЕ НОРМА'
        res3 = 'норма' if 23.5 <= u1 <= 24.5 and 23.5 <= u2 <= 24.5 else 'НЕ НОРМА'

        text.setText(f'<p>Напряжение без нагрузки: {u1:5.2f} В ... {res1}<br>'
                     f'Напряжение под нагрузкой: {u2:5.2f} В ... {res2}</p>'
                     f'<p>Результат проверки: {res3}</p>')
