import pygame

from engine.sprite import loadCharacters, characters
from engine.window import Window
from scenes.LoadingScene import LoadingScene
from scenes.MenuScene import MenuScene

# PYGAME SETUP
pygame.init()
pygame.font.init()

# Game Global Variables
window = Window()
running = True
story_result = None

loadCharacters(window)
active_scene = MenuScene(window, None)
# archer = characters["archer"]

# GAME LOOP
while running:
    # Getting pressed keys and all events
    keys = pygame.key.get_pressed()
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        events.append(event)

    # Update current scene
    if isinstance(active_scene, LoadingScene):
        active_scene.UpdateLoading(story_result, events, keys)
    else:
        active_scene.Update(events, keys)

    # Update current scene; if no scene switch, then active_scene.next should be equal to active_scene
    if active_scene.next is not None:
        next_scene = active_scene.next
        active_scene.next = None
        active_scene = next_scene

    pygame.display.flip()
    window.tick(60)

pygame.quit()
