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

        self.speak_start_time = None
        self.isSpeaking = False
        self.speak_duration = 0
        self.speak_text = ""
        self.isVisible = True
        self.isMoving = False
        self.direction = 1
        self.speech_max_width = 200

    def setDirection(self, direction):
        self.direction = direction

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + ' ', True, (0, 0, 0))
            word_width = word_surface.get_width()

            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def show(self):
        if not self.isVisible:
            return

        self.image = self.textures[self.window.animation_tick % len(self.textures)] if self.animated else self.image
        img = self.image
        if self.direction == -1:
            img = pygame.transform.flip(self.image, True, False)

        self.window.screen.blit(img, (self.rect.x, self.rect.y))

        # Show the speech bubble if speaking
        if self.isSpeaking:
            elapsed_time = pygame.time.get_ticks() - self.speak_start_time
            if elapsed_time < self.speak_duration:
                font = pygame.font.SysFont("Arial", 20)

                lines = self.wrap_text(self.speak_text, font, self.speech_max_width)
                line_height = font.get_linesize()
                total_height = line_height * len(lines)

                line_surfaces = [font.render(line, True, (0, 0, 0)) for line in lines]
                max_line_width = max(surface.get_width() for surface in line_surfaces)

                padding = 10
                bubble_width = max_line_width + padding * 2
                bubble_height = total_height + padding * 2

                if self.direction == 1:
                    bubble_x = self.rect.right + 5
                else:
                    bubble_x = self.rect.left - bubble_width - 5

                bubble_y = self.rect.top + 5
                bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
                pygame.draw.rect(self.window.screen, (255, 255, 255), bubble_rect)
                pygame.draw.rect(self.window.screen, (0, 0, 0), bubble_rect, 1)

                for i, surface in enumerate(line_surfaces):
                    text_y = bubble_y + padding + (i * line_height)
                    text_x = bubble_x + padding
                    self.window.screen.blit(surface, (text_x, text_y))
            else:
                self.isSpeaking = False
                if self.callback is not None:
                    self.callback()

    def setVisible(self, visible):
        self.isVisible = visible

    def speak(self, text, duration, callback=None):
        self.speak_text = text
        self.speak_duration = duration * 1000
        self.speak_start_time = pygame.time.get_ticks()
        self.isSpeaking = True
        self.callback = callback

    def move(self, vx, vy):
        self.isMoving = True
        self.rect.x += vx
        self.rect.y += vy


    def stopMoving(self):
        self.isMoving = False

    def move_to(self, x, y):
        self.rect.topleft = (x, y)


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
