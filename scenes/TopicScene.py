import threading
import pygame
from engine.ai import createTopics
from engine.button import Button
from engine.scene import SceneBase
from scenes.StoryScene import StoryScene


class TopicScene(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.title_font = pygame.font.SysFont('arial', 50)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = self.window.width-20
        self.btn_height = 50
        self.btn_spacing = 20  # Space between buttons

        # Calculate positions for buttons
        self.buttons = []

        self.topic_result = None
        self.topics_thread = threading.Thread(target=self.getTopics)
        self.topics_thread.start()

    def getTopics(self):
        self.topic_result = createTopics()

        if self.topic_result:
            i = 0
            for topic in self.topic_result["topics"]:
                rect = pygame.Rect(0, 0, self.btn_width, self.btn_height)
                rect.center = (self.window.width / 2, self.window.height / 2 + (self.btn_height + 10) * i)

                button = Button(self.window, rect, topic)  # Pass rect directly

                def switch(t):
                    self.Switch(StoryScene(self.window, topic=t))

                self.buttons.append({"button":button, "func":switch, "topic":topic})
                i += 1

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()
        self.window.screen.fill((0, 0, 0))

        # Display the title
        self.show_text(self.title_font, "Which topic do you want?", (self.width // 2, (self.height // 2) - 200), (255, 255, 255))

        if self.topic_result == None:
            self.show_text(self.title_font, "...", (self.width // 2, (self.height // 2) ),
                           (255, 255, 255))
        else:
            for obj in self.buttons:
                obj["button"].show()

        # Handle button click events
        for event in events:
                for obj in self.buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        obj["button"].on_click(lambda: obj["func"](obj["topic"]), mouse)


