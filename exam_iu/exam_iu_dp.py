from PyQt5 import QtCore

com = None


class ExamIUDP(QtCore.QState):
    """Установка поворотного электромагнита на исполнительное устройство"""
    success = QtCore.pyqtSignal()
    fail = QtCore.pyqtSignal()
    btnBack = None
    btnOk = None

    def __init__(self, parent=None, server=None, form=None):
        super().__init__(parent)
        global com
        com = self
        self.speed = 500
        self.reverse = False
        self.f1 = 0
        self.f2 = 0
        self.f3 = 0
        self.opc = server
        self.current = server.current
        self.frm_main = form
        self.frm = self.frm_main.exam_iu_dp_check
        self.text = self.frm.text
        self.btnOk = self.frm_main.btnPanel.btnOk.clicked
        self.btnBack = self.frm_main.btnPanel.btnBack.clicked
        self.pchv = self.opc.pchv
        self.tachometer = self.frm.tachometer
        self.pchv.speed_changed.connect(self.tachometer.setValue, QtCore.Qt.QueuedConnection)
        self.pchv.task_changed.connect(self.tachometer.setTask, QtCore.Qt.QueuedConnection)
        self.pa3 = self.opc.pa3
        self.pa3.changed.connect(self.frm.pa3.setValue, QtCore.Qt.QueuedConnection)
        self.freq = self.opc.freq
        self.pida = self.opc.pida
        self.pidc = self.opc.pidc
        self.indicator = self.frm.indicator
        self.pida.task_changed.connect(self.indicator.setTask, QtCore.Qt.QueuedConnection)
        self.opc.br2_changed.connect(self.indicator.setValue, QtCore.Qt.QueuedConnection)
        self.opc.dp_changed.connect(self.frm.dp.setValue, QtCore.Qt.QueuedConnection)
        com.btnBack = self.frm_main.btnPanel.btnBack.clicked
        com.btnOk = self.frm_main.btnPanel.btnOk.clicked
        self.ao = self.opc.ao

        # Обработка ошибок и возврат по нажатию НАЗАД
        self.error = Error(self)
        self.stop_PCHV = StopPCHV(self)
        self.wait_stop_pchv = WaitStopPCHV(self)
        self.disconnect_devices = DisconnectDevices(self)
        self.finish = Finish(self)
        self.addTransition(com.opc.error, self.error)
        self.error.addTransition(self.stop_PCHV)
        self.addTransition(com.btnBack, self.stop_PCHV)
        self.stop_PCHV.addTransition(self.wait_stop_pchv)
        self.wait_stop_pchv.addTransition(self.pchv.updated, self.wait_stop_pchv)
        self.wait_stop_pchv.addTransition(self.success, self.disconnect_devices)
        self.disconnect_devices.addTransition(self.finish)

        # Подготовка к испытанию и установка оборудования на стенд
        self.install_0 = Install0(self)
        self.install_1 = Install1(self)
        self.install_2 = Install2(self)
        self.install_3 = Install3(self)
        self.install_4 = Install4(self)
        self.set_dp = SetDp(self)

        self.install_0.addTransition(self.install_1)
        self.install_1.addTransition(com.btnOk, self.install_3)
        self.install_3.addTransition(com.btnOk, self.install_4)
        self.install_4.addTransition(com.btnOk, self.set_dp)

        # Подключение ДП и измерение максимальной частоты
        self.connect_dev = ConnectDev(self)
        self.show_f3 = ShowF3(self)
        self.measure_f3 = MeasureF3(self)
        self.set_dp.addTransition(self.btnOk, self.connect_dev)
        self.connect_dev.addTransition(self.show_f3)
        self.show_f3.addTransition(self.btnOk, self.measure_f3)

        # Установка на начальную позицию
        self.set_pos_0 = SetPos0(self)
        self.wait_pos_0 = WaitPos0(self)
        self.reset_br2 = ResetBr2(self)
        self.show_f1 = ShowF1(self)
        self.measure_f1 = MeasureF1(self)
        self.measure_f3.addTransition(self.set_pos_0)
        self.set_pos_0.addTransition(self.pchv.speed_reached, self.wait_pos_0)
        self.wait_pos_0.addTransition(self.wait_pos_0.done, self.reset_br2)
        self.wait_pos_0.addTransition(self.pa3.updated, self.wait_pos_0)
        self.reset_br2.addTransition(self.freq.updated, self.show_f1)
        self.show_f1.addTransition(self.btnOk, self.measure_f1)

        # Запуск ПЧВ и установка в позицию 10
        self.start_pchv = StartPCHV(self)
        self.set_pos8 = SetPos8(self)
        self.reset_br3 = ResetBr3(self)
        self.tune_current = TuneCurrent(self)
        self.measure_f2 = MeasureF2(self)
        self.measure_f1.addTransition(self.start_pchv)
        self.start_pchv.addTransition(self.pchv.speed_reached, self.set_pos8)
        self.set_pos8.addTransition(self.pidc.task_reached, self.reset_br3)
        self.reset_br3.addTransition(self.tune_current)
        # self.tune_current.addTransition(self.opc.br3_changed, self.tune_current)
        self.tune_current.addTransition(self.btnOk, self.measure_f2)

        # Результаты проверки
        self.set_current_0 = SetCurrent0(self)
        self.set_speed_0 = SetSpeed0(self)
        self.show_result = ShowResult(self)
        self.tune_dp = TuneDP(self)
        self.measure_f2.addTransition(self.set_current_0)
        self.set_current_0.addTransition(self.set_speed_0)
        self.set_speed_0.addTransition(self.show_result)
        self.show_result.addTransition(self.btnOk, self.tune_dp)
        self.tune_dp.addTransition(self.btnOk, self.measure_f1)

        self.setInitialState(self.install_0)


