from pygame import Rect

from engine.constants import TEXT_COLOR


class Text:
    def __init__(self, window, font, text, rect):
        self.window = window
        self.font = font
        self.text = text
        self.rect = rect
        self.color = TEXT_COLOR

    def show(self):
        text_object = self.font.value.render(self.text, True, self.color)
        text_rect = text_object.get_rect(center=self.rect.center)
        self.window.screen.blit(text_object, text_rect)

    def show_wrapped(self, aa=False, bkg=None):
        text = self.text
        y = self.rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > self.rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text[:i])[0] < self.rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(self.text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = self.font.render(text[:i], 1, TEXT_COLOR, bkg)
                image.set_colorkey(bkg)
            else:
                image = self.font.render(text[:i], aa, TEXT_COLOR)

            self.window.screen.blit(image, (self.rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text