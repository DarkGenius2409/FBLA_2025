import pygame
from pygame import Rect

from engine.constants import BTN_SELECTED_COLOR, TEXT_INPUT_SELECTED_COLOR, TEXT_INPUT_COLOR, TEXT_INPUT_BORDER_COLOR, \
    TEXT_COLOR
from engine.font import Fonts
from engine.text import Text


class TextInput:
    def __init__(self, window, rect, placeholder):
        self.window = window
        self.rect = Rect(rect)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.active_color = TEXT_INPUT_SELECTED_COLOR
        self.passive_color = TEXT_INPUT_COLOR
        self.font = Fonts.INPUT

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    self.text = self.text[:-1]

                # Unicode standard is used for string formation
                else:
                    self.text += event.unicode

    def show_text(self, text):
        text_object = self.font.value.render(text, True, TEXT_COLOR)
        text_rect = text_object.get_rect(center=self.rect.center)
        self.window.screen.blit(text_object, text_rect)

    def show(self):
        if self.active:
            color = self.active_color
        else:
            color = self.passive_color

        pygame.draw.rect(self.window.screen, TEXT_INPUT_BORDER_COLOR,
                         (self.rect.x, self.rect.y, self.rect.w, self.rect.h + 5))
        pygame.draw.rect(self.window.screen, color, self.rect)

        self.show_text(self.text if self.text != "" else self.placeholder)