import pygame.mouse
from engine.constants import BTN_COLOR, BTN_SELECTED_COLOR, BTN_DESTRUCTIVE_COLOR, BTN_DESTRUCTIVE_BORDER_COLOR, BTN_DESTRUCTIVE_SELECTED_COLOR, BTN_TEXT_COLOR, BTN_BORDER_COLOR
from engine.font import Fonts


class Card:
    def __init__(self, window, rect, text):
        super().__init__()
        self.window = window
        self.text = text
        self.rect = pygame.Rect(rect)  # Use the rect as provided
        self.font = Fonts.BTN_TEXT.value

    def on_click(self, func, mouse):
        if self.rect.collidepoint(mouse):
            func()

    def show_text(self, text):
        text_object = Fonts.MENU_BTN_TEXT.value.render(text, True, BTN_TEXT_COLOR)
        text_rect = text_object.get_rect(center=self.rect.center)
        self.window.screen.blit(text_object, text_rect)

    def show(self):
        mouse = pygame.mouse.get_pos()

        border_color = BTN_BORDER_COLOR
        fill_color = BTN_SELECTED_COLOR if self.rect.collidepoint(mouse) else BTN_COLOR

        # Draw border and button
        pygame.draw.rect(self.window.screen, border_color,
                         (self.rect.x - 3, self.rect.y - 3, self.rect.w + 6, self.rect.h + 6), border_radius=28)
        pygame.draw.rect(self.window.screen, fill_color, self.rect, border_radius=25)


