import os

import pygame

from engine.btn.button import Button
from engine.constants import BG_COLOR, TEXT_COLOR
from engine.font import Fonts
from engine.scene import SceneBase
from engine.text_input import TextInput
# from scenes.MenuScene import MenuScene


class SaveScene(SceneBase):
    def __init__(self, window, exported_story=None):
        super().__init__(window)
        self.exported_story = exported_story
        self.storyName = TextInput(self.window, (self.window.width//2-150, self.window.height//2-150, 300, 50), "Name Your Story")

        rect = (self.window.width/2-150,self.window.height/2-50, 300, 100)
        homeRect = (self.window.width / 2 - 150, self.window.height / 2 + 75, 300, 100)

        self.saveBtn = Button(self.window, rect, "Export story!")
        self.homeBtn = Button(self.window, homeRect, "Back to Home")

    def save(self):
        if self.storyName.text.strip() != "":
            self.window.export(self.storyName.text)
            self.window.fetched_stories = False

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()
        self.window.screen.fill(BG_COLOR)

        self.storyName.show()

        self.saveBtn.show()
        self.homeBtn.show()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.saveBtn.on_click(self.save, mouse)
                self.homeBtn.on_click(lambda: self.Switch(self.window.home), mouse)

            self.storyName.update(event)