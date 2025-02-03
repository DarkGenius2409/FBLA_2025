import pygame


# Base class for scenes
class SceneBase:
    def __init__(self, window, prev=None):
        # next scene to show; until scene switch is needed, the next scene is the same as the current
        self.next = None
        self.window = window
        self.prev = prev

    # Update method, takes in events, pressed keys, and the screen texture from main loop
    def Update(self, events, keys):
        pass

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    # Switches to next scene
    def Switch(self, next_scene):
        self.prev = self
        self.next = next_scene

    def SwitchBack(self):
        self.Switch(self.prev)