class Error(QtCore.QState):
    def onEntry(self, e):
        pass


class StopPid(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.current.setActive('manual', 0)


class StopPCHV(QtCore.QState):
    def onEntry(self, e):
        global com
        com.pchv.stop()


class WaitStopPCHV(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        if com.pchv.speed < 100:
            com.success.emit()


class DisconnectDevices(QtCore.QState):
    def onEntry(self, e):
        global com
        com.opc.do2.value = [0] * 32
        com.opc.do2.setActive()


class Finish(QtCore.QFinalState):
    def onEntry(self, e):
        global com
        com.opc.ai.setActive(False)
        com.opc.di.setActive(True)
        com.opc.pv1.setActive(False)
        com.opc.pv2.setActive(False)
        com.opc.pa1.setActive(False)
        com.opc.pa2.setActive(False)
        com.opc.pa3.setActive(False)
        com.pchv.setActive(False)
        # com.pidc.setActive(False)
        com.frm_main.connectmenu()
        com.opc.set_encoder_invert(False)


class Install0(QtCore.QState):
    """подготовка"""

    def onEntry(self, e):
        global com
        com.frm_main.disconnectmenu()
        com.dev_type = com.frm_main.select_iu.dev_type
        if com.dev_type in ['ЭГУ110', ]:
            com.opc.set_encoder_invert(True)
        if com.dev_type in ['ЭГУ104Л', 'ЭГУ102', 'ЭГУ110', 'ЭГУ114', 'ЭГУ116']:
            com.reverse = True
        else:
            com.reverse = False
        if com.dev_type == 'ЭГУ102':
            com.speed = 350
        else:
            com.speed = 500
        com.indicator.setArrowVisible(True, False)
        com.indicator.text.setVisible(False)
        com.frm.dp.setArrowVisible(True, False)
        com.freq.setClear(2)
        com.opc.ai.setActive(False)
        com.opc.di.setActive(True)
        com.opc.pv1.setActive(False)
        com.opc.pv2.setActive(False)
        com.opc.pa1.setActive(False)
        com.opc.pa2.setActive(False)
        com.opc.pa3.setActive(True)
        com.pchv.setActive(False)
        com.f1 = 0
        com.f2 = 0
        com.f3 = 0


class Install1(QtCore.QState):
    """установка оборудования 1"""

    def onEntry(self, e):
        global com
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_inst1)


class Install2(QtCore.QState):
    """установка оборудования 2"""

    def onEntry(self, e):
        global com
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_inst2)


class Install3(QtCore.QState):
    """установка оборудования 3"""

    def onEntry(self, e):
        global com
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_inst3)


