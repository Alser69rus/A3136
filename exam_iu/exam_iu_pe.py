from PyQt5 import QtCore

com = None


class ExamIuPe(QtCore.QState):
    """Установка поворотного электромагнита на исполнительное устройство"""
    success = QtCore.pyqtSignal()
    fail = QtCore.pyqtSignal()
    btnBack = None
    btnOk = None

    def __init__(self, parent=None, server=None, form=None):
        super().__init__(parent)
        global com
        com = self
        self.dev_type = ''
        self.reverse = False
        self.speed = 500
        self.u1 = 0
        self.u2 = 0
        self.i1 = 0
        self.i2 = 0
        self.opc = server
        self.current = server.current
        self.frm_main = form
        self.frm = self.frm_main.exam_iu_pe_check
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
        com.btnBack = self.frm_main.btnPanel.btnBack.clicked
        com.btnOk = self.frm_main.btnPanel.btnOk.clicked
        self.ao = self.opc.ao

        # Обработка ошибок и возврат по нажатию НАЗАД
        self.error = Error(self)
        self.stop_pid = StopPid(self)
        self.stop_PCHV = StopPCHV(self)
        self.wait_stop_pchv = WaitStopPCHV(self)
        self.disconnect_devices = DisconnectDevices(self)
        self.finish = Finish(self)
        self.addTransition(com.opc.error, self.error)
        self.error.addTransition(self.stop_pid)
        self.addTransition(com.btnBack, self.stop_pid)
        self.stop_pid.addTransition(self.stop_PCHV)
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
        self.set_pe = SetPe(self)
        self.show_check_win = ShowCheckWin(self)
        self.install_0.addTransition(self.install_1)
        self.install_1.addTransition(com.btnOk, self.install_3)
        self.install_3.addTransition(com.btnOk, self.install_4)
        self.install_4.addTransition(com.btnOk, self.set_pe)
        self.set_pe.addTransition(com.btnOk, self.show_check_win)

        # Запуск ПЧВ
        self.connect_pchv = ConnectPchv(self)
        self.connect_pe = ConnectPe(self)
        self.start_PCHV = StartPCHV(self)
        self.show_check_win.addTransition(self.connect_pchv)
        self.connect_pchv.addTransition(self.connect_pe)
        self.connect_pe.addTransition(self.start_PCHV)

        # Установка тока 0 А и сброс энкодера Br2
        self.set_current_0 = SetCurrent0(self)
        self.reset_br2 = ResetBr2(self)
        self.start_PCHV.addTransition(self.pchv.speed_reached, self.set_current_0)
        self.set_current_0.addTransition(self.set_current_0.done, self.reset_br2)
        self.set_current_0.addTransition(self.pa3.updated, self.set_current_0)

        # Установка тока 1,3 А и позиции 2
        self.set_current_13 = SetCurrent13(self)
        self.show_pos_2 = ShowPos2(self)
        self.tune_pos_2 = TunePos2(self)
        self.reset_br2.addTransition(self.freq.updated, self.set_current_13)
        self.set_current_13.addTransition(self.pidc.task_reached, self.show_pos_2)
        self.show_pos_2.addTransition(self.tune_pos_2)
        self.tune_pos_2.addTransition(self.opc.br3_changed, self.tune_pos_2)

        # Установка тока 2 А и позиции 8
        self.set_current_20 = SetCurrent20(self)
        self.show_pos_8 = ShowPos8(self)
        self.tune_pos_8 = TunePos8(self)
        self.tune_pos_2.addTransition(self.btnOk, self.set_current_20)
        self.set_current_20.addTransition(self.pidc.task_reached, self.show_pos_8)
        self.show_pos_8.addTransition(self.tune_pos_8)
        self.tune_pos_8.addTransition(self.opc.br3_changed, self.tune_pos_8)

        # Отображение результатов проверки и рекомендаций по настройке
        self.check_result = CheckResult(self)
        self.tune_i1 = TuneI1(self)
        self.tune_i2 = TuneI2(self)
        self.tune_pos_8.addTransition(self.btnOk, self.check_result)
        self.check_result.addTransition(self.btnOk, self.tune_i1)
        self.tune_i1.addTransition(self.success, self.tune_i2)
        self.tune_i1.addTransition(self.btnOk, self.tune_i2)
        self.tune_i2.addTransition(self.success, self.set_current_0)
        self.tune_i2.addTransition(self.btnOk, self.set_current_0)

        self.setInitialState(self.install_0)


class Error(QtCore.QState):
    def onEntry(self, e):
        pass


