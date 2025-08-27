try:
    from . import template, btn
except Exception:
    import aseMenu, btn


class mnuIU(template.Menu):
    def __init__(self, parent=None):
        super().__init__('Регулировка исполнительного устройства', parent)

        self.btn_iu_pe_tune = btn.Btn('Регулировка поворотного электромагнита')
        self.btn_iu_dp_tune = btn.Btn('Регулировка датчика положения')
        self.btn_iu_back = btn.Btn('Назад')

        self.set_lst([self.btn_iu_pe_tune, self.btn_iu_dp_tune, self.btn_iu_back])