class Install4(QtCore.QState):
    """установка оборудования 4"""

    def onEntry(self, e):
        global com
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_inst4)


class SetDp(QtCore.QState):
    """установка ПЭ на ИУ"""

    def onEntry(self, e):
        global com
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_set_dp)


class ConnectDev(QtCore.QState):
    """Подключение ПЧВ, ПЭ и ДП"""

    def onEntry(self, e):
        global com
        com.pchv.setActive(True)
        com.opc.connect_pchv(True, com.reverse)
        com.current.setActive('manual', 0)
        com.opc.connect_pe()
        com.opc.connect_dp()


class ShowF3(QtCore.QState):
    """Начало испытания"""

    def onEntry(self, e):
        global com
        com.text.setText(
            '<p>Необходимо ослабить стопорный болт рычага, сопряженного с пальцем 21 и задвинуть толкатель'
            ' 20, на котором установлены ферритовые кольца в катушку 22 до упора.</p>' + \
            '<p><br>Нажать ДА для продолжения.</p>')
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_dp_check)


class MeasureF3(QtCore.QState):
    """Запись частоты полностью задвинутого ДП"""

    def onEntry(self, QEvent):
        global com
        com.f3 = com.opc.dp


class SetPos0(QtCore.QState):
    """Запуск ПЧВ для установки позиции 0"""

    def onEntry(self, QEvent):
        global com
        com.pchv.set_speed(com.speed)
        com.text.setText('<p>Ожидайте.<br>Производится кратковременный запуск двигателя для установки'
                         ' индикатора нагрузки в положение "0"</p>')


class WaitPos0(QtCore.QState):
    """Установка позиции 0"""
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        global com
        com.current.setActive('manual', 0)
        com.text.setText('<p>Ожидайте.<br>Производится установка тока 0 А в силовой цепи</p>')
        if com.pa3.value < 0.9:
            self.done.emit()


class ResetBr2(QtCore.QState):
    """Сброс энкодера угла BR2"""

    def onEntry(self, QEvent):
        global com
        com.freq.setClear(0)
        com.indicator.setArrowVisible(True, False)
        com.indicator.text.setVisible(True)
        com.text.setText('<p>Ожидайте.<br>Производитсясброс датчика угла</p>')


class ShowF1(QtCore.QState):
    """Установка ДП в начальное положение"""

    def onEntry(self, QEvent):
        global com
        com.pchv.set_speed(0)
        com.text.setText(
            '<p>Установить выходной вал исполнительного устройства в положении "СТОП", при этом '
            'указатель нагрузки должен находится в положении "0"</p>'
            '<p>Изменяя положение рычага, сопряженного с пальцем 21, относительно зафиксированного в положении "СТОП" '
            'выходного вала 6 исполнительного устройства, установить его так, чтобы толкатель выступал относительно'
            'торца втулки на 0,5±0,5 мм. Стопорным болтом закрепить рычаг.</p>'
            '<p><br>Нажать ДА для продолжения<br></p>')


class MeasureF1(QtCore.QState):
    """Запись частоты начального положения ДП"""

    def onEntry(self, QEvent):
        global com
        com.f1 = com.opc.dp


class StartPCHV(QtCore.QState):
    """Запуск ПЧВ для установки указателя на поз. 10"""

    def onEntry(self, QEvent):
        global com
        com.pchv.set_speed(com.speed)
        com.text.setText('<p>Ожидайте</p><p>Производится установка скорости вращения вала исполнительного' + \
                         ' устройства 500 об/мин.</p>')


