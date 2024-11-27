import os
from operator import truediv

import pygame

class Sprite:
    def __init__(self, textures, animated, width, height, window):
        self.animated = animated
        if self.animated:
            self.textures = []
            for texture in textures:
                scaled_texture = pygame.transform.smoothscale(texture, (width, height))
                self.textures.append(scaled_texture)
            self.image = self.textures[0]
        else:
            self.image=pygame.transform.smoothscale(textures, (width, height))

        self.rect = self.image.get_rect()
        self.window = window

    def show(self):
        self.image = self.textures[self.window.animation_tick % len(self.textures)] if self.animated else self.image
        self.window.screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, vx, vy):
        self.rect.x += vx
        self.rect.y += vy

    def move_to(self, x, y):
        self.rect = self.rect.move(x, y)

    def rot(self, angle):
        og_rect = self.rect
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.rect.move(og_rect.x, og_rect.y)

    def scale(self, w, h):
        self.image = pygame.transform.smoothscale(self.image, (w, h))
        self.rect = self.rect.inflate(w, h)

    def check_window_col(self):
        if self.rect.x + self.rect.w > self.window.width or self.rect.x < 0:
            if self.rect.y + self.rect.h > self.window.height or self.rect.y < 0:
                return True, True
            else:
                return True, False
        elif self.rect.y + self.rect.h > self.window.height or self.rect.y < 0:
            return False, True
        else:
            return False, False

    def update(self, events, keys):
        pass

class TestSprite1(Sprite):
    def __init__(self, window, v):
        test_texture2 = pygame.image.load(os.path.join('test2.png'))
        super().__init__(test_texture2, False, 100, 100, window)
        self.vx = v
        self.vy = v

    def update(self, events, keys):
        window_col = self.check_window_col()
        if window_col[0]:
            self.vx *= -1
        if window_col[1]:
            self.vy *= -1
        self.move(self.vx, self.vy)
        self.show()

class TestSprite2(Sprite):
    def __init__(self, window, vx, vy):
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
        super().__init__(test_textures, True, 200, 200, window)
        self.rect = self.rect.move(self.window.width/2, self.window.height/2)
        self.vx = vx
        self.vy = vy

    def update(self, events, keys):
        if keys[pygame.K_RIGHT]:
            self.move(self.vx, 0)
        if keys[pygame.K_LEFT]:
            self.move(-self.vx, 0)
        if keys[pygame.K_UP]:
            self.move(0, -self.vy)
        if keys[pygame.K_DOWN]:
            self.move(0, self.vy)
        self.show()