# IMPORTS
import os
import random
import pygame

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"
BG_COLOR = pygame.Color(255, 0, 0)

# SPRITE CLASS
class Sprite(pygame.sprite.Sprite):
        def __init__(self, textures, width, height):
                self.textures = []
                for texture in textures:
                        scaled_texture = pygame.transform.smoothscale(texture, (width, height))
                        self.textures.append(scaled_texture)
                self.image = self.textures[0] 
                self.rect = self.image.get_rect()

        def show(self): 
                self.image=self.textures[tick%len(self.textures)]
                screen.blit(self.image, (self.rect.x, self.rect.y))

        def update(self):
                pass

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True
tick = 0

#GAME LOOP
while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        screen.fill(BG_COLOR)

        pygame.display.flip()

        clock.tick(60)
        tick += 1

pygame.quit()