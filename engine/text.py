class Text:
    def __init__(self, window, font, text, pos, color):
        self.window = window
        self.font = font
        self.text = text
        self.pos = pos
        self.color = color

    def show(self):
        text_object = self.font.value.render(self.text, True, self.color)
        text_rect = text_object.get_rect(center=self.pos)
        self.window.screen.blit(text_object, text_rect)