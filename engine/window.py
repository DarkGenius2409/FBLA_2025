import uuid
import pygame
import cv2
import numpy as np
from moviepy import VideoFileClip

from cloud import supabase

# CONSTANTS
WIDTH = 1280
HEIGHT = 720
TITLE = "GenPlay"


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

    def start_recording(self, filename="output/output.mp4"):
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
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)# Convert to BGR

            try:
                self.video_writer.write(frame)
            except:
                print("bug")

    def export(self, name):
        self.stop_recording()
        video_storage_path = f"videos/{name}.mp4"
        thumbnail_storage_path = f"thumbnails/{name}.jpg"

        with VideoFileClip("./output/output.mp4") as clip:
            clip.save_frame("./output/thumbnail.jpg", t=1.0)
        with open('./output/output.mp4', 'rb') as f:
            response = supabase.storage.from_("exported_videos").upload(
                file=f,
                path=video_storage_path,
                file_options={"cache-control": "3600", "upsert": "false"},
            )
        with open('./output/thumbnail.jpg', 'rb') as f:
            response = supabase.storage.from_("exported_videos").upload(
                file=f,
                path=thumbnail_storage_path,
                file_options={"cache-control": "3600", "upsert": "false"},
            )
        user_email = supabase.auth.get_user().user.email
        story = {
            "name": name,
            "user": user_email,
            "video_path": video_storage_path,
            "thumbnail_path": thumbnail_storage_path
        }
        supabase.table("stories").insert(story).execute()


    def tick(self):
        self.clock.tick(self.fps)
        self.animation_tick += 1