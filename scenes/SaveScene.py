import os

import pygame

from engine.btn.button import Button
from engine.constants import BG_COLOR, TEXT_COLOR
from engine.font import Fonts
from engine.scene import SceneBase
from engine.text_input import TextInput


class SaveScene(SceneBase):
    def __init__(self, window, exported_story=None):
        super().__init__(window)
        self.exported_story = exported_story
        self.font = pygame.font.SysFont("Arial", 20)
        self.storyName = TextInput(self.window, (self.window.width//2-50, self.window.height//2, 100, 50), "Name Your Story")

        rect = (self.window.width/2-150,self.window.height/2-50, 300, 100)

        self.saveBtn = Button(self.window, rect, "Export story!")


    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()
        self.window.screen.fill(BG_COLOR)
        self.saveBtn.show()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.saveBtn.on_click(self.window.export, mouse)