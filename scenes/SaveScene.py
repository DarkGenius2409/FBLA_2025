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
        self.saveBtn = Button(self.window, (self.window.width//2-50, self.window.height//2+70, 75, 50), "Save")

    def save_story(self):
        os.system(f"compile.bat {self.storyName.text}")

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        self.window.screen.fill(BG_COLOR)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.saveBtn.on_click(self.save_story, mouse)

        text_surface = Fonts.TITLE.value.render("THE END", True, TEXT_COLOR)
        text_rect = pygame.Rect(0, 0, self.window.width, self.window.height-100)
        text_surface_rect = text_surface.get_rect(center=text_rect.center)
        self.window.screen.blit(text_surface, text_surface_rect)

        self.storyName.show()
