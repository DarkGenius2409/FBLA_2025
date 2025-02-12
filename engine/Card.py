from turtledemo.sorting_animate import show_text

import pygame.mouse
from engine.constants import BTN_COLOR, BTN_SELECTED_COLOR, BTN_DESTRUCTIVE_COLOR, BTN_DESTRUCTIVE_BORDER_COLOR, \
    BTN_DESTRUCTIVE_SELECTED_COLOR, BTN_TEXT_COLOR, BTN_BORDER_COLOR, WIDTH, HEIGHT
from engine.font import Fonts


class Card:
    def __init__(self, window, rect, img, video, name):
        super().__init__()
        self.window = window
        self.name = name
        self.rect = pygame.Rect(rect)
        self.img_path = img
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (WIDTH*0.18, HEIGHT*0.18))
        self.video = video
        # Use the rect as provided
        self.font = Fonts.BTN_TEXT.value

    def on_click(self, func, mouse):
        if self.rect.collidepoint(mouse):
            func()

    def show_text(self, text, pos):
        text_object = Fonts.MENU_BTN_TEXT.value.render(text, True, BTN_TEXT_COLOR)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def show(self):
        mouse = pygame.mouse.get_pos()

        border_color = BTN_BORDER_COLOR
        fill_color = BTN_SELECTED_COLOR if self.rect.collidepoint(mouse) else BTN_COLOR

        # Draw border and button
        pygame.draw.rect(self.window.screen, border_color,
                         (self.rect.x - 3, self.rect.y - 3, self.rect.w + 6, self.rect.h + 6), border_radius=28)
        pygame.draw.rect(self.window.screen, fill_color, self.rect, border_radius=25)

        img_rect = self.img.get_rect(center=(self.rect.centerx, self.rect.centery-10))
        self.window.screen.blit(self.img, img_rect)

        self.show_text(self.name, (self.rect.centerx, self.rect.y+self.rect.h-10))




