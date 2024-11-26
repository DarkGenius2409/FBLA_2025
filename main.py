# imports
import pygame

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"
BG_COLOR = pygame.Color(0, 0, 0)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        screen.fill(BG_COLOR)

        pygame.display.flip()

        clock.tick(60)

pygame.quit()