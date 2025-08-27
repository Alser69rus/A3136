from PyQt5 import QtCore, QtWidgets, QtPrintSupport, QtGui
import time, os
import datetime
from dataclasses import dataclass, field

com = None
opc = None
frm_main = None
frm = None
frm1 = None
iu = None
data = None
ti = None


@dataclass
class Data:
    speed_idx: int = 0
    note: str = ''
    pr: list = field(default_factory=list)
    arr: list = field(default_factory=list)
    arr_average: list = field(default_factory=list)
    count: int = 0
    count2: int = 0
    value: float = 0
    i: float = 0
    a: float = 0
    f: float = 0
    res: str = ''
    i2: float = 0
    i8: float = 0
    f1: float = 0
    f9: float = 0
    num: int = 0


class Form(QtWidgets.QWidget):
    GR_HEIGHT = 300
    GR_WIDTH = 800
    GR_MX = 200
    GR_MY = 25
    GR_OFX = 40
    GR_OFY = 20

    def __init__(self, parent=None):
        super().__init__(parent)
        self.arr = []
        self.vbox = QtWidgets.QVBoxLayout()
        self.img_empty = QtGui.QPixmap('exam_iu\\empty.png')

        self.img = QtWidgets.QLabel()

        self.text = QtWidgets.QLabel()
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.img)
        self.vbox.addWidget(self.text)
        self.vbox.addStretch(1)
        self.img.setPixmap(self.img_empty)
        self.text.setText('')

    def paintEvent(self, QPaintEvent):
        if self.arr:
            painter = QtGui.QPainter(self)
            QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 1)
            points = [QtCore.QPointF(self.GR_OFX + i[0] * self.GR_MX, self.GR_HEIGHT - self.GR_OFY - i[1] * self.GR_MY)
                      for i in self.arr]
            painter.drawLine(self.GR_OFX, self.GR_HEIGHT - self.GR_OFY + 5, self.GR_OFX, self.GR_OFY)
            painter.drawLine(self.GR_OFX - 5, self.GR_HEIGHT - self.GR_OFY, self.GR_WIDTH - self.GR_OFX,
                             self.GR_HEIGHT - self.GR_OFY)
            for x in range(0, self.GR_WIDTH - self.GR_OFX * 2, int(self.GR_MX / 5)):
                painter.drawLine(self.GR_OFX + x, self.GR_HEIGHT - self.GR_OFY + 5, self.GR_OFX + x,
                                 self.GR_HEIGHT - self.GR_OFY - 5)
                painter.drawText(self.GR_OFX + x - 5, self.GR_HEIGHT - 2, '{:3.1f}'.format(x / self.GR_MX))
            for y in range(1, 10):
                painter.drawLine(self.GR_OFX - 5, self.GR_HEIGHT - self.GR_OFY - y * self.GR_MY, self.GR_OFX + 5,
                                 self.GR_HEIGHT - self.GR_OFY - y * self.GR_MY)
                painter.drawText(10, self.GR_HEIGHT - self.GR_OFY - y * self.GR_MY + 7, '{:3.1f}'.format(y))
            painter.drawText(self.GR_OFX + 10, self.GR_OFY + 10, 'Поз. инд.')
            painter.drawText(self.GR_WIDTH - 30, self.GR_HEIGHT - 5, 'I, A')
            i1, a1, i2, a2 = 1.3, 2.0, 2.0, 8.0
            QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.green)), 1)
            painter.drawLine(self.GR_OFX + (i1 - 0.05) * self.GR_MX, self.GR_HEIGHT - self.GR_OFY - a1 * self.GR_MY,
                             self.GR_OFX + (i2 - 0.05) * self.GR_MX, self.GR_HEIGHT - self.GR_OFY - a2 * self.GR_MY)
            painter.drawLine(self.GR_OFX + (i1 + 0.05) * self.GR_MX, self.GR_HEIGHT - self.GR_OFY - a1 * self.GR_MY,
                             self.GR_OFX + (i2 + 0.05) * self.GR_MX, self.GR_HEIGHT - self.GR_OFY - a2 * self.GR_MY)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.red)), 2))
            painter.drawPolyline(*points)


