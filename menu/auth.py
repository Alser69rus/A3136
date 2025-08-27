from PyQt5 import QtCore, QtWidgets, QtGui
from menu.template import Menu
from menu.btn import Btn
from menu.keypad import Keypad


class Auth(Menu):
    btn_back = QtCore.pyqtSignal(bool)
    btn_ok = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__('Данные испытания', parent, col=2)
        # self.vbox.setColumnMinimumWidth(0, 450)
        # self.vbox.setColumnMinimumWidth(1, 450)
        self.num = ''
        self.date = ''
        self.locomotive = ''
        self.section = ''
        self.name1 = ''
        self.name2 = ''

        self.btn_num = Btn('Заводской номер:')
        self.btn_date = Btn('Дата изготовления:')
        self.btn_locomotive = Btn('Номер тепловоза:')
        self.btn_section = Btn('Секция:')
        self.btn_name1 = Btn('Оператор:')
        self.btn_name2 = Btn('Проверяющий:')

        self.btn_iu_ok = Btn('Приступить к проверке')
        self.btn_iu_back = Btn('Назад')

        self.set_lst(
            [self.btn_num, self.btn_date, self.btn_locomotive, self.btn_section, self.btn_name1, self.btn_name2,
             self.btn_iu_ok, self.btn_iu_back])
        for item in [self.btn_num, self.btn_date, self.btn_locomotive, self.btn_section, self.btn_name1,
                     self.btn_name2]:
            item.clicked.connect(self.on_select)

        self.btn_iu_back.clicked.connect(self.btn_back)
        self.btn_iu_ok.clicked.connect(self.btn_ok)

    @QtCore.pyqtSlot()
    def reset(self):
        super().reset()
        self.num = ''
        self.date = ''
        self.locomotive = ''
        self.section = ''
        self.btn_iu_ok.setEnabled(False)
        self.setText()

    @QtCore.pyqtSlot()
    def setText(self):
        self.btn_num.setText('Заводской номер: {}'.format(self.num))
        self.btn_date.setText('Дата изготовления: {}'.format(self.date))
        self.btn_locomotive.setText('Номер тепловоза: {}'.format(self.locomotive))
        self.btn_section.setText('Секция: {}'.format(self.section))
        self.btn_name1.setText('Оператор: {}'.format(self.name1))
        self.btn_name2.setText('Проверяющий: {}'.format(self.name2))
        if all([self.num, self.date, self.locomotive, self.section, self.name1, self.name2]):
            self.btn_iu_ok.setEnabled(True)
        else:
            self.btn_iu_ok.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_select(self):
        sender = self.sender()
        with open('Сотрудники.txt', 'r', encoding='utf-8') as f:
            operators = f.read().split()
        # settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        # settings.setIniCodec('UTF-8')
        # operators = settings.value('employees')

        dialog = QtWidgets.QInputDialog(self)
        keypad = Keypad()
        dialog.setFont(QtGui.QFont('Segoi Ui', 16))

        if sender == self.btn_name1:
            dialog.setComboBoxItems(operators)
            dialog.setComboBoxEditable(True)
        if sender == self.btn_name2:
            dialog.setComboBoxItems(operators)
            dialog.setComboBoxEditable(True)

        if sender is self.btn_num:
            keypad.setText(self.num)
            result = keypad.exec()
        if sender is self.btn_date:
            keypad.setText(self.date)
            result = keypad.exec()
        if sender is self.btn_locomotive:
            keypad.setText(self.locomotive)
            result = keypad.exec()
        if sender is self.btn_section:
            keypad.setText(self.section)
            result = keypad.exec()
        if sender is self.btn_name1:
            result = dialog.exec()
        if sender is self.btn_name2:
            result = dialog.exec()

        # keypad.setText()

        if result == QtWidgets.QDialog.Accepted:
            if sender is self.btn_num:
                self.num = keypad.textValue()
            if sender is self.btn_date:
                self.date = keypad.textValue()
            if sender is self.btn_locomotive:
                self.locomotive = keypad.textValue()
            if sender is self.btn_section:
                self.section = keypad.textValue()
            if sender is self.btn_name1:
                self.name1 = dialog.textValue()
            if sender is self.btn_name2:
                self.name2 = dialog.textValue()

        self.setText()
