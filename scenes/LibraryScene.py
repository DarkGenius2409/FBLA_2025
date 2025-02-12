import pygame
from pygame import Rect

from cloud import supabase
from engine.Card import Card
from engine.CardGrid import CardGrid
from engine.constants import BG_COLOR, TEXT_COLOR, TITLE_COLOR
from engine.btn.button import Button, MenuButton
from engine.font import Fonts
from engine.scene import SceneBase
from scenes.VideoScene import VideoScene


class LibraryScene(SceneBase):
    def __init__(self, window, prev, thumbnails, videos, names):
        super().__init__(window, prev)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.cards = []
        if len(thumbnails) >= 1:
            card_rect = Rect(0, 0, self.width / 2 - 85, self.height / 4)
            card_rect.centery = self.height // 2 - 40
            card_rect.right = self.width/2 - 10
            self.cards.append(Card(self.window, card_rect, thumbnails[0], videos[0], names[0]))
        if len(thumbnails) >= 2:
            card_rect = Rect(0, 0, self.width / 2 - 85, self.height / 4)
            card_rect.centery = self.height // 2 - 40
            card_rect.left = self.width/2 + 10
            self.cards.append(Card(self.window, card_rect, thumbnails[1], videos[1], names[1]))
        if len(thumbnails) >= 3:
            card_rect = Rect(0, 0, self.width/2 - 85, self.height / 4)
            card_rect.centery = (3*self.height / 4) - 30
            card_rect.right = self.width/2 - 10
            self.cards.append(Card(self.window, card_rect, thumbnails[2], videos[2], names[2]))
        elif len(thumbnails) >= 4:
            self.cards = self.create_grid(thumbnails, videos, names).cards

        print()
        self.back_btn = MenuButton(self.window, (self.width//2 - self.btn_width/2, self.height - 100, self.btn_width, self.btn_height), "Back" )

    def create_grid(self, thumbnails,videos,names):
        card_grid_rect = Rect(0, 0, self.width - 150, self.height / 2)
        card_grid_rect.center = (self.width // 2, self.height // 2 + 75)
        return CardGrid(self.window, card_grid_rect, (2, 2), (20, 20), thumbnails, videos, names)

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill(BG_COLOR)

        self.show_text(Fonts.WELCOME.value,"Library", (self.width // 2, (self.height // 2) - 200 ), TEXT_COLOR)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_btn.on_click(lambda: self.SwitchBack(), mouse)
                for card in self.cards:
                    card.on_click(lambda: self.Switch(VideoScene(self.window, self, card.video, card.name, card.img_path)), mouse)

        for card in self.cards:
            card.show()
        self.back_btn.show()