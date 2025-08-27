from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QState, pyqtSignal
from dataclasses import dataclass, field

com = None


def i_to_v(i: float) -> int:
    return round((i - 4) * 1000 / (20 - 4))


@dataclass
class BU:
    dev_type: str
    prepare: bool = False
    prepare_r: bool = False

    di_res: list = field(default_factory=list)
    di_min: int = 0
    di_max: int = 0
    di_reg: str = ''

    fi_res: str = ''
    fi_note: str = ''

    shim_res: str = ''
    shim_note: str = ''
    shim_graph: list = field(default_factory=list)
    shim_i1: float = 0
    shim_i2: float = 0
    shim_res1: str = ''
    shim_res2: str = ''
    shim_res3: str = ''

    ai_res: str = ''
    ai_note: str = ''
    ai_i11: float = 0
    ai_i12: float = 0
    ai_i21: float = 0
    ai_i22: float = 0


bu = BU('')


class Form(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.arr = []
        self.vbox = QtWidgets.QVBoxLayout()
        self.img_bu = QtGui.QPixmap('exam_bu\\bu.png')
        self.img_prog = QtGui.QPixmap('exam_bu\\prog.png')
        self.img_prog2 = QtGui.QPixmap('exam_bu\\prog2.png')
        self.img_xp1 = QtGui.QPixmap('exam_bu\\xp1.png')
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
        self.img.setPixmap(self.img_empty)
        self.text.setText(
            '<p>Установите блок управления (БУ) на кронштейн на боковой стенке пульта.</p>'
            '<p>Подключите шлейфы к разъемам "XP1", "XP2", "XP3" блока управления и разъемам "XS1 БУ ПИТ.", '
            '"XS2 БУ ДВХ", "XS3 БУ АВХ" пульта соответственно</p>')


class BuAiTune(QState):
    def __init__(self, parent=None, server=None, form=None):
        super().__init__(parent)
        global com
        com = self
        self.opc = server
        self.do1 = server.do1
        self.do2 = server.do2
        self.gen = server.gen
        self.pa3 = server.pa3
        self.ao = server.ao
        self.freq = server.freq
        self.frm_main = form
        self.frm = Form()
        self.img = self.frm.img
        self.text = self.frm.text
        self.frm_main.stl.addWidget(self.frm)
        self.btnBack = self.frm_main.btnPanel.btnBack.clicked
        self.btnOk = self.frm_main.btnPanel.btnOk.clicked
        self.btnUp = self.frm_main.btnPanel.btnUp.clicked
        self.btnDown = self.frm_main.btnPanel.btnDown.clicked

        self.error = Error(self)
        self.finish = Finish(self)
        self.prepare1 = Prepare1(self)
        self.prepare2 = Prepare2(self)
        self.prepare3 = Prepare3(self)
        self.prepare4 = Prepare4(self)
        self.switch_work = SwitchWork(self)
        self.connect_bu_di = ConnectBUDI(self)
        self.connect_bu = ConnectBU(self)
        self.select_chanel = SelectChanel(self)

        self.ai_0_4 = Ai04(self)
        self.ai_0_20 = Ai020(self)
        self.ai_1_4 = Ai14(self)
        self.ai_1_20 = Ai120(self)
        self.save = Save(self)

        self.addTransition(self.opc.error, self.error)
        self.error.addTransition(self.finish)
        self.back_transition = self.addTransition(self.btnBack, self.finish)

        self.prepare1.addTransition(self.btnOk, self.prepare2)
        self.prepare2.addTransition(self.btnOk, self.prepare3)
        self.prepare3.addTransition(self.btnOk, self.prepare4)
        self.prepare4.addTransition(self.btnOk, self.switch_work)
        self.switch_work.addTransition(self.btnOk, self.connect_bu_di)
        self.switch_work.addTransition(self.switch_work.success, self.connect_bu_di)
        self.connect_bu_di.addTransition(self.connect_bu)
        self.connect_bu.addTransition(self.select_chanel)
        self.select_chanel.addTransition(self.select_chanel.chanel_0, self.ai_0_4)
        self.select_chanel.addTransition(self.select_chanel.chanel_1, self.ai_1_4)
        self.ai_0_4.addTransition(self.btnOk, self.ai_0_20)
        self.ai_0_20.addTransition(self.btnOk, self.ai_1_4)
        self.ai_1_4.addTransition(self.btnOk, self.ai_1_20)
        self.ai_1_20.addTransition(self.btnOk, self.save)
        self.save.addTransition(self.btnOk, self.finish)

        self.setInitialState(self.prepare1)


class Error(QtCore.QState):
    def onEntry(self, e):
        print('bu_error')


class Finish(QtCore.QFinalState):
    def onEntry(self, e):
        global com
        print('bu_finish')
        # com.opc.ai.setActive(False)
        # com.opc.di.setActive(True)
        # com.opc.pv1.setActive(False)
        # com.opc.pv2.setActive(False)
        # com.opc.pa1.setActive(False)
        # com.opc.pa2.setActive(False)
        # com.opc.pa3.setActive(False)
        # com.opc.connect_bu_di_power(False)
        # com.opc.connect_bu_power(False)
        com.freq.setActive(True)
        com.frm_main.stl.setCurrentWidget(com.frm_main.check_bu)

        com.opc.do1.setValue([0] * 32)
        com.opc.do2.setValue([0] * 32)
        com.ao.setActive(False)
        com.do2.setActive(False)
        com.frm_main.connectmenu()
        com.opc.connect_bu_di_power(False)
        com.opc.connect_bu_power(False)

    # com.pchv.setActive(False)


class Prepare1(QtCore.QState):
    def onEntry(self, QEvent):
        global com, bu
        bu = BU(dev_type=com.frm_main.select_bu.dev_type)
        com.frm_main.disconnectmenu()
        com.frm_main.stl.setCurrentWidget(com.frm)
        com.img.setPixmap(com.frm.img_bu_prog)
        com.text.setText('<p>Установите блок управления (БУ) на кронштейн на боковой стенке пульта.</p>'
                         '<p>Подключите шлейфы к разъемам "XP1", "XP2", "XP3" блока управления и разъемам '
                         '"XS1 БУ ПИТ.", "XS2 БУ ДВХ", "XS3 БУ АВХ" пульта соответственно</p>'
                         '<p>Нажмите "ДА" для продолжения.</p>')


class Prepare2(QtCore.QState):
    def onEntry(self, QEvent):
        global com, bu
        com.img.setPixmap(com.frm.img_bu_prog)
        com.text.setText('<p>Подключите разъем привода "XS10 ИУ ПЭ" к разъему привода "XP8 НАГРУЗКА", '
                         'или к разъему поворотного электромагнита регулятора. '
                         '</p><p>Нажмите "ДА" для продолжения.</p>')


class Prepare3(QtCore.QState):
    def onEntry(self, QEvent):
        global com, bu
        com.img.setPixmap(com.frm.img_bu_prog)
        com.text.setText('<p>Подключите при помощи шлейфа разъем пульта "XS12 БП Х2"'
                         ' и разъем "ХР13 24 В"</p><p>Нажмите "ДА" для продолжения.</p>')


class Prepare4(QtCore.QState):
    def onEntry(self, QEvent):
        global com, bu
        com.img.setPixmap(com.frm.img_bu_prog)
        com.text.setText('<p>Снимите защитную крышку с разъема БУ "ОСНОВНАЯ РАБОТА" и подключите'
                         ' программатор</p><p>Нажмите "ДА" для продолжения.</p>')


class SwitchWork(QtCore.QState):
    success = pyqtSignal()

    def onEntry(self, QEvent):
        if bu.dev_type == 'ЭРЧМ30Т3-06':
            com.text.setText('<p>Переведите переключатель "РЕЗЕРВНАЯ РАБОТА" на БУ в положение '
                             '"ОТКЛ."</p><p>Для продолжения нажмите "ДА"</p>')
        else:
            self.success.emit()


class ConnectBUDI(QtCore.QState):
    def onEntry(self, QEvent):
        com.text.setText('Производится подключение питания дискретных входов БУ')

        if bu.dev_type in ['ЭРЧМ30Т3-06', 'ЭРЧМ30Т3-04', 'ЭРЧМ30Т3-07']:
            com.opc.connect_bu_di_power(True, 110)
        elif bu.dev_type in ['ЭРЧМ30Т3-12', 'ЭРЧМ30Т3-12-01', 'ЭРЧМ30Т3-12-02', 'ЭРЧМ30Т3-12-03']:
            com.opc.connect_bu_di_power(True, 110)
        elif bu.dev_type in ['ЭРЧМ30Т3-08', 'ЭРЧМ30Т3-08-01']:
            com.opc.connect_bu_di_power(True, 75)
        elif bu.dev_type in ['ЭРЧМ30Т3-02', 'ЭРЧМ30Т3-05', 'ЭРЧМ30Т3-10', 'ЭРЧМ30Т3-10-01']:
            com.opc.connect_bu_di_power(True, 110)
        elif bu.dev_type in ['ЭРЧМ30Т4-01']:
            com.opc.connect_bu_di_power(True, 75)
        elif bu.dev_type in ['ЭРЧМ30Т4-02']:
            com.opc.connect_bu_di_power(True, 24)
        elif bu.dev_type in ['ЭРЧМ30Т4-02-01', 'ЭРЧМ30Т4-02-01', ]:
            com.opc.connect_bu_di_power(True, 48)
        elif bu.dev_type in ['ЭРЧМ30Т4-03']:
            com.opc.connect_bu_di_power(True, 75)
        else:
            com.opc.connect_bu_di_power(False)
            print(f'Неизвестный тип {bu.dev_type}')


class ConnectBU(QtCore.QState):
    def onEntry(self, QEvent):
        com.text.setText('Производится подключение питания БУ')
        com.opc.connect_bu_power()


class SelectChanel(QtCore.QState):
    chanel_0 = pyqtSignal()
    chanel_1 = pyqtSignal()

    def onEntry(self, event):
        if bu.dev_type in ['ЭРЧМ30Т4-02-02']:
            self.chanel_1.emit()
        else:
            self.chanel_0.emit()


class Ai04(QtCore.QState):
    def onEntry(self, QEvent):
        com.do2.setValue(1, 15)  # вкл пит. АО
        com.ao.setActive()
        com.do1.setActive()
        com.do2.setActive()
        v = i_to_v(4)
        com.ao.setValue([v, v] + com.ao.value[2:])
        com.img.setPixmap(com.frm.img_prog2)
        com.text.setText('<p>Установите на программаторе режим <b><font color="blue">PE9A</font></b>, '
                         'для этого зажав кнопку 1 или 2 '
                         'кнопками 5 и 6 установите требуемое значение режима.</p>'
                         '<p>Отпустив кнопки 1 и 2, кнопками 5 и 6 установите <b><font color="green">равным значение '
                         'нижнего и верхнего ряда</font></b> индикаторов.</p>'
                         '<p><br>Нажмите "ДА" для продолжения</p>')


class Ai020(QtCore.QState):
    def onEntry(self, QEvent):
        v = i_to_v(19.5)
        com.ao.setValue([v, v] + com.ao.value[2:])
        com.text.setText('<p>Установите на программаторе режим <b><font color="blue">PE9B</font></b>,'
                         ' для этого зажав кнопку 1 или 2 '
                         'кнопками 5 и 6 установите требуемое значение режима.</p>'
                         '<p>Отпустив кнопки 1 и 2, кнопками 5 и 6 установите значение верхнего ряда '
                         'индикаторов в диапазоне <b><font color="green">2,400-2,430</font></b>.</p>'
                         '<p><br>Нажмите "ДА" для продолжения</p>')


class Ai14(QtCore.QState):
    def onEntry(self, QEvent):
        v = i_to_v(4)
        com.ao.setValue([v, v] + com.ao.value[2:])
        com.text.setText('<p>Установите на программаторе режим <b><font color="blue">PEC2</font></b>, для этого зажав '
                         'кнопку 1 или 2 '
                         'кнопками 5 и 6 установите требуемое значение режима.</p>'
                         '<p>Отпустив кнопки 1 и 2, кнопками 5 и 6 установите <b><font color="green">равным значение '
                         'нижнего и верхнего ряда</font></b> индикаторов.</p>'
                         '<p><br>Нажмите "ДА" для продолжения</p>')


class Ai120(QtCore.QState):
    def onEntry(self, QEvent):
        v = i_to_v(19.5)
        com.ao.setValue([v, v] + com.ao.value[2:])
        com.text.setText('<p>Установите на программаторе режим <b><font color="blue">PEC0</font></b>,'
                         ' для этого зажав кнопку 1 или 2 '
                         'кнопками 5 и 6 установите требуемое значение режима.</p>'
                         '<p>Отпустив кнопки 1 и 2, кнопками 5 и 6 установите значение верхнего ряда '
                         'индикаторов в диапазоне <b><font color="green">15,44-15,56</font></b>.</p>'
                         '<p><br>Нажмите "ДА" для продолжения</p>')


class Save(QtCore.QState):
    def onEntry(self, QEvent):
        com.ao.setValue([0, 0] + com.ao.value[2:])

        com.text.setText('<p>Установите на программаторе режим <b><font color="blue">PEF0</font></b>,'
                         ' для этого зажав кнопку 1 или 2 '
                         'кнопками 5 и 6 установите требуемое значение режима.</p>'
                         '<p>После чего нажать и удерживать кнопку 3</p>'
                         '<p>После чего кратковременно нажать и отпустить кнопку 6</p>'
                         '<p>Дождавшись записи значений в память блока управления через 2-3 с, отпустите кнопку 3</p>'
                         '<p><br>Нажмите "ДА" для продолжения</p>')


class BuRtTune(QState):
    def __init__(self, parent=None):
        super().__init__(parent)
        global com
        self.error = Error(self)
        self.finish = Finish(self)
        self.prepare1 = Prepare1(self)
        self.prepare2 = Prepare2(self)
        self.prepare3 = Prepare3(self)
        self.prepare4 = Prepare4(self)
        self.switch_work = SwitchWork(self)
        self.connect_bu_di = ConnectBUDI(self)
        self.connect_bu = ConnectBU(self)

        self.addTransition(com.opc.error, self.error)
        self.error.addTransition(self.finish)
        self.back_transition = self.addTransition(com.btnBack, self.finish)

        self.prepare1.addTransition(com.btnOk, self.prepare2)
        self.prepare2.addTransition(com.btnOk, self.prepare3)
        self.prepare3.addTransition(com.btnOk, self.prepare4)

        self.ai_3_min = AI3Min(self)
        self.ai_3_max = AI3Max(self)
        self.ai_3_save = Save(self)

        self.prepare4.addTransition(com.btnOk, self.ai_3_min)
        self.ai_3_min.addTransition(com.btnOk, self.ai_3_max)
        self.ai_3_max.addTransition(com.btnOk, self.ai_3_save)
        self.ai_3_save.addTransition(com.btnOk, self.finish)

        self.setInitialState(self.prepare1)


class AI3Min(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.opc.connect_bu_power()
        com.opc.connect_bu_di_power(True, 110)
        com.do2.setValue(True, 31)
        com.img.setPixmap(com.frm.img_prog2)
        com.text.setText(f'<p>Для настройки канала АВХ3 - датчика температуры установите на программаторе режим '
                         f'<b><font color="blue">"PEC8"</font></b>. Для этого '
                         'удерживая кнопку 1 или 2 программатора кнопками 5 и 6 установите требуемое '
                         'значение режима.</p>'
                         f'<p>Кнопками 5 и 6 установите показания нижнего ряда индикаторов равным '
                         f'<b><font color="green">0000</font></b>. После чего нажмите кнопку 4.</p>'
                         '<p><br>Нажмите "ДА" для продолжения.</p>'
                         )


class AI3Max(QtCore.QState):
    def onEntry(self, QEvent):
        com.do2.setValue(False, 31)
        com.do2.setValue(True, 30)
        com.text.setText(f'<p>Установите на программаторе режим '
                         f'<b><font color="blue">"PEC9"</font></b>. Для этого '
                         'удерживая кнопку 1 или 2 программатора кнопками 5 и 6 установите требуемое '
                         'значение режима.</p>'
                         f'<p>Кнопками 5 и 6 установите показания нижнего ряда индикаторов равным '
                         f'<b><font color="green">0100</font></b>. После чего нажмите кнопку 4.</p>'
                         '<p><br>Нажмите "ДА" для продолжения.</p>'
                         )
