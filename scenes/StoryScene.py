import pygame
from engine.scene import SceneBase
from engine.sprite import Sprite

characters = {
    "fbi-agent":{"sprite":"assets/fbi.png"},
    "prisoner": {"sprite": "assets/prisoner.png"},
}

class Character(Sprite):
    def __init__(self, characterName, window):
        test_texture2 = pygame.image.load(characters[characterName]["sprite"])
        super().__init__(test_texture2, False, 250, 250, window)


class StoryScene(SceneBase):
    def __init__(self, window, story, signed_in):
        super().__init__(window)
        self.story = story
        self.signed_in = signed_in

        self.fbiAgent = Character("fbi-agent", self.window)
        self.prisoner = Character("prisoner", self.window)
        self.prisoner.move_to(0, 320)

        self.actionIndex = 0

    def getCurrentAction(self):
        if self.actionIndex >= len(self.story["actions"]):
            return self.story["actions"][len(self.story["actions"])-1]
        else:
            return self.story["actions"][self.actionIndex]

    def nextScene(self):
        self.actionIndex += 1

    def Update(self, events, keys):
        self.window.screen.fill((0,0,0))

        action = self.getCurrentAction()
        if action["actionType"] == "speak":
            if action["character"] == "fbi-agent" and not self.fbiAgent.isSpeaking:
                self.fbiAgent.speak(action["target"], 3, self.nextScene)
            if action["character"] == "prisoner" and not self.prisoner.isSpeaking:
                self.prisoner.speak(action["target"], 3, self.nextScene)
        else:
            self.nextScene()

        self.fbiAgent.show()
        self.prisoner.show()

