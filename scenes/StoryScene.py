import pygame
from sqlalchemy import false

from engine.scene import SceneBase
from engine.sprite import Sprite

characters = {
    "fbi-agent": {
        "sprite": "assets/fbi.png",
    },
    "prisoner": {
        "sprite": "assets/prisoner.png",
    }
}


class Character(Sprite):
    def __init__(self, characterName, window):
        self.characterName = characterName
        texture = pygame.image.load(characters[self.characterName]["sprite"])
        super().__init__(texture, False, 250, 250, window)


class StoryScene(SceneBase):
    def __init__(self, window, story):
        super().__init__(window)
        self.story = story

        # Create character instances dynamically
        self.characters = {}
        for char_name in characters.keys():
            self.characters[char_name] = Character(char_name, self.window)

        self.end = False
        self.currentScene = 0
        self.actionIndex = 0

        self.setupActiveScene()

    def getCurrentAction(self):
        return self.story["scenes"][self.currentScene]["actions"][self.actionIndex]

    def getCurrentScene(self):
        if self.currentScene > len(self.story["scenes"]) - 1:
            self.end = True
            return None
        return self.story["scenes"][self.currentScene]

    def setupActiveScene(self):
        scene = self.getCurrentScene()

        if scene is None:
            return

        for character in self.characters.values():
            character.setVisible(False)

        # Position visible characters
        y = self.window.height / 2

        for character_name in scene["characters"]:
            character = self.characters[character_name]
            index = list(self.characters.keys()).index(character_name)

            if index % 2 == 0:
                x = 20
                character.setDirection(1)
            else:
                x = self.window.width - (200 * (index + 1))
                character.setDirection(-1)

            character.setVisible(True)
            character.move_to(x, y)

    def nextAction(self):
        self.actionIndex += 1

        if self.actionIndex > len(self.getCurrentScene()["actions"]) - 1:
            self.actionIndex = 0
            self.currentScene += 1
            self.setupActiveScene()

    def Update(self, events, keys):
        self.window.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 20)

        if self.end:
            text_surface = font.render("THE END", True, (255, 255, 255))
            text_rect = pygame.Rect(0, 0, self.window.width, self.window.height)
            text_surface_rect = text_surface.get_rect(center=text_rect.center)
            self.window.screen.blit(text_surface, text_surface_rect)
        else:
            text_surface = font.render(f"Scene {self.currentScene+1} - {self.getCurrentScene()["backdrop"]}", True, (255, 255, 255))
            text_rect = pygame.Rect(0, 0, self.window.width, 40)
            text_surface_rect = text_surface.get_rect(center=text_rect.center)
            self.window.screen.blit(text_surface, text_surface_rect)

            action = self.getCurrentAction()
            character = self.characters[action["character"]]

            if action["actionType"] == "speak":
                if not character.isSpeaking:
                    character.speak(action["target"], 5, self.nextAction)
            elif action["actionType"] == "move":
                target_char = self.characters[action["target"]]

                dx = target_char.rect.x - character.rect.x
                dy = target_char.rect.y - character.rect.y

                if abs(dx) > 500 or abs(dy) > 10:
                    dx = 1 if dx > 0 else (-1 if dx < 0 else 0)

                    dy = 1 if dy > 0 else (-1 if dy < 0 else 0)

                    character.move(dx*5, dy*5)
                else:
                    character.stopMoving()
                    self.nextAction()
            elif action["actionType"] == "leave":
                character.setDirection(1)
                character.move(5, 0)

                if character.rect.x > self.window.width+100:
                    self.nextAction()

            # Show all characters
            for character in self.characters.values():
                character.show()