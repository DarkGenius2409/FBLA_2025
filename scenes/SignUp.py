from typing import get_origin

import gotrue.errors
import pygame

from cloud import supabase
from engine.constants import BG_COLOR, TEXT_COLOR, DANGER_COLOR
from engine.btn.button import Button
from engine.font import Fonts
from engine.scene import SceneBase
from engine.text_input import TextInput

class SignUpScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.title_font = Fonts.WELCOME.value
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.email = TextInput(self.window, (self.window.width // 2 - 150, self.window.height // 2 - 50, 300, 50), "Username")
        self.password = TextInput(self.window, (self.window.width//2-150, self.window.height//2 + 20, 300, 50), "Password")
        self.sign_in_btn = Button(self.window, (
            self.width // 2 - self.btn_width / 2, self.height // 2 + 140, self.btn_width, self.btn_height), "Create Account")
        self.back_btn = Button(self.window, (
        self.width // 2 - self.btn_width / 2, self.height // 2 + 210, self.btn_width, self.btn_height),
                               "Back")
        self.error_message = ""

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def sign_in(self):
        for char in "#$%^&*":
            if char in self.password.text:
                self.error_message = "Invalid character in password"
                return
        supabase.auth.sign_up(
            {"email": self.email.text, "password": self.password.text}
        )
        self.SwitchBack()

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill(BG_COLOR)

        self.show_text(self.title_font,"Create Account", (self.width // 2, (self.height // 2) - 150 ), TEXT_COLOR)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_btn.on_click(self.SwitchBack, mouse)
                self.sign_in_btn.on_click(self.sign_in, mouse)
            self.email.update(event)
            self.password.update(event)

        self.show_text(Fonts.SPEECH_TEXT.value, self.error_message, (self.width / 2, self.height - 50), DANGER_COLOR)
        self.email.show()
        self.password.show()
        self.sign_in_btn.show()
        self.back_btn.show()