class ExamIU2(QtCore.QState):
    def __init__(self, parent=None, server=None, form=None):
        super().__init__(parent)
        global opc, frm_main, frm, frm1, iu
        opc = server
        frm_main = form
        frm = Form()
        frm1 = form.exam_iu_pressure

        frm_main.stl.addWidget(frm)
        iu = frm_main.select_iu

        btnOk = frm_main.btnPanel.btnOk.clicked
        btnBack = frm_main.btnPanel.btnBack.clicked

        self.error = Error(self)
        self.stop_PCHV = StopPCHV(self)
        self.disconnect_devices = DisconnectDevices(self)
        self.finish = Finish(self)
        self.addTransition(opc.error, self.error)
        self.error.addTransition(self.stop_PCHV)
        self.addTransition(btnBack, self.stop_PCHV)
        self.stop_PCHV.addTransition(opc.pchv.break_on,self.disconnect_devices)
        self.disconnect_devices.addTransition(self.finish)

        self.install_0 = Install0(self)
        self.install_1 = Install1(self)
        self.install_2 = Install2(self)
        self.install_3 = Install3(self)
        self.install_4 = Install4(self)
        self.install_0.addTransition(self.install_1)
        self.install_1.addTransition(btnOk, self.install_2)
        self.install_2.addTransition(btnOk, self.install_3)
        self.install_3.addTransition(btnOk, self.install_4)
        self.setInitialState(self.install_0)

        # Прокачка
        self.connect_dev = ConnectDev(self)
        self.prepare = Prepare(self)
        self.wait_timer = WaitTimer(self)
        self.install_4.addTransition(btnOk, self.connect_dev)

        self.connect_dev.addTransition(self.prepare)
        self.prepare.addTransition(self.wait_timer)
        self.wait_timer.addTransition(opc.pchv.updated, self.wait_timer)

        # Замер давлений

        self.set_speed_pressure1 = SetSpeed(self)
        self.measure_p1 = MeasureP(self)
        self.set_speed_pressure2 = SetSpeed(self)
        self.measure_p2 = MeasureP(self)
        self.select_p3_i1 = SelectP3I1(self)
        self.stop_pchv1 = StopPCHV(self)
        self.connect_pchv_reverse = ConnectPchvReverse(self)
        self.set_speed_pressure3 = SetSpeed(self)
        self.measure_p3 = MeasureP(self)
        self.set_speed_pressure4 = SetSpeed(self)
        self.measure_p4 = MeasureP(self)
        self.stop_pchv2 = StopPCHV(self)
        self.connect_pchv2 = ConnectPchv(self)
        self.wait_timer.addTransition(self.wait_timer.done, self.set_speed_pressure1)
        self.set_speed_pressure1.addTransition(opc.pchv.speed_reached, self.measure_p1)
        self.measure_p1.addTransition(self.measure_p1.done, self.set_speed_pressure2)
        self.measure_p1.addTransition(opc.ai.updated, self.measure_p1)
        self.set_speed_pressure2.addTransition(opc.pchv.speed_reached, self.measure_p2)
        self.measure_p2.addTransition(opc.ai.updated, self.measure_p2)
        self.measure_p2.addTransition(self.measure_p2.done, self.select_p3_i1)

        self.select_p3_i1.addTransition(self.select_p3_i1.fail, self.stop_pchv1)
        self.stop_pchv1.addTransition(opc.pchv.break_on, self.connect_pchv_reverse)
        self.connect_pchv_reverse.addTransition(opc.do2.updated, self.set_speed_pressure3)
        self.set_speed_pressure3.addTransition(opc.pchv.speed_reached, self.measure_p3)
        self.measure_p3.addTransition(self.measure_p3.done, self.set_speed_pressure4)
        self.measure_p3.addTransition(opc.ai.updated, self.measure_p3)
        self.set_speed_pressure4.addTransition(opc.pchv.speed_reached, self.measure_p4)
        self.measure_p4.addTransition(self.measure_p4.done, self.stop_pchv2)
        self.measure_p4.addTransition(opc.ai.updated, self.measure_p4)
        self.stop_pchv2.addTransition(opc.pchv.break_on, self.connect_pchv2)

        self.show_frm2 = ShowFrm2(self)
        self.set_speed_pe = SetSpeed(self)
        self.set_pos0 = SetPos0(self)
        self.select_p3_i1.addTransition(self.select_p3_i1.success, self.set_speed_pe)
        self.connect_pchv2.addTransition(opc.do2.updated, self.set_speed_pe)
        self.set_speed_pe.addTransition(opc.pchv.speed_reached, self.show_frm2)
        self.show_frm2.addTransition(self.set_pos0)

        self.set_current_up = SetCurrentUp(self)
        self.set_current_down = SetCurrentDown(self)
        self.measure_iaf_up = MeasureIAF(self)
        self.measure_iaf_down = MeasureIAF(self)
        self.set_pos0.addTransition(opc.freq.updated, self.set_current_up)
        self.set_current_up.addTransition(opc.pa3.updated, self.measure_iaf_up)
        self.measure_iaf_up.addTransition(opc.pa3.updated, self.measure_iaf_up)
        self.measure_iaf_up.addTransition(self.measure_iaf_up.done, self.set_current_up)
        self.set_current_up.addTransition(self.set_current_up.done, self.set_current_down)
        self.set_current_down.addTransition(opc.pa3.updated, self.measure_iaf_down)
        self.measure_iaf_down.addTransition(opc.pa3.updated, self.measure_iaf_down)
        self.measure_iaf_down.addTransition(self.measure_iaf_down.done, self.set_current_down)

        self.stop_all = StopAll(self)
        self.extract_res = ExtractRes(self)
        self.print_result = PrintResult(self)
        self.set_current_down.addTransition(self.set_current_down.done, self.stop_all)
        self.stop_all.addTransition(self.extract_res)
        self.extract_res.addTransition(self.print_result)
        self.print_result.addTransition(btnOk, self.disconnect_devices)
        frm_main.frm_print.paintRequested.connect(self.print_result.preview)


