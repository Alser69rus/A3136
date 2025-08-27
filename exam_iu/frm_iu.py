from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
from PyQt5.QtCore import pyqtSlot as pyqtSlot

import guielement.scale as scale
from guielement.scale import ScaledDevice as ScaledDevice


class Form_iu_set_pe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        # self.pixmap = QtGui.QPixmap('img_iu1.png')
        self.pixmap = QtGui.QPixmap('exam_iu\\img_iu1.png')
        self.pixmap.setDevicePixelRatio(1.05)
        self.text = QtWidgets.QLabel(
            'Установка поворотного электромагнита на исполнительное устройство:\n' + \
            ' а) снять верхнюю крышку 4 исполнительного устройства\n' + \
            ' б) перед установкой поворотного электромагнита проверить угол a\n' + \
            '    между рычагами 18 и 32, он должен составлять 60°, при необходимости\n' + \
            '    отрегулировать поворотом рычага 18\n' + \
            'в) расстояние L от рычага 18 до привалочной плоскости должно составлять\n' + \
            '   19±0,5 мм\n' + \
            'г) установить поворотный электромагнит 9 на верхнем корпусе исполнительного\n' + \
            '   устройства и закрепить его. Закрепить свободный конец пружины 31 на\n' + \
            '   упорном рычаге 27.' + \
            '\n\nНажать кнопку ПРИНЯТЬ для продолжения')
        self.text.setFont(QtGui.QFont('Segoi UI', 13))
        self.text.setWordWrap(True)
        self.lbl = QtWidgets.QLabel()
        self.lbl.setPixmap(self.pixmap)
        self.vbox.addWidget(self.lbl)
        self.vbox.addWidget(self.text)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)


class Form_iu_set_dp(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.pixmap = QtGui.QPixmap('exam_iu\\img_iu_dp.png')
        self.pixmap.setDevicePixelRatio(1.05)
        self.text = QtWidgets.QLabel('<p>Установка датчика положения на исполнительное устройство:</p>' + \
                                     '<p> а) снять верхнюю крышку 4 исполнительного устройства</p>' + \
                                     '<p> б) установить преобразователь линейных перемещений 5 на верхнем корпусе. ' + \
                                     'При этом палец 21, ввернутый в рычаг, установленный на выходном валу ' + \
                                     'исполнительного устройства, должен войти в паз толкателя 20, на котором ' + \
                                     'закреплены ферритовые кольца. Закрепить корпус преобразователя линейных ' + \
                                     'перемещений.</p>' + \
                                     '<p><br>Нажать кнопку ПРИНЯТЬ для продолжения</p>')
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.lbl = QtWidgets.QLabel()
        self.lbl.setPixmap(self.pixmap)
        self.vbox.addWidget(self.lbl)
        self.vbox.addWidget(self.text)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)


class Form_iu_inst1(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()
        self.img = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap('exam_iu\\inst1.png')
        self.img.setScaledContents(True)
        self.pixmap.setDevicePixelRatio(1.05)
        self.img.setPixmap(self.pixmap)
        self.table = QtWidgets.QWidget()
        self.table.setLayout(self.hbox)
        self.hbox.addWidget(self.text)
        self.hbox.addSpacing(20)
        self.hbox.addWidget(self.img)
        self.hbox.addStretch(1)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.table)
        self.vbox.addStretch(1)
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.text.setText('Установка исполнительного устройства на привод стенда:\n' + \
                          'а) Установить на вал привода подходящую муфту (рис. 1)\n' + \
                          'б) Установить исполительное устройство и зафиксируйте его\n' + \
                          '   при помощи болтов (рис. 2)\n'
                          'в) Проверьте отчутствие перекосов при помощи поворота вала\n' + \
                          '   за шестерню. При необходимости устраните перекос (рис. 3)' + \
                          '\n\nНажать кнопку ПРИНЯТЬ для продолжения')
        self.text.setAlignment(QtCore.Qt.AlignTop)


class Form_iu_inst2(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()
        self.img = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap('exam_iu\\inst2.png')
        self.img.setScaledContents(True)
        self.pixmap.setDevicePixelRatio(1.05)
        self.img.setPixmap(self.pixmap)
        self.table = QtWidgets.QWidget()
        self.table.setLayout(self.hbox)
        self.hbox.addWidget(self.text)
        self.hbox.addSpacing(20)
        self.hbox.addWidget(self.img)
        self.hbox.addStretch(1)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.table)
        self.vbox.addStretch(1)
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setText('Установка датчика давления на исполнительное устройство:\n' + \
                          'а) Со стороны силового вала, противоположной стороне стрелочного\n' + \
                          '   указателя снимите кронштейн и выкрутите пробку\n   аккумулятора (рис. 4)\n' + \
                          'б) В отверстие аккумулятора ввинтите штуцер, а затем датчик давления.\n' + \
                          '   После чего подключите датчик к разъему шлейфа (рис. 5)\n'
                          'в) Второй конец шлейфа должен быть подключен к разъему\n' + \
                          '   ХР21 ДАТЧИК ДАВЛЕНИЯ (рис. 6)' + \
                          '\n\nНажать кнопку ПРИНЯТЬ для продолжения')
        self.text.setWordWrap(True)
        self.text.setAlignment(QtCore.Qt.AlignTop)


