import pygame

from cloud import supabase
from engine.constants import BG_COLOR, TEXT_COLOR, TITLE_COLOR
from engine.btn.button import Button, MenuButton
from engine.font import Fonts
from engine.scene import SceneBase
from scenes.HelpScene import HelpScene
from scenes.LibraryScene import LibraryScene
from scenes.SignInScene import SignInScene
from scenes.TopicScene import TopicScene


class MenuScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.signed_in = False
        self.fetched_stories = False
        self.thumbnail_paths = []
        self.video_paths = []
        self.names = []
        self.start_btn = MenuButton(self.window, (self.width//2 - self.btn_width/2, self.height//2, self.btn_width, self.btn_height), "New Story" )
        self.sign_in_btn = MenuButton(self.window, (
            self.width // 2 - self.btn_width / 2, self.height // 2 + self.btn_height+20, self.btn_width, self.btn_height), "Sign In")
        self.sign_out_btn = MenuButton(self.window, (
            self.width // 2 - self.btn_width / 2, self.height // 2 + self.btn_height + 20, self.btn_width,
            self.btn_height), "Sign Out")
        self.help_btn = MenuButton(self.window, (self.width // 2 - self.btn_width/2, self.height // 2 + 2*(self.btn_height+20), self.btn_width, self.btn_height),
                                "Help")
        self.library_btn = MenuButton(self.window, (
        self.width // 2 - self.btn_width / 2, self.height // 2 + 3 * (self.btn_height + 20), self.btn_width,
        self.btn_height),
                                   "Library")

        self.background = pygame.image.load("assets/menu_background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.window.width, self.window.height))
        self.background.set_alpha(55)

        self.logo = pygame.image.load("assets/logo.png")
        self.logo = pygame.transform.scale(self.logo, (150, 150))

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        if supabase.auth.get_user() is not None:
            self.signed_in = True
            if not self.fetched_stories:
                user_email = supabase.auth.get_user().user.email
                data = supabase.table("stories").select("name, video_path, thumbnail_path").eq("user",
                                                                                               user_email).execute().data
                for obj in data:
                    self.names.append(obj["name"])
                    thumbnail_path = f"./library/{obj['name']}_thumbnail.png"
                    with open(thumbnail_path, "wb+") as f:
                        response = supabase.storage.from_("exported_videos").download(
                            obj["thumbnail_path"]
                        )
                        f.write(response)
                    self.thumbnail_paths.append(thumbnail_path)

                    video_path = f"./library/{obj['name']}_video.mp4"
                    with open(video_path, "wb+") as f:
                        response = supabase.storage.from_("exported_videos").download(
                            obj["video_path"]
                        )
                        f.write(response)
                    self.video_paths.append(video_path)

        self.window.screen.fill(BG_COLOR)
        self.window.screen.blit( self.background, (0,0))
        self.show_text(Fonts.WELCOME.value,"GemPlay", (self.width // 2+50, (self.height // 2) - 100), TITLE_COLOR)

        self.window.screen.blit(self.logo, (self.width//2-250, self.height//2-175))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                def sign_out():
                    supabase.auth.sign_out()
                    self.Switch(MenuScene(self.window, self))

                self.start_btn.on_click(lambda: self.Switch(TopicScene(self.window)), mouse)
                self.sign_in_btn.on_click(lambda: self.Switch(SignInScene(self.window, self)), mouse) if not self.signed_in else self.sign_out_btn.on_click(sign_out, mouse)
                self.help_btn.on_click(lambda: self.Switch(HelpScene(self.window, self)), mouse)
                if self.signed_in:
                    self.library_btn.on_click(lambda: self.Switch(LibraryScene(self.window, self, self.thumbnail_paths, self.video_paths, self.names)), mouse)

        self.start_btn.show()
        self.sign_in_btn.show() if not self.signed_in else self.sign_out_btn.show()
        self.help_btn.show()
        if self.signed_in:
            self.library_btn.show()
