import pygame

from engine.constants import BG_COLOR, TEXT_COLOR
from engine.btn.button import Button
from engine.scene import SceneBase
from scenes.HelpScene import HelpScene
from scenes.SignInScene import SignInScene
from scenes.TopicScene import TopicScene


class MenuScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.title_font = pygame.font.SysFont('arial', 90)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.start_btn = Button(self.window, (self.width//2 - self.btn_width/2, self.height//2, self.btn_width, self.btn_height), "New Story" )
        self.sign_in_btn = Button(self.window, (
        self.width // 2 - self.btn_width / 2, self.height // 2 + self.btn_height+20, self.btn_width, self.btn_height), "Sign In")
        self.help_btn = Button(self.window, (self.width // 2 - self.btn_width/2, self.height // 2 + 2*(self.btn_height+20), self.btn_width, self.btn_height),
                                "Help")


    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        self.window.screen.fill(BG_COLOR)

        self.show_text(self.title_font,"Welcome", (self.width // 2, (self.height // 2) - 100), TEXT_COLOR)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                def switch_topic():
                    self.Switch(TopicScene(self.window))
                def switch_sign_in():
                    self.Switch(SignInScene(self.window, self))
                def switch_help():
                    self.Switch(HelpScene(self.window, self))

                self.start_btn.on_click(switch_topic, mouse)
                self.sign_in_btn.on_click(switch_sign_in, mouse)
                self.help_btn.on_click(switch_help, mouse)

        self.start_btn.show()
        self.sign_in_btn.show()
        self.help_btn.show()
