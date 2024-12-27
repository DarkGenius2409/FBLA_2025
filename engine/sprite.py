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
