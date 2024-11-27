# imports
import pygame
from scene import Scene1

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True

# scenes
active_scene = Scene1()

while running:
        # getting pressed keys and all events
        keys = pygame.key.get_pressed()
        events = []
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                events.append(event)

        # Updating current scene with events, pressed keys, and scenes
        active_scene.Update(events, keys, screen)

        # Updating current scene; if no scene switch, then active_scene.next should be equal to active scene
        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(60)

pygame.quit()