class StopPid(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        # com.current.setActive('pidc',0)
        com.current.setActive('manual', 0)


class StopPCHV(QtCore.QState):
    def onEntry(self, e):
        global com
        com.pchv.stop()


class WaitStopPCHV(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        if com.pchv.breaking:
            com.success.emit()


class DisconnectDevices(QtCore.QState):
    def onEntry(self, e):
        global com
        com.opc.do2.setValue([0] * 32)


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
        com.pidc.setActive(False)
        com.frm_main.connectmenu()
        com.pchv.setActive(False)
        # com.current.setActive(False)
        com.opc.set_encoder_invert(False)


class Install0(QtCore.QState):
    """подготовка"""

    def onEntry(self, e):
        global com
        com.frm_main.disconnectmenu()
        com.dev_type = com.frm_main.select_iu.dev_type
        if com.dev_type in ['ЭГУ110',]:
            com.opc.set_encoder_invert(True)
            print("invert")
        if com.dev_type in ['ЭГУ104Л', 'ЭГУ102', 'ЭГУ110', 'ЭГУ114', 'ЭГУ116']:
            com.reverse = True
        else:
            com.reverse = False
        if com.dev_type == 'ЭГУ102':
            com.speed = 350
        else:
            com.speed = 500
        com.indicator.setArrowVisible(False, False)
        com.indicator.text.setVisible(False)
        com.freq.setClear(2)
        com.opc.ai.setActive(False)
        com.opc.di.setActive(True)
        com.opc.pv1.setActive(False)
        com.opc.pv2.setActive(False)
        com.opc.pa1.setActive(False)
        com.opc.pa2.setActive(False)
        com.opc.pa3.setActive(True)
        com.pchv.setActive(False)
        com.i1 = 0
        com.i2 = 0
        com.u1 = 0
        com.u2 = 0


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


class SetPe(QtCore.QState):
    """установка ПЭ на ИУ"""

    def onEntry(self, e):
        global com
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_set_pe)


class ShowCheckWin(QtCore.QState):
    """Начало испытания"""

    def onEntry(self, e):
        global com
        com.text.setText('<p>Ожидайте.<br>Выполняется установка скорости вращения вала ИУ 500 об/мин.</p>')
        com.frm_main.stl.setCurrentWidget(com.frm_main.exam_iu_pe_check)


class ConnectPchv(QtCore.QState):
    """Подключение ПЧВ"""

    def onEntry(self, e):
        global com
        com.pchv.setActive(True)
        com.opc.connect_pchv(True, com.reverse)


class ConnectPe(QtCore.QState):
    """Подключение силового канала VD2"""

    def onEntry(self, QEvent):
        global com
        com.current.setActive('manual', 0)
        com.opc.connect_pe()


class StartPCHV(QtCore.QState):
    """Запуск ПЧВ на скорости 500"""

    def onEntry(self, e):
        global com
        com.pchv.speed = com.speed


class SetCurrent0(QtCore.QState):
    """установка тока 0 А в силовой цепи"""
    done = QtCore.pyqtSignal()

    def onEntry(self, QEvent):
        global com
        com.text.setText('<p>Ожидайте. <br>Выполняется установка тока 0 А в силовой цепи.</p>')
        com.current.setActive('manual', 0)
        if com.pa3.value < 0.9:
            self.done.emit()


class SetCurrent13(QtCore.QState):
    """Установка тока 1,3 А в силовой цепи"""

    def onEntry(self, QEvent):
        com.text.setText('<p>Ожидайте.<br>Выполняется установка тока 1,3 А в силовой цепи.</p>')
        com.current.setActive('pidc', 1.3)
        com.indicator.setTask(2)


class SetCurrent20(QtCore.QState):
    """Установка тока 2,0 А в силовой цепи"""

    def onEntry(self, QEvent):
        com.text.setText('<p>Ожидайте.<br>Выполняется установка тока 2,0 А в силовой цепи.</p>')
        com.current.setActive('pidc', 2.0)
        com.indicator.setTask(8)


class ResetBr2(QtCore.QState):
    """Сброс энкодера угла BR2"""

    def onEntry(self, QEvent):
        global com
        com.freq.setClear(0)
        com.indicator.setArrowVisible(True, True)
        com.indicator.text.setVisible(True)
        com.i1 = 0
        com.i2 = 0
        com.u1 = 0
        com.u2 = 0


class ShowPos2(QtCore.QState):
    """Подготовка к проверке позиции 2"""

    def onEntry(self, e):
        global com
        # com.u1 = com.ao.value[2]
        # com.freq.setClear(2)]
        com.current.setActive('br3')
        com.text.setText('<p>При помощи поворота рукоятки BR3 отрегулируйте ток силовой цепи ' + \
                         'таким образом, чтобы указатель нагрузки на выходном валу ИУ находился на ' + \
                         'позиции 2</p><p>Нажмите ДА для продолжения</p>')


class TunePos2(QtCore.QState):
    """Настройка тока позиции 2"""

    def onEntry(self, e):
        global com
        com.i1 = com.pa3.value
        com.indicator.setTask(2)


class ShowPos8(QtCore.QState):
    """Подготовка к проверке позиции 8"""

    def onEntry(self, QEvent):
        global com
        # com.u2 = com.ao.value[2]
        #         # com.freq.setClear(2)
        com.indicator.setTask(8)
        com.current.setActive('br3')
        com.text.setText('<p>При помощи поворота рукоятки BR3 отрегулируйте ток силовой цепи ' + \
                         'таким образом, чтобы указатель нагрузки на выходном валу ИУ находился на ' + \
                         'позиции 8.</p><p>Нажмите ДА для продолжения</p>')


class TunePos8(QtCore.QState):
    """Настройка тока позиции 2"""

    def onEntry(self, e):
        global com
        # com.ao.setValue(com.u2 + com.opc.br3, 2)
        com.i2 = com.pa3.value


class CheckResult(QtCore.QState):
    """Проверка на соответствие ТУ"""

    def onEntry(self, e):
        global com
        # com.pidc.setTask(0)
        com.current.setActive('pidc', 0)
        res1 = '<font color="green">НОРМА<font color="black">' if 1.25 <= com.i1 <= 1.35 else '<font color="red">НЕ НОРМА<font color="black">'
        res2 = '<font color="green">НОРМА<font color="black">' if 1.95 <= com.i2 <= 2.05 else '<font color="red">НЕ НОРМА<font color="black">'
        if 1.25 <= com.i1 <= 1.35 and 1.95 <= com.i2 <= 2.05:
            res3 = 'Настройка не требуется.'
        else:
            res3 = '<font color="red">Требуется настройка поворотного электромагнита.<font color="black">'

        com.text.setText('<p>Результаты проверки:<br>' + \
                         'Ток на позиции 2 выходного вала ИУ:<br>' + \
                         'Норма: {} А. Факт: {:4.3f} А. Результат: {}<br>'.format('1,25-1,35', com.i1, res1) + \
                         'Ток на позиции 8 выходного вала ИУ:<br>' + \
                         'Норма: {} А. Факт: {:4.3f} А. Результат: {}<br>'.format('1,95-2,05', com.i2, res2) + \
                         res3 + '</p><p>Нажмите НАЗАД для прекращения проверки и выхода в меню<br>' + \
                         'Нажмите ДА для продолжения проверки</p>')


class TuneI1(QtCore.QState):
    def onEntry(self, e):
        global com
        if 1.25 <= com.i1 <= 1.35:
            com.success.emit()
        else:
            com.current.setActive('pidc', 1.3)

        com.text.setText('<p>При помощи винта 25 отрегулируйте натяжение пружины 31 '
                         'чтобы стрелка указателя силового вала ИУ встала на позицию 2.</p>'
                         '<p>Если натяжением пружины не получается отрегулировать позицию указателя, '
                         'пружину следует заменить и выполнить повторную проверку.</p>'
                         '<Если заменой пружины невозможно исправить проблему, необходимо заменить'
                         'поворотный электромагнит, а неисправный отдать в ремонт.</p><br>'
                         '<p>Нажмите НАЗАД для прекращения проверки и выхода в меню<br>'
                         'Нажмите ДА для продолжения проверки</p>')


class TuneI2(QtCore.QState):
    def onEntry(self, QEvent):
        global com
        if 1.95 <= com.i2 <= 2.05:
            com.success.emit()
        else:
            com.current.setActive('pidc', 2.0)

        com.text.setText(
            '<p>Изменяя положение рычага 17 относительно привалочной плоскости поворотного электромагнита ' + \
            '(изменяя размер "L") установить стрелку указателя нагрузки на деление 8. При этом угол a не ' + \
            'должен меняться.</p>' + \
            '<p>После настройки следует выполнить повторную проверку. Если настроить поворотный электромагнит' + \
            'не удалось, то следует его заменить, а неисправный отдать в ремонт.</p>' + \
            '<p>Нажмите НАЗАД для прекращения проверки и выхода в меню<br>' + \
            'Нажмите ДА для продолжения проверки</p>')
