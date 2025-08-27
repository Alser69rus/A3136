from PyQt5 import QtCore, QtWidgets
from menu.template import Menu
from menu.btn import Btn
import exam_bu.exam_bu_prog


class CheckBU(Menu):
    btn_back = QtCore.pyqtSignal()
    btn_ok = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__('Проверка блока управления', parent, col=2)
        self.dev_type = ''

        self.btn_prepare = Btn('Подготовка')
        self.btn_di = Btn('Проверка дискретных входов')
        self.btn_fi = Btn('Проверка частотных входов')
        self.btn_shim = Btn('Проверка ШИМ силового канала')
        self.btn_ai = Btn('Проверка аналоговых входов')
        self.btn_rt = Btn('Проверка канала температуры масла')

        self.btn_prepare_r = Btn('Подготовка к проверке рез. каналов')
        self.btn_di_r = Btn('Проверка рез. канала дискретных входов')
        self.btn_fi_r = Btn('Проверка резервного канала ДЧД')
        self.btn_shim_r = Btn('Проверка резервного канала ШИМ')

        self.btn_protocol = Btn('Завершение испытаний')

        lst = [self.btn_prepare, self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai, self.btn_rt,
               self.btn_prepare_r, self.btn_di_r, self.btn_fi_r, self.btn_shim_r, self.btn_protocol]
        self.set_lst(lst)

        self.btn_protocol.clicked.connect(self.btn_back)

    def reset(self):
        exam_bu.exam_bu_prog.bu = exam_bu.exam_bu_prog.BU(dev_type=self.dev_type)
        self.set_btn_visible()
        super().reset()


    def set_btn_visible(self):
        vis = []

        if self.dev_type == 'ЭРЧМ30Т3-06':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai, self.btn_rt,
                   self.btn_prepare_r, self.btn_di_r, self.btn_fi_r, self.btn_shim_r]
        elif self.dev_type == 'ЭРЧМ30Т3-07':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai, self.btn_rt]
        elif self.dev_type == 'ЭРЧМ30Т3-04':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai, self.btn_rt]
        elif self.dev_type == 'ЭРЧМ30Т3-08':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-08-01':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-02':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-05':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-10':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-10-01':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-12':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-12-01':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-12-02':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т3-12-03':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т4-01':
            vis = [self.btn_di, self.btn_fi, self.btn_shim]
        elif self.dev_type == 'ЭРЧМ30Т4-02':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т4-02-01':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т4-02-02':
            vis = [self.btn_di, self.btn_fi, self.btn_shim, self.btn_ai]
        elif self.dev_type == 'ЭРЧМ30Т4-03':
            vis = [self.btn_di, self.btn_fi, self.btn_shim]

        vis += [self.btn_protocol, self.btn_prepare]

        for elem in self.list:
            if elem != self.btn_protocol and elem != self.btn_prepare:
                elem.setEnabled(False)
            if elem in vis:
                elem.setVisible(True)
            else:
                elem.setVisible(False)