class SetPos8(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        com.current.setActive('pidc', 2.0)
        com.text.setText('<p>Ожидайте.</p><p>Производится предварительная установка тока 2 A в силовой цепи' + \
                         ' поворотного электромагнита</p>')


class ResetBr3(QtCore.QState):
    """Сброс энкодера Br3"""

    def onEntry(self, QEvent):
        global com
        # com.u = com.ao.value[2]
        # com.freq.setClear(2)
        com.current.setActive('br3')
        com.text.setText('<p>Поворотом рукоятки энкодера BR3 установите ток в силовой цепи таким образом, чтобы ' + \
                         'указатель нагрузки исполнительного устройства находился на позиции "10"</p>' + \
                         '<p><font color="red">Внимание!!! Будьте осторожны и старайтесь не повышать ток в силовой' + \
                         ' цепи больше необходимого, поскольку это может привести к механической поломке датчика ' + \
                         'положения, в том случае, если он не правильно отрегулирован. Так же не рекомендуется ' + \
                         'находится в этом режиме дольше нескольких минут во избежание перегрева силовой' + \
                         'цепи стенда.<font color="black"></p><p><br>Нажать ДА для продолжения</p>')


class TuneCurrent(QtCore.QState):
    """Ручная регулировка тока для установки позиции 10"""

    def onEntry(self, QEvent):
        global com
        # com.ao.setValue(com.u + com.opc.br3, 2)
        pass


class MeasureF2(QtCore.QState):
    """Запись частоты конечного положения ДП"""

    def onEntry(self, QEvent):
        global com
        com.f2 = com.opc.dp


class SetCurrent0(QtCore.QState):
    """Сброс тока в 0"""

    def onEntry(self, QEvent):
        global com
        com.current.setActive('manual', 0)
        com.text.setText('<p>Ожидайте.</p><p>Производится отключение силовой цепи</p>')


class SetSpeed0(QtCore.QState):
    """Остановка ПЧВ"""

    def onEntry(self, QEvent):
        global com
        com.pchv.set_speed(0)
        com.text.setText('<p>Ожидайте.</p><p>Производится остановка привода</p>')
        if com.pchv.speed < 100:
            comm.success.emit()


class ShowResult(QtCore.QState):
    """Отображение результатов проверки"""

    def onEntry(self, QEvent):
        global com
        if com.f1 < com.f2:
            res1 = 'НОРМА' if com.f1 <= 20 else '<font color="red">НЕ НОРМА<font color="black">'
            res2 = 'НОРМА' if com.f2 >= 24 else '<font color="red">НЕ НОРМА<font color="black">'
            res3 = 'НОРМА' if com.f3 >= com.f2 + 0.5 else '<font color="red">НЕ НОРМА<font color="black">'
            com.text.setText('<p>Результаты проверки:</p>'
                             '<p>Показания датчика положения:<br> на позиции "0": '
                             '{:6.3f} кГц, норма не более 20 кГц, результат: {}<br>'.format(com.f1, res1) + \
                             ' на позиции "10": '
                             '{:6.3f} кГц, норма не менее 24 кГц, результат: {}<br>'.format(com.f2, res2) + \
                             'в крайнем положении: {:6.3f} кГц, норма: больше чем на позиции "10"'.format(com.f3) + \
                             ', результат: {}</p>'.format(res3) + \
                             '<p><br>Нажать ДА для продолжения</p>')
        else:
            res1 = 'НОРМА' if com.f1 >= 24 else '<font color="red">НЕ НОРМА<font color="black">'
            res2 = 'НОРМА' if com.f2 <= 20 else '<font color="red">НЕ НОРМА<font color="black">'
            res3 = 'НОРМА' if com.f3 <= com.f2 - 0.5 else '<font color="red">НЕ НОРМА<font color="black">'
            com.text.setText('<p>Результаты проверки:</p>'
                             '<p>Показания датчика положения:<br> на позиции "0": '
                             '{:6.3f} кГц, норма не менее 24 кГц, результат: {}<br>'.format(com.f1, res1) + \
                             ' на позиции "10": '
                             '{:6.3f} кГц, норма не более 20 кГц, результат: {}<br>'.format(com.f2, res2) + \
                             'в крайнем положении: {:6.3f} кГц, норма: меньше чем на позиции "10"'.format(com.f3) + \
                             ', результат: {}</p>'.format(res3) + \
                             '<p><br>Нажать ДА для продолжения</p>')


class TuneDP(QtCore.QState):
    """Рекомендации по настройке"""

    def onEntry(self, QEvent):
        global com
        com.text.setText('<p>Ослабив стопорный болт, поверните рычаг с пальцем 21, чтобы положение толкателя 20'
                         ' относительно торца втулки увеличилось примерно на 0,5 мм  и повторите проверку.</p><p>'
                         'Нажмите ДА для повторной проверки<br>'
                         'Нажмите НАЗАД для выхода в меню</p>')
