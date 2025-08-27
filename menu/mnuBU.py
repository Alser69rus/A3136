from menu.template import Menu
from menu.btn import Btn


class MnuBU(Menu):
    def __init__(self, parent=None):
        super().__init__('Регулировка блока управления', parent)

        self.btn_bu_ai_tune = Btn('Настройка АВХ1 - ДДН и АВХ2 - ДДМ')
        self.btn_bu_ai_3_tune = Btn('Настройка АВХ3 - датчик температуры масла\n'
                                    '(ЭРЧМ30Т3-04, ЭРЧМ30Т3-06, ЭРЧМ30Т3-07)')
        self.btn_bu_dp = Btn('Согласование датчика положения')

        self.btn_bu_back = Btn('Назад')

        self.set_lst([self.btn_bu_ai_tune, self.btn_bu_ai_3_tune,self.btn_bu_dp, self.btn_bu_back,])
