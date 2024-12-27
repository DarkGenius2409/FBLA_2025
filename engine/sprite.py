import pygame

class Sprite:
    def __init__(self, textures, animated, width, height, window):
        self.callback = None
        self.animated = animated
        if self.animated:
            self.textures = []
            for texture in textures:
                scaled_texture = pygame.transform.smoothscale(texture, (width, height))
                self.textures.append(scaled_texture)
            self.image = self.textures[0]
        else:
            self.image = pygame.transform.smoothscale(textures, (width, height))

        self.rect = self.image.get_rect()
        self.window = window

        self.isSpeaking = False
        self.speak_start_time = None
        self.speak_duration = 0
        self.speak_text = ""

    def show(self):
        self.image = self.textures[self.window.animation_tick % len(self.textures)] if self.animated else self.image
        self.window.screen.blit(self.image, (self.rect.x, self.rect.y))

        # Show the speech bubble if speaking
        if self.isSpeaking:
            elapsed_time = pygame.time.get_ticks() - self.speak_start_time
            if elapsed_time < self.speak_duration:
                font = pygame.font.SysFont("Arial", 20)
                text_surface = font.render(self.speak_text, True, (0, 0, 0))

                text_rect = pygame.Rect(self.rect.right, self.rect.top + 5, text_surface.get_width() + 10,
                                        text_surface.get_height() + 10)

                text_surface_rect = text_surface.get_rect(center=text_rect.center)

                pygame.draw.rect(self.window.screen, (255, 255, 255), text_rect)
                self.window.screen.blit(text_surface, text_surface_rect)
            else:
                self.isSpeaking = False

                if not (self.callback is None):
                    self.callback()

    def speak(self, text, duration, callback=None):
        self.speak_text = text
        self.speak_duration = duration * 1000
        self.speak_start_time = pygame.time.get_ticks()
        self.isSpeaking = True
        self.callback = callback

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
