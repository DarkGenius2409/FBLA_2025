import pygame

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"

class Window:
    def __init__(self, width=WIDTH, height=HEIGHT, title=TITLE):
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.animation_tick = 0

    def tick(self, framerate):
        self.clock.tick(framerate)
        self.animation_tick += 1