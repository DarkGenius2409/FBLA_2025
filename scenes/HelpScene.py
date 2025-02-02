import pygame

from engine.constants import BG_COLOR, TEXT_COLOR
from engine.btn.button import Button, MenuButton
from engine.font import Fonts
from engine.scene import SceneBase

class HelpScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.back_btn = MenuButton(self.window, (self.width//2 - self.btn_width/2, self.height//2, self.btn_width, self.btn_height), "Back" )

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill(BG_COLOR)

        self.show_text(Fonts.TITLE.value,"Need Help?", (self.width // 2, (self.height // 2) - 100 ), (TEXT_COLOR))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_btn.on_click(self.SwitchBack, mouse)

        self.back_btn.show()