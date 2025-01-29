import pygame

characters = {}


class Sprite:
    def __init__(self, spritesheets, frame_width, frame_height, window):
        self.speak_complete_callback = None
        self.animations = {}
        self.current_animation = None
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.window = window
        self.rect = pygame.Rect(
            0, 0, frame_width , frame_height
        )
        self.isSpeaking = False
        self.speech_end_time = 0
        self.speech_text = None
        self.speech_font = pygame.font.SysFont("Arial", 24)
        self.speech_color = (255, 255, 255)
        self.speech_bg_color = (0, 0, 0)
        self.visible = True
        self.direction = 1  # 1 for normal, -1 for flipped
        self.up = 5

        for name in spritesheets.keys():
            self.load_animation(spritesheets[name]["file"], frame_width, frame_height, name, spritesheets[name]["speed"])

        if self.animations:
            self.switch_animation(
                next(iter(self.animations))
            )  # Default to the first animation

    def setVisible(self, visible):
        self.visible = visible

    def load_animation(self, spritesheet_path, frame_width, frame_height, name, speed):
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        animation = []
        for y in range(0, spritesheet.get_height(), frame_height):
            for x in range(0, spritesheet.get_width(), frame_width):
                frame = spritesheet.subsurface(
                    pygame.Rect(x, y, frame_width, frame_height)
                )
                scaled_frame = pygame.transform.scale(
                    frame, (frame_width * 5, frame_height * 5)
                )
                animation.append(scaled_frame)
        self.animations[name] = {"animation":animation, "speed":speed}

    def switch_animation(self, animation_name):
        if (animation_name in self.animations) and not (
            animation_name == self.current_animation
        ):
            self.current_animation = animation_name
            self.current_frame = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.animations[self.current_animation]["speed"]:
            self.last_frame_time = current_time
            self.current_frame = (self.current_frame + 1) % len(
                self.animations[self.current_animation]["animation"]
            )

            print(self.current_frame)

        self.show()

        if self.isSpeaking:
            self.update_speech()

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + " ", True, (0, 0, 0))
            word_width = word_surface.get_width()

            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def show(self):
        if not self.visible:
            return

        if self.current_animation:
            frame = self.animations[self.current_animation]["animation"][self.current_frame]
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            self.window.screen.blit(frame, self.rect.topleft)

        if self.isSpeaking:
            font = pygame.font.SysFont("Arial", 20)

            lines = self.wrap_text(self.speech_text, font, 200)
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
            if self.speak_complete_callback is not None:
                self.speak_complete_callback()

    def move(self, vx, vy):
        self.rect.x += vx
        self.rect.y += 1 * self.up
        self.up = -self.up

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
        x_collision = (
            self.rect.x + self.rect.width > self.window.width or self.rect.x < 0
        )
        y_collision = (
            self.rect.y + self.rect.height > self.window.height or self.rect.y < 0
        )
        return x_collision, y_collision

    def scale(self, w, h):
        self.rect = self.rect.inflate(w - self.rect.width, h - self.rect.height)
        for animation_name, frames in self.animations.items():
            self.animations[animation_name] = [
                pygame.transform.scale(frame, (w, h)) for frame in frames
            ]

    def rot(self, angle):
        for animation_name, frames in self.animations.items():
            self.animations[animation_name] = [
                pygame.transform.rotate(frame, angle) for frame in frames
            ]


def loadCharacters(window):
    archer = Sprite(
        {
            "idle": {"file":"assets/archer/archer-idle.png", "speed":100},
            "walk": {"file":"assets/archer/archer-walk.png", "speed":150}
        },
        100,
        100,
        window,
    )
    archer.switch_animation("idle")

    soldier = Sprite(
        {
            "idle": {"file":"assets/soldier/soldier-idle.png", "speed":100},
            "walk": {"file":"assets/soldier/soldier-walk.png", "speed":150}
        },
        100,
        100,
        window,
    )
    soldier.switch_animation("idle")

    characters["soldier"] = soldier
    characters["archer"] = archer
