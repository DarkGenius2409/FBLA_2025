# IMPORTS
import os
import random
import pygame
from scene import Scene1

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"

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

        def move(self, x, y, vx, vy):
                self.rect.x += vx
                self.rect.y += vy

        def update(self):
                pass

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True
tick = 0

test_textures = [
        pygame.image.load(os.path.join('test', 'sprite_00.png')),
        pygame.image.load(os.path.join('test', 'sprite_01.png')),
        pygame.image.load(os.path.join('test', 'sprite_02.png')),
        pygame.image.load(os.path.join('test', 'sprite_03.png')),
        pygame.image.load(os.path.join('test', 'sprite_04.png')),
        pygame.image.load(os.path.join('test', 'sprite_05.png')),
        pygame.image.load(os.path.join('test', 'sprite_06.png')),
        pygame.image.load(os.path.join('test', 'sprite_07.png')),
        pygame.image.load(os.path.join('test', 'sprite_08.png')),
        pygame.image.load(os.path.join('test', 'sprite_09.png')),
        pygame.image.load(os.path.join('test', 'sprite_10.png')),
        pygame.image.load(os.path.join('test', 'sprite_11.png')),
        pygame.image.load(os.path.join('test', 'sprite_12.png')),
        pygame.image.load(os.path.join('test', 'sprite_13.png')),
        pygame.image.load(os.path.join('test', 'sprite_14.png')),
        pygame.image.load(os.path.join('test', 'sprite_15.png'))
]

test_sprite = Sprite(test_textures, 100, 100)

#GAME LOOP
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

        dest_x = random.randint(0, WIDTH)
        dest_y = random.randint(0, HEIGHT)

        pygame.display.flip()
        clock.tick(60)
        tick += 1

pygame.quit()