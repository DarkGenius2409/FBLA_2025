import pygame

# Base class for scenes
class SceneBase:
    def __init__(self):
        # next scene to show; until scene switch is needed, the next scene is the same as the current
        self.next = self

    # Update method, takes in events, pressed keys, and the screen texture from main loop
    def Update(self, events, keys, screen):
        pass

    # Switches to next scene
    def Switch(self, next_scene):
        self.next = next_scene

# Testing scenes; basically they switch to each other when the enter key is being held down
class Scene1(SceneBase):
    def Update(self, events, keys, screen):
        screen.fill((255,0,0))

        if keys[pygame.K_RETURN]:
            self.Switch(Scene2())

class Scene2(SceneBase):
    def Update(self, events, keys, screen):
        screen.fill((0,255,0))

        if keys[pygame.K_RETURN]:
            self.Switch(Scene1())