import pygame
from pygame import Rect

from engine.font import Fonts
from engine.text import Text


class TextInput:
    def __init__(self, window, rect, placeholder):
        self.window = window
        self.rect = Rect(rect)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.active_color = (170, 170, 170)
        self.passive_color = (100, 100, 100)

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

    def show(self):
        if self.active:
            color = self.active_color
        else:
            color = self.passive_color

        pygame.draw.rect(self.window.screen, color, self.rect)
        if self.text is not None:
            text = Text(self.window, Fonts.INPUT, self.text, (self.rect.x+self.rect.w/2, self.rect.y+self.rect.h/2, self.rect.w, self.rect.h))
        else:
            text = Text(self.window, Fonts.INPUT, self.placeholder, (self.rect.x+self.rect.w/2, self.rect.y+self.rect.h/2, self.rect.w, self.rect.h))

        text.show()

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()