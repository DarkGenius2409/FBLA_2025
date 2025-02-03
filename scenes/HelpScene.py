import pygame

from engine.constants import BG_COLOR, TEXT_COLOR, TITLE_COLOR
from engine.btn.button import Button, MenuButton
from engine.font import Fonts
from engine.scene import SceneBase


class HelpScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.width = self.window.width
        self.height = self.window.height
        self.btn_width = 200
        self.btn_height = 50
        self.back_btn = MenuButton(self.window, (
        self.width // 2 - self.btn_width / 2, (self.height // 2) + 180, self.btn_width, self.btn_height), "Back")
        self.questions = [
            FAQ(self.window,"Why am I getting an error when I click a choice?",
            "Close the application and open it up again. These errors are rare and often closing and reopening the application works.",
           50, (self.height // 2) - 140),

            FAQ(self.window,"How do I export the story?",
            "Once you are finished with the story or you click the 'exit' button, you will be prompted with an 'Export' button that will allow you to save a video of the story you made!",
            50, (self.height // 2) - 60),

            FAQ(self.window,"Are the stories random?",
            "The stories are somewhat random, but not quite! This application utilizes an AI model that will be generating a story according to the choices you select. The choices you select will influence the movements of the character, the story plot, and the backdrops.",
            50, (self.height // 2) + 20),

            FAQ(self.window,"I want to know more about how this application was coded. How do I contact?",
            "Email gemplay@gmail.com for any questions, comments, or concerns!",
            50, (self.height // 2) + 100)
        ]

    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    def Update(self, events, keys):
        mouse = pygame.mouse.get_pos()

        # Clear the screen with black background
        self.window.screen.fill(BG_COLOR)

        self.show_text(Fonts.WELCOME.value, "Need Help?", (self.width // 2, (self.height // 2) - 220), TEXT_COLOR)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_btn.on_click(self.SwitchBack, mouse)
                for faq in self.questions:
                    faq.check_click(event.pos)

        for faq in self.questions:
            faq.show(self.window.screen)

        self.back_btn.show()


class FAQ:
    def __init__(self, window, question, answer, x, y):
        self.question = question
        self.window = window
        self.answer = answer
        self.rect = pygame.Rect(x, y, self.window.width-40, 40)
        self.visible = False

    def wrap_text(self, text, font):
        rect = self.rect
        lines = []

        while text:
            i = 1

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width-24 and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            lines.append(text[:i])

            # remove the text we just blitted
            text = text[i:]

        return lines

    def show(self, screen):
        question_text = Fonts.FAQ_TEXT.value.render(self.question, True, TEXT_COLOR)
        screen.blit(question_text, (self.rect.x, self.rect.y))

        if self.visible:
            # answer_text = Fonts.FAQ_ANSWER_TEXT.value.render(self.answer, True, TEXT_COLOR)
            # screen.blit(answer_text, (self.rect.x + 10, self.rect.y + 40))

            lines = self.wrap_text(self.answer, Fonts.FAQ_ANSWER_TEXT.value)

            fontHeight = Fonts.FAQ_ANSWER_TEXT.value.size("Tg")[1]
            lineSpacing = 2
            y = self.rect.y+ 40 - ((len(lines) - 1) * 0.5 * (fontHeight + lineSpacing))

            for line in lines:
                image = Fonts.FAQ_ANSWER_TEXT.value.render(line, True, TEXT_COLOR)
                screen.blit(image, (self.rect.x+10, y))
                y += fontHeight + lineSpacing

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.visible = not self.visible