class Form_iu_inst3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()
        self.img = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap('exam_iu\\inst3.png')
        self.img.setScaledContents(True)
        # self.pixmap.setDevicePixelRatio(1.05)
        self.img.setPixmap(self.pixmap)
        self.table = QtWidgets.QWidget()
        self.table.setLayout(self.hbox)
        self.hbox.addWidget(self.text)
        self.hbox.addSpacing(20)
        self.hbox.addWidget(self.img)
        self.hbox.addStretch(1)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.table)
        self.vbox.addStretch(1)
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.text.setText('Установка датчика угла поворота на исполнительное устройство:\n' + \
                          'а) Снимете с силового вала рычаг, ослабив крепежный болт (рис. 7).\n' + \
                          'б) На кронштейне датчика угла поворота ослабьте барашки (рис.8)\n' + \
                          'в) Установите на вал исполнительного устройства резиновую муфту '
                          'и присоедините датчик угла поворота, по возможности соосно с валом (рис. 9). ' + \
                          'После чего зафиксируйте положение кронштейна затянув барашки.\n' + \
                          'г) Разъем датчика подключите к разъему привода ХР17 ДАТЧИК УГЛА' + \
                          '\n\nНажать кнопку ПРИНЯТЬ для продолжения')
        self.text.setAlignment(QtCore.Qt.AlignTop)


class Form_iu_inst4(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()
        self.img = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap('exam_iu\\inst4.png')
        self.img.setScaledContents(True)
        # self.pixmap.setDevicePixelRatio(1.05)
        self.img.setPixmap(self.pixmap)
        self.table = QtWidgets.QWidget()
        self.table.setLayout(self.hbox)
        self.hbox.addWidget(self.text)
        self.hbox.addSpacing(20)
        self.hbox.addWidget(self.img)
        self.hbox.addStretch(1)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.table)
        self.vbox.addStretch(1)
        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.text.setText('Подключение поворотного электромагнита и датчика положения:\n' + \
                          'а) Датчик положения подключается к разъему ХР9 ИУ ДП.\n' + \
                          'б) Поворотный электромагнит подключается к разъему XS10 ИУ ПЭ\n' + \
                          'при этом в зависимости от конструкции он либо подключается при помощи '
                          'шлейфа с разъемами (рис.12 и рис. 13) или при помощи шлейфа с зажимами (пара одноцветных х3 х4)' + \
                          '\n\nНажать кнопку ПРИНЯТЬ для продолжения')
        self.text.setAlignment(QtCore.Qt.AlignTop)


