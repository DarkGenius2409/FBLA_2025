import pygame

from engine.button import Button
from engine.scene import SceneBase
from scenes.TopicScene import TopicScene


class MenuScene(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.title_font = pygame.font.SysFont('arial', 90)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.start_btn = Button(self.window, (self.width//2, self.height//2, self.btn_width, self.btn_height), "New Story" )


    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill((0,0,0))

        self.show_text(self.title_font,"Welcome", (self.width // 2, (self.height // 2) - 100 ), (255,255,255))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                def switch():
                    self.Switch(TopicScene(self.window))

                self.start_btn.on_click(switch, mouse)

        self.start_btn.show()