class Error(QtCore.QState):
    def onEntry(self, e):
        pass


class StopPCHV(QtCore.QState):
    def onEntry(self, e):
        opc.pchv.stop()


class DisconnectDevices(QtCore.QState):
    def onEntry(self, e):
        opc.pchv.setActive(False)
        opc.do2.setValue([0] * 32)


class Finish(QtCore.QFinalState):
    def onEntry(self, e):
        opc.ai.setActive(False)
        opc.di.setActive(True)
        opc.pv1.setActive(False)
        opc.pv2.setActive(False)
        opc.pa1.setActive(False)
        opc.pa2.setActive(False)
        opc.pa3.setActive(False)
        frm_main.connectmenu()
        opc.pchv.setActive(False)


class Install0(QtCore.QState):
    def onEntry(self, e):
        global data
        frm_main.disconnectmenu()
        opc.freq.setClear(2)
        opc.ai.setActive(True)
        opc.di.setActive(True)
        opc.pa3.setActive(True)
        opc.pchv.setActive(False)
        # frm_main.stl.setCurrentWidget(frm)
        data = Data()


class Install1(QtCore.QState):
    def onEntry(self, e):
        frm_main.stl.setCurrentWidget(frm_main.exam_iu_pe_inst1)


class Install2(QtCore.QState):
    def onEntry(self, e):
        frm_main.stl.setCurrentWidget(frm_main.exam_iu_pe_inst2)


class Install3(QtCore.QState):
    def onEntry(self, e):
        frm_main.stl.setCurrentWidget(frm_main.exam_iu_pe_inst3)


class Install4(QtCore.QState):
    def onEntry(self, e):
        frm_main.stl.setCurrentWidget(frm_main.exam_iu_pe_inst4)


