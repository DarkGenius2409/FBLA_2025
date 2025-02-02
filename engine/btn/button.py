import pygame.mouse
from engine.constants import BTN_COLOR, BTN_SELECTED_COLOR, BTN_DESTRUCTIVE_COLOR, BTN_DESTRUCTIVE_BORDER_COLOR, BTN_DESTRUCTIVE_SELECTED_COLOR, BTN_TEXT_COLOR, BTN_BORDER_COLOR
from engine.font import Fonts


class Button:
    def __init__(self, window, rect, text, variant="default"):
        super().__init__()
        self.window = window
        self.text = text
        self.rect = pygame.Rect(rect)  # Use the rect as provided
        self.variant = variant

    def on_click(self, func, mouse):
        if self.rect.collidepoint(mouse):
            func()

    def show_text(self, text):
        rect = self.rect
        font = Fonts.BTN_TEXT.value
        y = rect.centery
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width-24 and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            image = font.render(text[:i], True, BTN_TEXT_COLOR)
            text_rect = image.get_rect(center=(self.rect.centerx, y))
            self.window.screen.blit(image, text_rect)

            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def show(self):
        mouse = pygame.mouse.get_pos()

        # Determine colors based on variant
        if self.variant == "destructive":
            border_color = BTN_DESTRUCTIVE_BORDER_COLOR
            fill_color = BTN_DESTRUCTIVE_SELECTED_COLOR if self.rect.collidepoint(mouse) else BTN_DESTRUCTIVE_COLOR
        else:
            border_color = BTN_BORDER_COLOR
            fill_color = BTN_SELECTED_COLOR if self.rect.collidepoint(mouse) else BTN_COLOR

        # Draw border and button
        pygame.draw.rect(self.window.screen, border_color,
                         (self.rect.x - 3, self.rect.y - 3, self.rect.w + 6, self.rect.h + 6), border_radius=28)
        pygame.draw.rect(self.window.screen, fill_color, self.rect, border_radius=25)

        self.show_text(self.text)


class MenuButton(Button):
    def __init__(self, window, rect, text):
        super().__init__(window, rect, text)

    def show_text(self, text):
        text_object = Fonts.MENU_BTN_TEXT.value.render(text, True, BTN_TEXT_COLOR)
        text_rect = text_object.get_rect(center=self.rect.center)
        self.window.screen.blit(text_object, text_rect)


