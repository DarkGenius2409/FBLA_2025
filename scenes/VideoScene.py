import math

import pygame
from pygame import Rect

from engine.btn.button import MenuButton
from engine.constants import BG_COLOR, WIDTH, HEIGHT, TEXT_COLOR
from engine.font import Fonts
from engine.scene import SceneBase
from pyvidplayer2 import Video


class VideoScene(SceneBase):
    def __init__(self, window, prev, video, name):
        super().__init__(window, prev)
        self.video_rect = Rect(0,0, math.floor(WIDTH*0.5), math.floor(HEIGHT*0.5))
        self.video_rect.centerx = self.window.width/2
        self.video_rect.centery = self.window.height/2
        self.video = Video(video)
        self.video.resize((math.floor(WIDTH*0.5), math.floor(HEIGHT*0.5)))
        self.name = name
        self.back_btn = MenuButton(self.window, (
            self.window.width // 2 - 100, (self.window.height // 2) + 220, 200, 50), "Back")

    def Update(self, events, keys):
        self.window.screen.fill(BG_COLOR)
        mouse = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.video_rect.collidepoint(mouse):
                    self.video.toggle_pause()
                self.back_btn.on_click(self.SwitchBack, mouse)

        self.show_text(Fonts.WELCOME.value, self.name, (self.window.width // 2, (self.window.height // 2) - 220), TEXT_COLOR)
        self.video.draw(self.window.screen, (self.video_rect.x, self.video_rect.y))
        self.back_btn.show()