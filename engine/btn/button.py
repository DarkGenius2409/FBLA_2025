import pygame.mouse
from pygame import Rect

from engine.constants import BTN_COLOR, BTN_SELECTED_COLOR, TEXT_COLOR
from engine.font import Fonts


class Button:
    def __init__(self, window, rect, text):
        super().__init__()
        self.window = window
        self.text = text
        self.rect = pygame.Rect(rect)  # Use the rect as provided
        self.font = Fonts.BTN_TEXT.value
        self.color_light = BTN_SELECTED_COLOR
        self.color_dark = BTN_COLOR

    def on_click(self, func, mouse):
        if self.rect.collidepoint(mouse):
            func()

    def show_text(self, text, aa=False, bkg=None):
        rect = self.rect
        y = rect.centery
        lineSpacing = -2

        # get the height of the font
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = self.font.render(text[:i], 1, TEXT_COLOR, bkg)
                image.set_colorkey(bkg)
            else:
                image = self.font.render(text[:i], aa, TEXT_COLOR)

            text_rect = image.get_rect(center=(self.rect.centerx, y))
            self.window.screen.blit(image, text_rect)
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def show(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(self.window.screen, self.color_light, self.rect, border_radius=25)
        else:
            pygame.draw.rect(self.window.screen, self.color_dark, self.rect, border_radius=25)

        self.show_text(self.text)
