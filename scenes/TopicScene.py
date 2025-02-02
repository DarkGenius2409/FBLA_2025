import threading
import pygame
from pygame import Rect

from engine.ai.generate import createTopics
from engine.btn.button import Button
from engine.btn.button_grid import ButtonGrid
from engine.colors import BG_COLOR, TEXT_COLOR
from engine.font import Fonts
from engine.scene import SceneBase
from scenes.StoryScene import StoryScene


class TopicScene(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.title_font = Fonts.TITLE.value
        self.width = self.window.width
        self.height = self.window.height

        self.topic_result = None
        self.topics_thread = threading.Thread(target=self.getTopics)
        self.topics_thread.start()
        self.topics = self.getTopics()

        self.btn_grid_rect = Rect(0, 0, self.width - 150, self.height / 2)
        self.btn_grid_rect.center = (self.width // 2, self.height // 2 + 75)
        self.btn_height = 50
        self.btn_spacing_x = 20
        self.btn_spacing_y = 20

        def switch(t):
            self.Switch(StoryScene(self.window, prev=self, topic=t))

        self.btn_grid = ButtonGrid(self.window, self.btn_grid_rect, (2, 2), (self.btn_spacing_y, self.btn_spacing_y),
                                   switch, self.topics)



    def getTopics(self):
        self.topic_result = createTopics()
        topics = []

        if self.topic_result:
            # i = 0
            for topic in self.topic_result["topics"]:
                # rect = pygame.Rect(0, 0, self.btn_width, self.btn_height)
                # rect.center = (self.window.width / 2, self.window.height / 2 + (self.btn_height + 10) * i)
                #
                # button = Button(self.window, rect, topic)  # Pass rect directly
                #
                # def switch(t):
                #     self.Switch(StoryScene(self.window, prev=self, topic=t))
                #
                # self.buttons.append({"button":button, "func":switch, "topic":topic})
                # i += 1
                topics.append(topic)

        return topics

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()
        self.window.screen.fill(BG_COLOR)

        # Display the title
        self.show_text(self.title_font, "Which topic do you want?", (self.width // 2, (self.height // 2) - 200),
                       TEXT_COLOR)

        if self.topic_result is None:
            self.show_text(self.title_font, "...", (self.width // 2, (self.height // 2) ),
                           TEXT_COLOR)
        else:
            self.btn_grid.show()

        # Handle button click events
        for event in events:
                for obj in self.btn_grid.buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        obj.btn.on_click(lambda: obj.func(obj.text), mouse)


