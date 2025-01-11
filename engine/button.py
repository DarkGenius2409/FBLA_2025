import pygame.mouse


class Button:
    def __init__(self, window, rect, text):
        super().__init__()
        self.window = window
        self.text = text
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.font = pygame.font.SysFont('arial', 20)
        # light shade of the button
        self.color_light = (170, 170, 170)
        # dark shade of the button
        self.color_dark = (100, 100, 100)

    def on_click(self, func, mouse):
        if self.x / 2 - self.width / 2 <= mouse[
            0] <= self.x / 2 + self.width / 2 and self.y / 2 - self.height / 2 <= mouse[
            1] <= self.y + self.height / 2:
            func()

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def show(self):
        mouse = pygame.mouse.get_pos()
        if self.x / 2 - self.width / 2 <= mouse[
            0] <= self.x / 2 + self.width / 2 and self.y / 2 - self.height / 2 <= mouse[
            1] <= self.y + self.height / 2:
            pygame.draw.rect(self.window.screen, self.color_light,
                             [self.x - self.width / 2, self.y / 2 - self.height / 2,
                              self.width, self.height], border_radius=25)
        else:
            pygame.draw.rect(self.window.screen, self.color_dark,
                             [self.x - self.width / 2,
                              self.y - self.height / 2,
                              self.width, self.height], border_radius=25)

        # superimposing the text onto our button
        self.show_text(self.font, self.text, (self.x, self.y), (255, 255, 255))