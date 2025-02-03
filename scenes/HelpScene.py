import pygame

from engine.ai.generate import askQuestion
from engine.constants import BG_COLOR, TEXT_COLOR, TITLE_COLOR
from engine.btn.button import MenuButton
from engine.font import Fonts
from engine.scene import SceneBase
from engine.text_input import TextInput


class HelpScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.back_btn = MenuButton(self.window, (
        self.width // 2 - self.btn_width / 2, (self.height -self.btn_height-20), self.btn_width, self.btn_height), "Back")

        self.messages = []
        self.messageInput = TextInput(self.window, (self.window.width//2-200, (self.height -self.btn_height-120), 300, 50), "Write here..")

        self.send = MenuButton(self.window, (self.window.width//2+125, (self.height -self.btn_height-120), 100, 50),
                                   "Send")

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def show_msg(self, text, pos, sent=True):
        text_object = Fonts.SPEECH_TEXT.value.render(text, True, (255,255,255))
        text_rect = text_object.get_rect(center=pos)
        other = text_rect.copy()
        other.width = 800
        other.height=100
        other.center = pos

        color = (0,200,0)
        if not sent:
            color = "#8532a8"

        pygame.draw.rect(self.window.screen, color, other, border_radius=15)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill(BG_COLOR)
        y = (self.height // 2-50)
        i = 0

        for msg in self.messages:
            self.show_msg(msg["message"], (self.width // 2, y + 110*i), sent=msg["sent"])
            i+=1

        self.show_text(Fonts.WELCOME.value, "Need Help?", (self.width // 2, (self.height // 2) - 220), TEXT_COLOR)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_btn.on_click(self.SwitchBack, mouse)

                def sendMsg():
                    self.messages = []
                    text = askQuestion(self.messageInput.text)
                    self.messages = [{"message":self.messageInput.text, "sent":True}, {"message":text, "sent":False}]
                    self.messageInput.text = ""
                self.send.on_click(sendMsg, mouse)

            self.messageInput.update(event)

        self.send.show()
        self.back_btn.show()
        self.messageInput.show()
