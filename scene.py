import pygame

from sprite import TestSprite1, TestSprite2


# Base class for scenes
class SceneBase:
    def __init__(self, window):
        # next scene to show; until scene switch is needed, the next scene is the same as the current
        self.next = self
        self.window = window

    # Update method, takes in events, pressed keys, and the screen texture from main loop
    def Update(self, events, keys):
        pass

    # Switches to next scene
    def Switch(self, next_scene):
        self.next = next_scene

# Testing scenes; basically they switch to each other when the enter key is being held down
class Scene1(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.test_sprite = TestSprite2(self.window, 10, 10)

    def Update(self, events, keys):
        self.window.screen.fill((255,0,0))
        self.test_sprite.update(events, keys)

        if keys[pygame.K_RETURN]:
            self.Switch(Scene2(self.window))

class Scene2(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.test_sprite = TestSprite1(self.window, 5)
    def Update(self, events, keys):
        self.window.screen.fill((0,255,0))
        self.test_sprite.update(events, keys)

        if keys[pygame.K_RETURN]:
            self.Switch(Scene1(self.window))

