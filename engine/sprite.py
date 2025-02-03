import threading

import pygame
import pyttsx3
from engine.font import Fonts

engine = pyttsx3.init()
characters = {}

class Sprite:
    def __init__(self, spritesheets, scale, window):
        self.speak_complete_callback = None
        self.animations = {}
        self.current_animation = list(spritesheets.keys())[0]
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.window = window
        self.isSpeaking = False
        self.speech_end_time = 0
        self.speech_text = None
        self.speech_font = pygame.font.SysFont("Arial", 24)
        self.speech_color = (255, 255, 255)
        self.speech_bg_color = (0, 0, 0)
        self.visible = True
        self.direction = 1
        self.rect = None
        self.scale = scale

        for name in spritesheets.keys():
            sheet = spritesheets[name]
            self.load_animation(sheet["file"], sheet["frames"], name, sheet["speed"])


    def load_animation(self, path, frames, name, speed):
        animation = []
        for x in range(frames):
            frame = pygame.image.load(path + f"/{x}.png")
            frame = pygame.transform.scale(frame, (self.scale*frame.get_width(),self.scale*frame.get_height()))

            if self.rect is None:
                self.rect = pygame.rect.Rect(0, 0, frame.get_width(), frame.get_height())

            animation.append(frame)

        self.animations[name] = {"animation": animation, "speed": speed}

    def switch_animation(self, animation_name):
        if (animation_name in self.animations) and not (
            animation_name == self.current_animation
        ):
            self.current_animation = animation_name
            self.current_frame = 0

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines


    def draw_speech_bubble(self):
        font = Fonts.SPEECH_TEXT.value
        padding = (20, 20)


        # Render text lines
        lines = self.wrap_text(self.speech_text, font, 200)
        line_surfaces = [font.render(line, True, (0, 0, 0)) for line in lines]

        # Calculate speech bubble dimensions
        text_width = max(surface.get_width() for surface in line_surfaces)
        text_height = sum(surface.get_height() for surface in line_surfaces)
        bubble_width = text_width + padding[0] * 2
        bubble_height = text_height + padding[1] * 2

        bubble_x = self.rect.x
        bubble_y = self.rect.top - bubble_height - 10

        # Ensure bubble is within screen bounds
        bubble_x = max(10, min(bubble_x, self.window.width - bubble_width - 10))
        bubble_y = max(10, bubble_y)

        # Colors
        bubble_color = (255, 255, 255)
        border_color = (0, 0, 0)

        # Draw speech bubble rectangle
        pygame.draw.rect(self.window.screen, bubble_color, (bubble_x, bubble_y, bubble_width, bubble_height),
                         border_radius=10)
        pygame.draw.rect(self.window.screen, border_color, (bubble_x, bubble_y, bubble_width, bubble_height), 2,
                         border_radius=10)

        tail_points = [
            (bubble_x + bubble_width // 2 - 10, bubble_y + bubble_height),  # Bottom middle
            (bubble_x + bubble_width // 2 + 10, bubble_y + bubble_height),  # Bottom middle-right
            (bubble_x + bubble_width // 2, bubble_y + bubble_height + 15)  # Bottom tip
        ]
        pygame.draw.polygon(self.window.screen, bubble_color, tail_points)
        pygame.draw.polygon(self.window.screen, border_color, tail_points, 2)

        # Draw text inside the bubble
        for i, surface in enumerate(line_surfaces):
            text_x = bubble_x + padding[0]
            text_y = bubble_y + padding[1] + (i * surface.get_height())
            self.window.screen.blit(surface, (text_x, text_y))

    def update(self):
        self.show()

    def show(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.animations[self.current_animation]["speed"]:
            self.last_frame_time = current_time
            self.current_frame = (self.current_frame + 1) % len(
                self.animations[self.current_animation]["animation"]
            )

        if not self.visible:
            return

        if self.current_animation:
            frame = self.animations[self.current_animation]["animation"][self.current_frame]
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            self.window.screen.blit(frame, self.rect)

            # hitbox
            # pygame.draw.rect(self.window.screen, (255,0,0), self.rect,
            #                  border_radius=10)

        if self.isSpeaking and self.speech_text:
           self.draw_speech_bubble()

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
        self.speak_complete_callback = on_complete
        engine.say(text)


        engine.runAndWait()

        def end(_, completed):
            if completed:
                self.isSpeaking = False
                self.speech_text = None
                if self.speak_complete_callback:
                    self.speak_complete_callback()
                    self.speak_complete_callback = None

        engine.connect('finished-utterance', end)

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


def loadCharacters(window):
    characters["archer"]  = Sprite(
        {
            "idle": {"file":"assets/archer/idle", "speed":150, "frames":5},
            "walk": {"file":"assets/archer/walk", "speed":100, "frames":7},
        },
        7,
        window,
    )

    characters["soldier"] = Sprite(
        {
            "idle": {"file":"assets/soldier/idle", "speed":100, "frames":5},
            "walk": {"file":"assets/soldier/walk", "speed":50, "frames":5},
        },
        7,
        window,
    )
