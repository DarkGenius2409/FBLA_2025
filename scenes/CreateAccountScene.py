import pygame

from engine.colors import BG_COLOR, TEXT_COLOR
from engine.btn.button import Button
from engine.scene import SceneBase


class CreateAccountScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.title_font = pygame.font.SysFont('arial', 90)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50

        self.sign_in_btn = Button(self.window, (
        self.width // 2 - self.btn_width / 2, self.height // 2, self.btn_width, self.btn_height), "Create Account")
        self.back_btn = Button(self.window, (self.width//2 - self.btn_width/2, self.height//2 + self.btn_height+20, self.btn_width, self.btn_height), "Back" )

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill((BG_COLOR))

        self.show_text(self.title_font,"Create Account", (self.width // 2, (self.height // 2) - 100 ), (TEXT_COLOR))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_btn.on_click(self.SwitchBack, mouse)

        self.back_btn.show()