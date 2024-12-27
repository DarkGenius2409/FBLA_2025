import threading
import pygame
from engine.ai import createStory
from engine.window import Window
from scenes.LoadingScene import LoadingScene

# PYGAME SETUP
pygame.init()
pygame.font.init()

# Game Global Variables
window = Window()
running = True
story_result = None

# Creating the story with AI
def fetch_story(prompt):
    global story_result
    story_result = createStory(prompt)

story_thread = threading.Thread(target=fetch_story, args=("FBI agent interrogates the prisoner",))
story_thread.start()

active_scene = LoadingScene(window)

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
    active_scene = active_scene.next

    pygame.display.flip()
    window.tick(60)

pygame.quit()
