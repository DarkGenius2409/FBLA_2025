import pygame

from engine.Card import Card
from engine.btn.button import Button
from engine.btn.button_obj import ButtonObj


class CardGrid:
    def __init__(self, window, rect, dimensions, spacing, imgs, videos, names):
        self.window =window
        self.x = rect[0]
        self.y = rect[1]
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.spacing_x = spacing[0]
        self.spacing_y = spacing[1]
        self.btn_w = (rect[2]-self.cols*self.spacing_x)/self.cols
        self.btn_h = (rect[3]-self.rows*self.spacing_y)/self.rows
        self.imgs = imgs
        self.videos = videos
        self.names = names

        self.cards = []

        btn_y = self.y
        for i in range(self.rows):
            btn_x = self.x
            for j in range(self.cols):
                btn = Card(self.window, (btn_x, btn_y, self.btn_w, self.btn_h), self.imgs[i*self.cols+j], self.videos[i*self.cols+j], self.names[i*self.cols+j])
                self.cards.append(btn)
                btn_x += self.btn_w + self.spacing_x
            btn_y += self.btn_h + self.spacing_y

    def show(self):
        for card in self.cards:
            card.show()