class ConnectDev(QtCore.QState):
    def onEntry(self, QEvent):
        opc.pchv.setActive(True)
        opc.connect_pchv(True, iu.dir[0])
        opc.connect_pe(True)
        opc.connect_dp(True)
        opc.current.setActive('manual', 10)


class ConnectPchvReverse(QtCore.QState):
    def onEntry(self, QEvent):
        opc.connect_pchv(True, iu.dir[1])
        data.speed_idx = 1


class ConnectPchv(QtCore.QState):
    def onEntry(self, QEvent):
        opc.connect_pchv(True, iu.dir[0])


class Prepare(QtCore.QState):
    def onEntry(self, QEvent):
        global ti
        frm_main.stl.setCurrentWidget(frm1)
        ti = time.time()
        opc.pchv.speed = iu.speed[0]
        frm1.timer.setValue(frm1.timer.max_v)
        data.pr = []
        data.note = ''


class WaitTimer(QtCore.QState):
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        t = frm1.timer.max_v + ti - time.time()
        frm1.timer.setValue(t)
        frm1.text.setText('<p>Ожидайте.<br>Выполняется прогрев исполнительного устройства перед началом '
                          'испытания.</p><p>Осталось {: 3.0f} мин {: 2.0f} сек</p>'.format(t // 60, t % 60))
        if t <= 0:
            data.speed_idx = 1
            self.done.emit()


class SetSpeed(QtCore.QState):
    def onEntry(self, QEvent):
        opc.pchv.speed = iu.speed[data.speed_idx]
        frm1.text.setText('<p>Ожидайте.<br>Выполняется установка скорости вращения '
                          '{: 4.0f}</p>'.format(iu.speed[data.speed_idx]))
        data.count = 0
        data.value = 0


class MeasureP(QtCore.QState):
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        data.count += 1
        data.value += opc.pressure
        frm1.text.setText('<p>Ожидайте.<br>Выполняется измерение давления в аккумуляторе<br>'
                          'Давление: {: 5.3f} МПа, измерение завершено на: {:.0%}</p>'.format(data.value / data.count,
                                                                                              data.count / 23))
        if data.count == 23:
            data.pr.append(data.value / data.count)
            data.speed_idx += 1
            self.done.emit()


class SelectP3I1(QtCore.QState):
    success = QtCore.pyqtSignal()
    fail = QtCore.pyqtSignal()

    def onEntry(self, QEvent):

        if iu.dir[0] == iu.dir[1]:
            data.speed_idx = 3
            self.success.emit()
        else:
            self.fail.emit()


class ShowFrm2(QtCore.QState):
    def onEntry(self, QEvent):
        frm_main.stl.setCurrentWidget(frm)


class SetPos0(QtCore.QState):
    def onEntry(self, QEvent):
        opc.current.setActive('manual', 0)
        frm.text.setText('<p>Ожидайте.<br>Выполняется установка тока 0 А в силовой цепи.</p>')
        # frm.img.setPixmap(frm.img_empty)
        frm.img.setMinimumHeight(frm.GR_HEIGHT)
        frm.img.clear()
        opc.freq.setClear(0)
        data.count = 0
        opc.ai.setActive(False)


class SetCurrentUp(QtCore.QState):
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        data.i = opc.pa3.value
        data.a = opc.freq.value[0]
        data.f = opc.freq.value[7]

        if data.i > 2.6 or data.a > 9.5 or data.count > 990:

            self.done.emit()
        else:
            frm.text.setText('<p>Выполняется построение рабочей диаграмы:</p>'
                             f'<p>Ток силовой цепи {data.i:5.3f} А<br>'
                             f'Позиция указателя нагрузки {data.a:4.1f}<br>'
                             f'Частота датчика положения {data.f:6.3f} кГц'
                             f'</p>')
            data.arr.append((data.i, data.a, data.f))
            frm.arr = data.arr
            frm.img.update()
        if 0.5 <= data.a <= 2.5 or 7.5 <= data.a <= 9.5 or 1.25 <= data.i <= 1.35 or 1.95 <= data.i <= 2.05:
            data.count += 1
        else:
            data.count += 5
        opc.current.setActive('manual', data.count)
        data.count2 = 0
        data.i = 0
        data.a = 0
        data.f = 0


class SetCurrentDown(QtCore.QState):
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        data.i = opc.pa3.value
        data.a = opc.freq.value[0]
        data.f = opc.freq.value[7]
        if data.i < 0.8 or data.a < 0.1 or data.count < 10:
            self.done.emit()
        else:
            frm.text.setText(f'<p>Выполняется построение рабочей диаграмы:</p>'
                             f'<p>Ток силовой цепи {data.i:5.3f} А<br>'
                             f'Позиция указателя нагрузки {data.a:4.1f}<br>'
                             f'Частота датчика положения {data.f:6.3} кГц'
                             f'</p>')
            data.arr.append((data.i, data.a, data.f))
            frm.arr = data.arr
            frm.img.update()

        if 0.5 <= data.a <= 2.5 or 7.5 <= data.a <= 9.5 or 1.25 <= data.i <= 1.35 or 1.95 <= data.i <= 2.05:
            data.count -= 1
        else:
            data.count -= 5

        opc.current.setActive('manual', data.count)

        data.count2 = 0
        data.i = 0
        data.a = 0
        data.f = 0


class MeasureIAF(QtCore.QState):
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):

        data.count2 += 1
        data.i += opc.pa3.value
        data.a += opc.freq.value[0]
        data.f += opc.freq.value[7]
        if opc.pa3.value < 0.8:
            self.done.emit()
        if data.count2 >= 0:
            data.i /= data.count2
            data.a /= data.count2
            data.f /= data.count2
            self.done.emit()


class StopAll(QtCore.QState):
    def onEntry(self, QEvent):
        global data
        opc.current.setActive('manual', 0)
        opc.pchv.speed = 0


class ExtractRes(QtCore.QState):
    def onEntry(self, QEvent):
        global data
        data.arr = [v for v in data.arr if 0.8 <= v[0] <= 2.6]

        def MNK(values):
            n = len(values)
            if not n: return 0, 0
            sumx = sum([v[0] for v in values])
            sumy = sum([v[1] for v in values])
            sumx2 = sum([v[0] * v[0] for v in values])
            sumxy = sum([v[0] * v[1] for v in values])
            if n * sumx2 - sumx * sumx == 0: return 0, 0
            a = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
            b = (sumy - a * sumx) / n
            return a, b

        data.arr_average = []
        for a in range(0, 10):
            a_min = a - 0.5
            a_max = a + 0.5
            data_a = [v for v in data.arr if a_min <= v[1] <= a_max]
            data_i = [(v[1], v[0]) for v in data_a]
            data_f = [(v[1], v[2]) for v in data_a]
            ai, bi = MNK(data_i)
            af, bf = MNK(data_f)
            data.arr_average.append((ai * a + bi, a, af * a + bf))

        if data.arr_average[1][0] == 0:
            data.note += 'Не удалось установить вал регулятора в позицию "1";'
            data.f1 = 0
        else:
            data.f1 = data.arr_average[1][2]

        if data.arr_average[2][0] == 0:
            data.note += 'Не удалось установить вал регулятора в позицию "2";'
            data.i2 = 0
        else:
            data.i2 = data.arr_average[2][0]

        if data.arr_average[8][0] == 0:
            data.note += 'Не удалось установить вал регулятора в позицию "8";'
            data.i8 = 0
        else:
            data.i8 = data.arr_average[8][0]

        if data.arr_average[9][0] == 0:
            data.note += 'Не удалось установить вал регулятора в позицию "9";'
            data.f9 = 0
        else:
            data.f9 = data.arr_average[9][2]


class PrintResult(QtCore.QState):
    HEIGHT = 1200
    WIDTH = 1600
    K_X = 800
    K_Y = 100
    OFF_X = 80
    OFF_Y = 40
    OFF_I = 0.8

    def onEntry(self, QEvent):
        settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        settings.setIniCodec('UTF-8')
        protocol_path = settings.value('protocol/path', 'c:\\протоколы\\')
        settings.setValue('protocol/path', protocol_path)
        last_date = settings.value('protocol/date', '01-01-2019')
        data.num = int(settings.value('protocol/num', 0))
        today = datetime.datetime.today()
        month = int(str(last_date).split('-')[1])
        if month != today.month:
            data.num = 0
        data.num += 1
        protocol_path += f'{today.year:0>4}-{today.month:0>2}\\'
        if not os.path.exists(protocol_path):
            os.makedirs(protocol_path)
        protocol_path += f'N {data.num} {today.day:0>2}-{today.month:0>2}-{today.year:0>4} ИУ {iu.dev_type} завN' + \
                         f' {frm_main.auth.num} {frm_main.auth.date}.pdf'

        frm_main.frm_print.updatePreview()
        frm_main.stl.setCurrentWidget(frm_main.frm_print)
        wr = QtGui.QPdfWriter(protocol_path)
        self.preview(wr)

        settings.setValue('protocol/num', data.num)
        settings.setValue('protocol/date', today.strftime('%d-%m-%Y'))

    def preview(self, printer):
        SPACE = 62
        # V_SPACE = 20

        layout = QtGui.QPageLayout()
        layout.setPageSize(QtGui.QPageSize(QtGui.QPageSize.A4))
        layout.setOrientation(QtGui.QPageLayout.Portrait)
        # layout.setMargins(20, 10, 5, 15, QtPrintSupport.QPrinter.Millimeter)
        printer.setPageLayout(layout)
        printer.setResolution(300)
        painter = QtGui.QPainter()

        painter.begin(printer)
        color = QtGui.QColor(QtCore.Qt.black)
        pen = QtGui.QPen(color)
        brush = QtGui.QBrush(color)
        font = QtGui.QFont('Segoi ui', 10)
        header_font = QtGui.QFont('Segoi ui', 14)
        painter.setPen(pen)
        painter.setBrush(brush)
        protocol_num = data.num
        protocol_date = datetime.datetime.today().strftime('%d-%m-%Y')

        # Заголовок
        # x, y = 200, 30
        x, y = 625, 94
        painter.setFont(header_font)
        painter.drawText(x, y, f'Протокол испытания № {protocol_num: <3d} от  {protocol_date}')
        painter.setFont(font)
        # Шапка
        # x = 50
        x = 156
        y += SPACE * 2.5
        painter.drawText(x, y, f'Тип исполнительного устройства: {iu.dev_type}')
        y += SPACE
        painter.drawText(x, y, f'Зав. № {frm_main.auth.num}     Дата изготовления: {frm_main.auth.date}')
        y += SPACE
        painter.drawText(x, y, f'Тепловоз № {frm_main.auth.locomotive}     Секция: {frm_main.auth.section}')
        # Шапка таблицы
        y += SPACE * 1.5
        # w = [0, 400, 520, 620]
        w = [0, 1250, 1625, 1937]

        def print_row(row):
            nonlocal x, y
            for i, v in enumerate(row):
                painter.drawText(x + w[i], y, v)
            y += SPACE

        if data.arr:
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 4))
            points = [QtCore.QPointF(x + self.OFF_X + (i[0] - self.OFF_I) * self.K_X,
                                     y + self.HEIGHT - self.OFF_Y - i[1] * self.K_Y) for i in data.arr]
            points2 = [QtCore.QPointF(x + self.OFF_X + (i[0] - self.OFF_I) * self.K_X,
                                      y + self.HEIGHT - self.OFF_Y - i[1] * self.K_Y) for i in data.arr_average]
            painter.drawLine(x + self.OFF_X, y + self.HEIGHT - self.OFF_Y + 5, x + self.OFF_X, y + self.OFF_Y)
            painter.drawLine(x + self.OFF_X - 5, y + self.HEIGHT - self.OFF_Y, x + self.WIDTH - self.OFF_X,
                             y + self.HEIGHT - self.OFF_Y)

            for xx in range(0, self.WIDTH - self.OFF_X * 2, int(self.K_X / 10)):
                QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.lightGray)), 1)
                painter.drawLine(x + self.OFF_X + xx, y + self.HEIGHT - self.OFF_Y - 5,
                                 x + self.OFF_X + xx, y + 2 * self.OFF_Y)
                QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 4)
                painter.drawLine(x + self.OFF_X + xx, y + self.HEIGHT - self.OFF_Y + 5,
                                 x + self.OFF_X + xx, y + self.HEIGHT - self.OFF_Y - 5)
                painter.drawText(x + self.OFF_X + xx - 25,
                                 y + self.HEIGHT - 2,
                                 f'{((xx) / self.K_X+self.OFF_I):3.1f}')
            for yy in range(1, 11):
                QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.lightGray)), 1)
                painter.drawLine(x + self.OFF_X + 5, y + self.HEIGHT - self.OFF_Y - yy * self.K_Y,
                                 x + self.OFF_X + self.WIDTH - 2 * self.OFF_X,
                                 y + self.HEIGHT - self.OFF_Y - yy * self.K_Y)
                QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 4)
                painter.drawLine(x + self.OFF_X - 5, y + self.HEIGHT - self.OFF_Y - yy * self.K_Y,
                                 x + self.OFF_X + 5, y + self.HEIGHT - self.OFF_Y - yy * self.K_Y)
                painter.drawText(x - 10,
                                 y + self.HEIGHT - self.OFF_Y - yy * self.K_Y + 7,
                                 f'{yy:3.1f}')
            painter.drawText(x + self.OFF_X + 10, y + self.OFF_Y + 10, 'Поз. инд.')
            painter.drawText(x + self.WIDTH - 30, y + self.HEIGHT - 5, 'I, A')
            i1, a1, i2, a2 = 1.3, 2.0, 2.0, 8.0
            QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.green)), 1)
            painter.drawLine(x + self.OFF_X + (i1 - 0.05 - self.OFF_I) * self.K_X,
                             y + self.HEIGHT - self.OFF_Y - a1 * self.K_Y,
                             x + self.OFF_X + (i2 - 0.05 - self.OFF_I) * self.K_X,
                             y + self.HEIGHT - self.OFF_Y - a2 * self.K_Y)
            painter.drawLine(x + self.OFF_X + (i1 + 0.05 - self.OFF_I) * self.K_X,
                             y + self.HEIGHT - self.OFF_Y - a1 * self.K_Y,
                             x + self.OFF_X + (i2 + 0.05 - self.OFF_I) * self.K_X,
                             y + self.HEIGHT - self.OFF_Y - a2 * self.K_Y)

            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)), 1))
            painter.drawPolyline(*points)

            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.red)), 8))
            painter.drawPolyline(*points2)

            # painter.drawRect(x + self.WIDTH - 300, y,
            #                 x + self.WIDTH, y + 200)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.red)), 8))
            painter.drawLine(x + self.WIDTH - 40, y + 250, x + self.WIDTH, y + 250)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)), 4))
            painter.drawLine(x + self.WIDTH - 40, y + 300, x + self.WIDTH, y + 300)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.green)), 4))
            painter.drawLine(x + self.WIDTH - 40, y + 350, x + self.WIDTH, y + 350)

            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)), 2))
            painter.drawText(x + self.WIDTH + 20, y + 250, 'Рабочая характеристика')
            painter.drawText(x + self.WIDTH + 20, y + 300, 'Данные измерений')
            painter.drawText(x + self.WIDTH + 20, y + 350, 'Норм. характеристика')

            y += 1300

        print_row(['Параметр', 'Норма', 'Факт', 'Результат'])
        y += SPACE
        # y += 20
        name = f'1. Давление масла на скорости {iu.speed[1]} об/мин, МПа'
        norm = f'не менее {iu.pressure[0]: >3.1f}'
        print_row([name, norm, '', ''])
        name = '     - при левом вращении' if iu.dir[0] else '     - при правом вращении'
        norm = ''
        fact = f'{data.pr[0]: <4.1f}'
        res = 'норма' if data.pr[0] >= iu.pressure[0] else 'НЕ НОРМА'
        print_row([name, norm, fact, res])
        if iu.dir[0] != iu.dir[1]:
            name = '     - при левом вращении' if iu.dir[1] else '     - при правом вращении'
            norm = ''
            fact = f'{data.pr[2]: <4.1f}'
            res = 'норма' if data.pr[2] >= iu.pressure[0] else 'НЕ НОРМА'
            print_row([name, norm, fact, res])

        name = f'2. Давление масла на скорости {iu.speed[2]} об/мин, МПа'
        norm = f'не менее {iu.pressure[1]: >3.1f}'
        print_row([name, norm, '', ''])
        name = '     - при левом вращении' if iu.dir[0] else '     - при правом вращении'
        norm = ''
        fact = f'{data.pr[1]: <4.1f}'
        res = 'норма' if data.pr[1] >= iu.pressure[1] else 'НЕ НОРМА'
        print_row([name, norm, fact, res])
        if iu.dir[0] != iu.dir[1]:
            name = '     - при левом вращении' if iu.dir[1] else '     - при правом вращении'
            norm = ''
            fact = f'{com.pr[3]: <4.1f}'
            res = 'норма' if data.pr[3] >= iu.pressure[1] else 'НЕ НОРМА'
            print_row([name, norm, fact, res])

        name = '3. Проверка тока ПЭ на позиции "2", А'
        norm = f'{iu.current[0]:4.3f}-{iu.current[1]:4.3f}'
        fact = f'{data.i2: <4.3f}'
        res = 'норма' if iu.current[0] <= data.i2 <= iu.current[1] else 'НЕ НОРМА'
        print_row([name, norm, fact, res])

        name = '4. Проверка тока ПЭ на позиции "8", А'
        norm = f'{iu.current[2]:4.3f}-{iu.current[3]:4.3f}'
        fact = f'{data.i8: <4.3f}'
        res = 'норма' if iu.current[2] <= data.i8 <= iu.current[3] else 'НЕ НОРМА'
        print_row([name, norm, fact, res])

        if not (iu.freq is None):
            name = '5. Проверка сигнала ДП на позиции "1", кГц'
            if data.f1 > data.f9:
                norm = 'не менее 24'
                res = 'норма' if data.f1 >= iu.freq[1] else 'НЕ НОРМА'
            else:
                norm = 'не более 20'
                res = 'норма' if 10 <= data.f1 <= iu.freq[0] else 'НЕ НОРМА'
            fact = f'{data.f1: <6.3f}'

            print_row([name, norm, fact, res])

            name = '6. Проверка сигнала ДП на позиции "9", кГц'
            if data.f1 < data.f9:
                norm = 'не менее 24'
                res = 'норма' if data.f9 >= iu.freq[1] else 'НЕ НОРМА'
            else:
                norm = 'не более 20'
                res = 'норма' if 10 <= data.f9 <= iu.freq[0] else 'НЕ НОРМА'
            fact = f'{data.f9: <6.3f}'

            print_row([name, norm, fact, res])

        if data.note:
            note = data.note.split(';')
            y += SPACE * 2.5
            painter.drawText(x, y, 'Примечание:')
            for s in note:
                y += SPACE
                painter.drawText(x + 40, y, s)

        painter.setFont(header_font)
        y += SPACE * 2.5
        painter.drawText(x, y, 'Испытание провел:')
        painter.drawText(x + 312, y, f'{frm_main.auth.name1: >50}    {"_" * 20}')
        # painter.drawText(x + 100, y, '{: >50}    {}'.format(com.auth.name1, '_' * 20))

        y += SPACE * 2
        painter.drawText(x, y, 'Испытание проверил:')
        painter.drawText(x + 312, y, f'{frm_main.auth.name2: >50}    {"_" * 20}')

        painter.end()
