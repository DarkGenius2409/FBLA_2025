import pygame.mouse


class Button:
    def __init__(self, window, rect, text):
        super().__init__()
        self.window = window
        self.text = text
        self.rect = pygame.Rect(rect)  # Use the rect as provided
        self.font = pygame.font.SysFont('arial', 20)
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)

    def on_click(self, func, mouse):
        if self.rect.collidepoint(mouse):
            func()

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def show(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(self.window.screen, self.color_light, self.rect, border_radius=25)
        else:
            pygame.draw.rect(self.window.screen, self.color_dark, self.rect, border_radius=25)

        self.show_text(self.font, self.text, self.rect.center, (255, 255, 255))
