try:
    from . import template, btn
except Exception:
    import aseMenu, btn


class MainMenu(template.Menu):
    def __init__(self, parent=None):
        super().__init__('Главное меню', parent)
        self.btnBU = btn.Btn('Проверка блока управления при помощи программатора')
        self.btnBUTune = btn.Btn('Регулировка блока управления')
        self.btnIU = btn.Btn('Проверка исполнительного устройства')
        self.btnIUTune = btn.Btn('Регулировка исполнительного устройства')
        self.btnBP = btn.Btn('Проверка блока питания')
        self.btnQuit = btn.Btn('Выход')

        self.set_lst([self.btnBU,self.btnBUTune, self.btnIU,self.btnIUTune,self.btnBP, self.btnQuit])