class Form_iu_pe_check(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()

        self.pa3 = ScaledDevice(width=380, height=320, arr_x=180, arr_y=155, arr_r=90, min_a=270,
                                max_a=-22.5, min_v=0, max_v=2.6, mark_prim=13, mark_sec=2, mark_ter=5,
                                f_mark='{: >.1f}', f_text='{:>5.3f} А')
        self.pa3.caption.setText('PA3')
        self.pa3.text.setAlignment(QtCore.Qt.AlignRight)
        self.pa3.setArrowVisible(True, False)

        self.tachometer = ScaledDevice(width=280, height=320, arr_x=250, arr_y=250, arr_r=180, min_a=180, max_a=90,
                                       min_v=0, max_v=600, mark_prim=6, mark_sec=2, mark_ter=5, f_mark='{:3.0f}',
                                       f_text='{:>3.0f} об/мин')
        self.tachometer.caption.setText('Тахометр')

        self.indicator = ScaledDevice(width=280, height=320, arr_x=130, arr_y=500, arr_r=350, arr_length=40, min_a=106,
                                      max_a=74, min_v=0, max_v=10, mark_prim=10, mark_sec=2, mark_ter=1,
                                      f_mark='{:.0f}', f_text='Позиция: {:>3.1f}')
        self.indicator.caption.setText('Указатель\nнагрузки')

        self.panel = QtWidgets.QWidget()

        self.hbox.addWidget(self.pa3)
        self.hbox.addWidget(self.tachometer)
        self.hbox.addWidget(self.indicator)
        self.panel.setLayout(self.hbox)

        self.vbox.addWidget(self.panel)
        self.vbox.addWidget(self.text)
        self.setLayout(self.vbox)

        self.panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.text.setText('Запуск вращения вала ИУ на скорости 500 об/мин\n')
        self.text.setAlignment(QtCore.Qt.AlignTop)


class Form_iu_dp_check(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()

        self.pa3 = ScaledDevice(width=200, height=250, arr_x=100, arr_y=115, arr_r=35, min_a=270,
                                max_a=-22.5, min_v=0, max_v=2.6, mark_prim=13, mark_sec=2, mark_ter=1,
                                f_mark='{: >.1f}', f_text='{:>5.3f} А')
        self.pa3.caption.setText('PA3')
        self.pa3.text.setAlignment(QtCore.Qt.AlignRight)
        self.pa3.setArrowVisible(True, False)
        self.pa3.setValue(0)

        self.tachometer = ScaledDevice(width=200, height=250, arr_x=180, arr_y=190, arr_r=100, min_a=180, max_a=90,
                                       min_v=0, max_v=600, mark_prim=6, mark_sec=5, mark_ter=1, f_mark='{:3.0f}',
                                       f_text='{:>3.0f} об/мин')
        self.tachometer.caption.setText('Тахометр')
        self.tachometer.setValue(0)

        self.indicator = ScaledDevice(width=230, height=250, arr_x=100, arr_y=410, arr_r=270, arr_length=40, min_a=106,
                                      max_a=74, min_v=0, max_v=10, mark_prim=10, mark_sec=2, mark_ter=1,
                                      f_mark='{:.0f}', f_text='Позиция: {: >4.1f}')
        self.indicator.caption.setText('Указатель\nнагрузки')
        self.indicator.setValue(0)

        self.dp = ScaledDevice(width=320, height=250, arr_x=160, arr_y=610, arr_r=470, arr_length=40, min_a=106,
                               max_a=74, min_v=14, max_v=26, mark_prim=6, mark_sec=2, mark_ter=5,
                               f_mark='{:.0f}', f_text='Частота: {: >6.3f} кГц')
        self.dp.caption.setText('Показания ДП')
        self.dp.setValue(0)

        self.panel = QtWidgets.QWidget()

        self.hbox.addWidget(self.pa3)
        self.hbox.addWidget(self.tachometer)
        self.hbox.addWidget(self.indicator)
        self.hbox.addWidget(self.dp)
        self.panel.setLayout(self.hbox)

        self.vbox.addWidget(self.panel)
        self.vbox.addWidget(self.text)
        self.setLayout(self.vbox)

        self.panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.text.setText('Запуск вращения вала ИУ на скорости 500 об/мин\n')
        self.text.setAlignment(QtCore.Qt.AlignTop)


class FormIUPressureCheck(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.text = QtWidgets.QLabel()
        settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        settings.setIniCodec('UTF-8')

        self.pressure = ScaledDevice(width=300, height=330, arr_x=150, arr_y=160, arr_r=70, min_a=270,
                                     max_a=-22.5, min_v=0, max_v=1.6, mark_prim=16, mark_sec=5, mark_ter=1,
                                     f_mark='{: >.1f}', f_text='{:>5.3f} МПа')
        self.pressure.caption.setText('Давление')
        self.pressure.text.setAlignment(QtCore.Qt.AlignRight)
        self.pressure.setArrowVisible(True, False)
        self.pressure.setValue(0)

        self.tachometer = ScaledDevice(width=330, height=330, arr_x=170, arr_y=250, arr_r=100, min_a=180, max_a=36,
                                       min_v=0, max_v=1600, mark_prim=8, mark_sec=2, mark_ter=5, f_mark='{:3.0f}',
                                       f_text='{:>3.0f} об/мин')
        self.tachometer.caption.setText('Тахометр')
        self.tachometer.setValue(0)

        self.timer = ScaledDevice(width=290, height=330, arr_x=145, arr_y=160, arr_r=60, min_a=90,
                                  max_a=-240, min_v=0, max_v=settings.value('progrev', 600, int), mark_prim=6, mark_sec=2, mark_ter=5,
                                  f_mark='{:.0f}', f_text='Осталось: {: >3.0f} сек')
        self.timer.caption.setText('Таймер')
        self.timer.setArrowVisible(True, False)
        self.timer.setValue(0)

        self.panel = QtWidgets.QWidget()

        self.hbox.addWidget(self.pressure)
        self.hbox.addWidget(self.tachometer)
        self.hbox.addWidget(self.timer)
        self.panel.setLayout(self.hbox)

        self.vbox.addWidget(self.panel)
        self.vbox.addWidget(self.text)
        self.setLayout(self.vbox)

        self.panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.text.setFont(QtGui.QFont('Segoi UI', 14))
        self.text.setWordWrap(True)
        self.text.setText('Запуск вращения вала ИУ на скорости 500 об/мин\n')
        self.text.setAlignment(QtCore.Qt.AlignTop)


class FormPrint(QtPrintSupport.QPrintPreviewWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.fitToWidth()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = FormIUPressureCheck()
    win.show()
    print(win.width(), win.height())
    app.exec_()
