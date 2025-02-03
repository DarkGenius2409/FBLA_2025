import pygame

from engine.btn.button import Button
from engine.btn.button_obj import ButtonObj


class CardGrid:
    def __init__(self, window, rect, dimensions, spacing, funcs, texts):
        self.window =window
        self.x = rect[0]
        self.y = rect[1]
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.spacing_x = spacing[0]
        self.spacing_y = spacing[1]
        self.btn_w = (rect[2]-self.cols*self.spacing_x)/self.cols
        self.btn_h = (rect[3]-self.rows*self.spacing_y)/self.rows
        self.funcs = funcs
        self.texts = texts

        self.buttons = []

        btn_y = self.y
        for i in range(self.rows):
            btn_x = self.x
            for j in range(self.cols):
                btn = Button(self.window, (btn_x, btn_y, self.btn_w, self.btn_h), self.texts[i*self.cols+j])
                self.buttons.append(ButtonObj(btn, self.funcs[i] if isinstance(self.funcs, list) else self.funcs, self.texts[i]))
                btn_x += self.btn_w + self.spacing_x
            btn_y += self.btn_h + self.spacing_y


    def show(self):
        for btn in self.buttons:
            btn.show()

