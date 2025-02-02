import pygame
import cv2
import numpy as np

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "FBLA 2025"


class Window:
    def __init__(self, width=WIDTH, height=HEIGHT, title=TITLE, fps=60):
        pygame.init()  # Ensure pygame is initialized

        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = False
        self.recording = False
        self.fps = fps

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.animation_tick = 0

        self.video_writer = None

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen  # Toggle state

        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self.toggle_fullscreen()

        elif event.type == pygame.VIDEORESIZE:  # Handle window resize
            if not self.fullscreen:  # Only allow resizing in windowed mode
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        elif event.type == pygame.WINDOWMAXIMIZED:
            if not self.fullscreen:  # Maximize only in windowed mode
                self.width, self.height = pygame.display.get_window_size()
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def start_recording(self, filename="output.mp4"):
        if not self.recording:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
            self.video_writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))
            self.recording = True

    def stop_recording(self):
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        self.recording = False

    def update_recording(self):
        if self.recording and self.video_writer:
            frame = pygame.surfarray.array3d(self.screen)
            frame = np.rot90(frame, k=-1)  # Rotate to match OpenCV format
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR
            self.video_writer.write(frame)

    def export(self):
        self.stop_recording()

    def tick(self):
        self.clock.tick(self.fps)
        self.animation_tick += 1