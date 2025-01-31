import threading
import pygame
import random
from engine.ai.generate import createStory
from engine.button import Button
from engine.constants import BG_COLOR, TEXT_COLOR
from engine.scene import SceneBase
from engine.sprite import characters
from scenes.SaveScene import SaveScene


class StoryScene(SceneBase):
    totalScenes = 0
    totalSummary = []
    def __init__(self, window, topic, end=False):
        super().__init__(window)
        self.topic = topic
        self.story = None
        self.endStory = end

        # Create character instances dynamically
        self.characters = {}
        for char_name in characters.keys():
            self.characters[char_name] = characters[char_name]

        self.end = False
        self.currentScene = 0
        self.actionIndex = 0
        self.arial = pygame.font.SysFont('arial', 50)

        story_thread = threading.Thread(target=self.getStory)
        story_thread.start()


    # Creating the story with AI
    def getStory(self):
        self.story = createStory(self.topic, self.endStory)
        self.setupActiveScene()

    def getCurrentAction(self):
        return self.story["scenes"][self.currentScene]["actions"][self.actionIndex]

    def getCurrentScene(self):
        if self.currentScene > len(self.story["scenes"]) - 1:
            self.end = True

            end = False
            if StoryScene.totalScenes > 2:
                end = random.choice([True, False])

            StoryScene.totalSummary.append(self.story["summary"])
            self.Switch(ChoiceScene(self.window, "\nAfter,".join(StoryScene.totalSummary), self.story["question"], end))
            StoryScene.totalScenes += 1

            return None
        return self.story["scenes"][self.currentScene]

    def setupActiveScene(self):
        scene = self.getCurrentScene()

        if scene is None:
            return

        for character in self.characters.values():
            character.visible = False

        # Position visible characters
        y = self.window.height / 2

        for character_name in scene["characters"]:
            character = self.characters[character_name]
            index = list(self.characters.keys()).index(character_name)
            spacing = 20

            if index % 2 == 0:
                x = spacing  * (index + 1)
                character.setDirection(1)
            else:
                x = self.window.width - character.rect.width - ( spacing * (index + 1))
                character.setDirection(-1)

            character.visible = True
            character.move_to(x, y)

    def nextAction(self):
        self.actionIndex += 1

        if self.actionIndex > len(self.getCurrentScene()["actions"]) - 1:
            self.actionIndex = 0
            self.currentScene += 1
            self.setupActiveScene()

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        self.window.screen.fill((BG_COLOR))

        if self.story is None:
            self.show_text(self.arial, "Loading...", (self.window.width // 2, (self.window.height // 2) ), (255, 255, 255))
            return

        font = pygame.font.SysFont("Arial", 20)

        if self.end:
            self.Switch(SaveScene(self.window))
            # text_surface = font.render("THE END", True, (TEXT_COLOR))
            # text_rect = pygame.Rect(0, 0, self.window.width, self.window.height)
            # text_surface_rect = text_surface.get_rect(center=text_rect.center)
            # self.window.screen.blit(text_surface, text_surface_rect)
        else:
            backdrop = self.getCurrentScene()["backdrop"]
            text_surface = font.render(f"Scene {self.currentScene+1} - {backdrop}", True, (TEXT_COLOR))
            text_rect = pygame.Rect(0, 0, self.window.width, 40)
            text_surface_rect = text_surface.get_rect(center=text_rect.center)
            self.window.screen.blit(text_surface, text_surface_rect)

            action = self.getCurrentAction()
            inActiveCharacters = list(self.characters.values())
            character = self.characters[action["character"]]
            inActiveCharacters.remove(character)

            if action["actionType"] == "speak":
                character.switch_animation("idle")

                if not character.isSpeaking:
                    character.speak(action["target"], 5, self.nextAction)
            elif action["actionType"] == "move":
                target_char = self.characters[action["target"]]
                character.switch_animation("walk")

                dx = target_char.rect.x - character.rect.x
                if abs(dx) > 300:
                    dx = 1 if dx > 0 else (-1 if dx < 0 else 0)
                    character.move(dx*5, 0)
                else:
                    character.switch_animation("idle")
                    self.nextAction()

            elif action["actionType"] == "leave":
                character.setDirection(1)
                character.move(5, 0)
                character.switch_animation("walk")

                if character.rect.x > self.window.width+100:
                    self.nextAction()

            for c in inActiveCharacters:
                c.switch_animation("idle")

            for character in self.characters.values():
                character.update()



class ChoiceScene(SceneBase):
    def __init__(self, window, previousTopic, question, end=False):
        super().__init__(window)
        self.title_font = pygame.font.SysFont('arial', 50)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = self.window.width-20
        self.btn_height = 50
        self.btn_spacing = 20
        self.question = question
        self.end = end

        self.buttons = []

        i = 0
        for answer in self.question:
            rect = pygame.Rect(0, 0, self.btn_width, self.btn_height)
            rect.center = (self.window.width / 2, self.window.height / 2 + (self.btn_height + 10) * i)

            button = Button(self.window, rect, answer)

            def switch(ans):
                self.Switch(StoryScene(self.window, end=self.end, topic=f"So far, this has already happened: {previousTopic} Now, {ans}"))

            self.buttons.append({"button": button, "func": switch, "answer": answer})
            i += 1


    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()
        self.window.screen.fill((0, 0, 0))

        # Display the title
        self.show_text(self.title_font, "What should happen next?", (self.width // 2, (self.height // 2) - 200), (TEXT_COLOR))

        for obj in self.buttons:
            obj["button"].show()
        # Handle button click events
        for event in events:
                for obj in self.buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        obj["button"].on_click(lambda: obj["func"](obj["answer"]), mouse)