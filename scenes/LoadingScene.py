import pygame
from engine.scene import SceneBase
from scenes.StoryScene import StoryScene

class LoadingScene(SceneBase):
    def __init__(self, window):
        super().__init__(window)
        self.font = pygame.font.SysFont('arial', 30)
        self.text = self.font.render('Loading....', True, (255, 255, 255))


    def UpdateLoading(self, story_result, events, keys):
        # Clear the screen with a black background
        self.window.screen.fill((0, 0, 0))

        text_rect = self.text.get_rect(center=(self.window.width // 2, self.window.height // 2))
        self.window.screen.blit(self.text, text_rect)

        # Check if story_result is available and switch to the StoryScene
        if story_result is not None:
            self.Switch(StoryScene(self.window, story_result))