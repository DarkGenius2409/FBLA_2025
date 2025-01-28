import pygame

characters = {}

class Sprite:
    def __init__(self, spritesheets, frame_width, frame_height, window):
        self.speak_complete_callback = None
        self.animations = {}
        self.current_animation = None
        self.current_frame = 0
        self.animation_speed = 200  # Time per frame in milliseconds
        self.last_frame_time = pygame.time.get_ticks()
        self.window = window
        self.rect = pygame.Rect(0, 0, frame_width * 5, frame_height * 5)  # Adjust rect size to 5x scale
        self.isSpeaking = False
        self.speech_end_time = 0
        self.speech_text = None
        self.speech_font = pygame.font.SysFont("Arial", 24)
        self.speech_color = (255, 255, 255)
        self.speech_bg_color = (0, 0, 0)
        self.visible = True
        self.direction = 1  # 1 for normal, -1 for flipped

        for name, spritesheet_path in spritesheets.items():
            self.load_animation(spritesheet_path, frame_width, frame_height, name)

        if self.animations:
            self.switch_animation(next(iter(self.animations)))  # Default to the first animation

    def setVisible(self, visible):
        self.visible = visible

    def load_animation(self, spritesheet_path, frame_width, frame_height, name):
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        animation = []
        for y in range(0, spritesheet.get_height(), frame_height):
            for x in range(0, spritesheet.get_width(), frame_width):
                frame = spritesheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                scaled_frame = pygame.transform.scale(frame, (frame_width * 5, frame_height * 5))
                animation.append(scaled_frame)
        self.animations[name] = animation

    def switch_animation(self, animation_name):
        if (animation_name in self.animations) and not (animation_name == self.current_animation):
            self.current_animation = animation_name
            self.current_frame = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.animation_speed:
            self.last_frame_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])

        self.show()

        if self.isSpeaking:
            self.update_speech()

    def show(self):
        if not self.visible:
            return

        if self.current_animation:
            frame = self.animations[self.current_animation][self.current_frame]
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            self.window.screen.blit(frame, self.rect.topleft)

        if self.isSpeaking and self.speech_text:
            text_surface = self.speech_font.render(self.speech_text, True, self.speech_color)
            text_rect = text_surface.get_rect()
            text_rect.midbottom = self.rect.midtop
            pygame.draw.rect(
                self.window.screen,
                self.speech_bg_color,
                text_rect.inflate(10, 10),
                border_radius=5
            )
            self.window.screen.blit(text_surface, text_rect)
        else:
                self.isSpeaking = False
                if self.speak_complete_callback is not None:
                    self.speak_complete_callback()
    def move(self, vx, vy):
        self.rect.x += vx
        self.rect.y += vy

    def move_to(self, x, y):
        self.rect.topleft = (x, y)

    def setDirection(self, direction):
        self.direction = direction

    def speak(self, text, duration, on_complete=None):
        self.isSpeaking = True
        self.speech_text = text
        self.speech_end_time = pygame.time.get_ticks() + (duration * 1000)
        self.speak_complete_callback = on_complete

    def update_speech(self):
        if self.isSpeaking and pygame.time.get_ticks() > self.speech_end_time:
            self.isSpeaking = False
            self.speech_text = None
            if self.speak_complete_callback:
                self.speak_complete_callback()
                self.speak_complete_callback = None

    def check_window_col(self):
        x_collision = self.rect.x + self.rect.width > self.window.width or self.rect.x < 0
        y_collision = self.rect.y + self.rect.height > self.window.height or self.rect.y < 0
        return x_collision, y_collision

    def scale(self, w, h):
        self.rect = self.rect.inflate(w - self.rect.width, h - self.rect.height)
        for animation_name, frames in self.animations.items():
            self.animations[animation_name] = [pygame.transform.scale(frame, (w, h)) for frame in frames]

    def rot(self, angle):
        for animation_name, frames in self.animations.items():
            self.animations[animation_name] = [pygame.transform.rotate(frame, angle) for frame in frames]


def loadCharacters(window):
    archer = Sprite({
        "idle": "assets/archer/archer-idle.png",
        "walk": "assets/archer/archer-walk.png"
    }, 100, 100, window)
    archer.switch_animation("idle")

    soldier = Sprite({
        "idle": "assets/soldier/soldier-idle.png",
        "walk": "assets/soldier/soldier-walk.png"
    }, 100, 100, window)
    soldier.switch_animation("idle")

    characters["soldier"] = soldier
    characters["archer"] = archer
