import pygame


# Base class for scenes
class SceneBase:
    def __init__(self, window, prev=None):
        # next scene to show; until scene switch is needed, the next scene is the same as the current
        self.next = self
        self.window = window
        self.prev = prev

    # Update method, takes in events, pressed keys, and the screen texture from main loop
    def Update(self, events, keys):
        pass

    # Switches to next scene
    def Switch(self, next_scene):
        self.next = next_scene

    def SwitchBack(self):
        self.Switch(self.prev)

