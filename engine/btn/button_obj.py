class ButtonObj:
    def __init__(self, btn, func, text=None):
        self.btn = btn
        self.func = func
        self.text = text

    def show(self):
        self.btn.show()