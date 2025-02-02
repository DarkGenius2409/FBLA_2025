import os

import pygame

from engine.sprite import loadCharacters, characters
from engine.window import Window
from scenes.MenuScene import MenuScene

# PYGAME SETUP
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Game Global Variables
window = Window()
active_scene = MenuScene(window, None)
loadCharacters(window)


running = True

# GAME LOOP
while running:
    # Getting pressed keys and all events
    keys = pygame.key.get_pressed()
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        window.handle_event(event)
        events.append(event)

    # Update current scene
    active_scene.Update(events, keys)

    # Update current scene; if no scene switch, then active_scene.next should be equal to active_scene
    if active_scene.next is not None:
        next_scene = active_scene.next
        active_scene.next = None
        active_scene = next_scene


    pygame.display.flip()
    window.update_recording()
    window.tick()

pygame.quit()
