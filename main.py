import pygame

# Importing necessary modules from the project
from cloud import supabase  # Cloud database connection (Supabase)
from engine.sprite import loadCharacters, characters  # Character sprite loading
from engine.window import Window  # Game window setup
from scenes.MenuScene import MenuScene  # Main menu scene

# PYGAME SETUP
pygame.init()  # Initialize pygame
pygame.font.init()  # Initialize font module
pygame.mixer.init()  # Initialize sound mixer for audio handling

# Game Global Variables
window = Window(fps=120)  # Create the game window
active_scene = MenuScene(window, None)  # Set the initial scene to MenuScene
window.home = active_scene  # Store the home scene reference
loadCharacters(window)  # Load character sprites into the game

running = True  # Game loop control variable

# GAME LOOP
while running:
    # Getting pressed keys and all events
    keys = pygame.key.get_pressed()  # Get the current state of all keys
    events = []  # List to store events

    for event in pygame.event.get():  # Process all events in the event queue
        if event.type == pygame.QUIT:  # Check if the user wants to quit
            running = False  # Exit the game loop

        window.handle_event(event)  # Pass event handling to the window
        events.append(event)  # Store event for later use

    # Update the current scene with the collected events and key states
    active_scene.Update(events, keys)

    # Handle scene switching; if next scene is set, transition to it
    if active_scene.next is not None:
        next_scene = active_scene.next  # Store reference to the next scene
        active_scene.next = None  # Reset next scene reference
        active_scene = next_scene  # Switch to the new scene

    pygame.display.flip()  # Refresh the screen to display updates
    window.update_recording()  # Update any screen recording (if implemented)
    window.tick()  # Maintain consistent frame rate

pygame.quit()  # Quit pygame and clean up resources