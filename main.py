# IMPORTS
import os
import random
import pygame
from scene import Scene1
from window import Window

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"

# PYGAME SETUP
pygame.init()
window = Window(WIDTH, HEIGHT, TITLE)
running = True

# GAME LOOP
# scenes
active_scene = Scene1(window)

while running:
        # getting pressed keys and all events
        keys = pygame.key.get_pressed()
        events = []
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                events.append(event)

        # Updating current scene with events, pressed keys, and scenes
        active_scene.Update(events, keys)

        # Updating current scene; if no scene switch, then active_scene.next should be equal to active scene
        active_scene = active_scene.next

        dest_x = random.randint(0, WIDTH)
        dest_y = random.randint(0, HEIGHT)

        pygame.display.flip()
        window.clock.tick(60)
        window.animation_tick += 1

pygame.quit()