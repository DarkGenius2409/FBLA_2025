import pygame

from engine.constants import TEXT_COLOR, BG_COLOR
from engine.scene import SceneBase
from scenes.StoryScene import StoryScene

class HelpScene(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.font = pygame.font.SysFont('arial', 30)
        self.text = self.font.render('Help', True, (TEXT_COLOR))


    def UpdateLoading(self, story_result, events, keys):
        # Clear the screen with a black background
        self.window.screen.fill((BG_COLOR))

        text_rect = self.text.get_rect(center=(self.window.width // 2, self.window.height // 2))
        self.window.screen.blit(self.text, text_rect)

        # Check if story_result is available and switch to the StoryScene
        if story_result is not None:
            self.Switch(StoryScene(self.window, story_result))