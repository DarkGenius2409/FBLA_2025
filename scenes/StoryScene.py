import threading
import pygame
import random
from pygame import Rect
from engine.ai.generate import createStory
from engine.btn.button import Button, MenuButton
from engine.btn.button_grid import ButtonGrid
from engine.constants import BG_COLOR, TEXT_COLOR
from engine.font import Fonts
from engine.scene import SceneBase
from engine.sprite import characters
from scenes.SaveScene import SaveScene


class StoryScene(SceneBase):
    totalScenes = 0
    totalSummary = []
    def __init__(self, window, topic, end=False, prev=None):
        super().__init__(window, prev)
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
        self.failed = False
        self.back_btn = MenuButton(self.window, (self.window.width/2-50,self.window.height/2-25+100,100,50), "Back" )
        self.background = None

        story_thread = threading.Thread(target=self.getStory)
        story_thread.start()


    def setBackground(self):
        scene = self.getCurrentScene()
        self.background = pygame.transform.scale(pygame.image.load(f"assets/backdrops/{scene["backdrop"]}.png"), (self.window.width, self.window.height))

    # Creating the story with AI
    def getStory(self):
        try:
            self.failed = False
            self.story = createStory(self.topic, self.endStory)
            self.setupActiveScene()
            self.window.start_recording()
            self.setBackground()
        except Exception as e:
            print(e)
            self.failed = True

    def getCurrentAction(self):
        return self.story["scenes"][self.currentScene]["actions"][self.actionIndex]

    def getCurrentScene(self):
        if self.currentScene > len(self.story["scenes"]) - 1:
            self.end = True

            end = False
            if StoryScene.totalScenes > 2:
                end = random.choice([True, False])

            StoryScene.totalSummary.append(self.story["summary"])
            self.Switch(ChoiceScene(self.window, "\nAfter,".join(StoryScene.totalSummary), self.story["question"], end, prev=self))
            self.window.stop_recording()
            self.background = None
            StoryScene.totalScenes += 1

            return None
        return self.story["scenes"][self.currentScene]

    def setupActiveScene(self):
        scene = self.getCurrentScene()

        if scene is None:
            return


        pygame.mixer.music.stop()
        pygame.mixer.music.load(f"assets/music/{scene["music"]}.mp3")
        pygame.mixer.music.play()

        for character in self.characters.values():
            character.visible = False


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
            character.move_to(x, 0)
            character.rect.bottom = self.window.height + 50

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
        self.Show()

        if  self.failed:
            mouse = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.back_btn.on_click(self.SwitchBack, mouse)


    def Show(self):
        self.window.screen.fill(BG_COLOR)

        if self.background is not None:
            self.window.screen.blit(self.background, (0,0))

        if self.story is None:
            if self.failed:
                self.show_text(Fonts.TITLE.value, "An error occurred!", (self.window.width // 2, (self.window.height // 2)),
                               (255, 0, 0))
                self.back_btn.show()
            else:
                self.show_text(Fonts.TITLE.value, "Loading...", (self.window.width // 2, (self.window.height // 2)),
                               TEXT_COLOR)

            return


        if self.end:
            self.Switch(SaveScene(self.window))
        else:
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
    def __init__(self, window, previousTopic, question, end=False, prev=None):
        super().__init__(window, prev)
        self.title_font = Fonts.TITLE.value
        self.width = self.window.width
        self.height = self.window.height

        self.question = question
        self.end = end

        self.btn_grid_rect = Rect(0, 0, self.width-20, self.height/2)
        self.btn_grid_rect.center = (self.width//2, self.height//2+45)
        self.btn_height = 50
        self.btn_spacing_x = 20
        self.btn_spacing_y = 20

        rect = pygame.Rect(0, 0, 300, 100)
        rect.center = (self.window.width/2, 0)
        rect.bottom = self.window.height - 20
        self.exitButton = Button(self.window, rect, "Exit!", variant="destructive")
        self.background = pygame.image.load("assets/menu_background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.window.width, self.window.height))
        self.background.set_alpha(55)

        def switch(ans):
            self.Switch(StoryScene(self.window, end=self.end,  prev=self, topic=f"So far, this has already happened: {previousTopic} Now, {ans}"))
        self.btn_grid = ButtonGrid(self.window, self.btn_grid_rect, (2,2), (self.btn_spacing_y, self.btn_spacing_y), switch, self.question)


    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()
        self.window.screen.fill(BG_COLOR)
        self.window.screen.blit( self.background, (0,0))

        # Display the title
        self.show_text(self.title_font, "What should happen next?", (self.width // 2, (self.height // 2) - 200),
                       TEXT_COLOR)

        self.btn_grid.show()
        self.exitButton.show()
        # Handle button click events
        for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for obj in self.btn_grid.buttons:
                        obj.btn.on_click(lambda: obj.func(obj.text), mouse)

                    def saveScreen():
                        self.Switch(SaveScene(self.window))
                    self.exitButton.on_click(saveScreen, mouse )