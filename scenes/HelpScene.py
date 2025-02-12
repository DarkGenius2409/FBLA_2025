import pygame
from engine.constants import BG_COLOR, TEXT_COLOR
from engine.btn.button import MenuButton
from engine.font import Fonts
from engine.scene import SceneBase
from engine.text_input import TextInput
from engine.ai.generate import askQuestion

class HelpScene(SceneBase):
    def __init__(self, window, prev):
        super().__init__(window, prev)
        self.width = self.window.width
        self.height = self.window.height

        # Instantiating Back Button
        self.btn_width = 200
        self.btn_height = 50
        self.back_btn = MenuButton(self.window, (
            self.width // 2 - self.btn_width / 2, self.height - self.btn_height - 20, self.btn_width, self.btn_height
        ), "Back")

        # Chatbot Section
        self.messages = []
        self.messageInput = TextInput(self.window, (self.width - 400, self.height - 200, 300, 50), "Write here..")
        self.send = MenuButton(self.window, (self.width - 200, self.height - 130, 100, 50), "Send")

        # How-To Steps
        steps = [
            "1. Sign in and insert your username and password",
            "2. Once logged in, click the new story button to generate your own custom story",
            "3. Click the help button if you have any questions, comments, and concerns",
            "4. Keep selecting a choice until the story comes to an end (~10 choices)",
            "5. Click the “Exit” button to stop the story at any time and export it to a cloud library",
            "6. If you don’t want to export, click the “home” button to navigate to the welcome page",
            "7. Click the library button to see all the videos you have exported in your account",
            "8. Interact with an AI chatbot on help page that will answer any questions regarding the app"
        ]
        self.steps = []

        for step in steps:
            self.steps.append(self.wrap_text(step, Fonts.SPEECH_TEXT.value, max_width=800))

    # Show Text Function
    def show_text(self, font, text, pos, color):
        text_object = font.render(text, True, color)
        text_rect = text_object.get_rect(center=pos)
        self.window.screen.blit(text_object, text_rect)

    # Update Method: runs every frame
    def Update(self, events, keys):
        # Gets mouse pos on the current frame
        mouse = pygame.mouse.get_pos()

        # Clear the screen with background color
        self.window.screen.fill(BG_COLOR)

        # Show the title
        self.show_text(Fonts.TITLE.value, "How to use:", (180, 60), TEXT_COLOR)

        # Show all the steps to use the app
        y = 60
        for step in self.steps:
            offset = 0
            for i, line in enumerate(step):
                text_surface = Fonts.SPEECH_TEXT.value.render(line, True, TEXT_COLOR)
                text_rect = text_surface.get_rect()
                text_rect.left = 60
                text_rect.y = y + i * 20 + 40
                offset += i * 20 + 30
                self.window.screen.blit(text_surface, text_rect)
            y += offset+10

        # Display chatbot messages
        y = self.height // 2 - 150
        for msg in self.messages:
            rect = self.show_msg(msg["message"], (self.width - 250, y), sent=msg["sent"])
            y = rect.bottom + 120

        # Check for any events
        for event in events:
            # Checks if mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if back button is clicked
                self.back_btn.on_click(self.SwitchBack, mouse)

                # Callback Function for sending the chatbot a question
                def sendMsg():
                    if self.messageInput.text.strip():
                        text = askQuestion(self.messageInput.text)
                        self.messages = []
                        self.messages.append({"message": f"You: {self.messageInput.text}", "sent": True})
                        self.messages.append({"message": f"AI: {text}", "sent": False})
                        self.messageInput.text = ""

                # Checks if
                self.send.on_click(sendMsg, mouse)

            # Updates message text input
            self.messageInput.update(event)

        # Shows all UI elements
        self.send.show()
        self.back_btn.show()
        self.messageInput.show()

    # Show msg method
    def show_msg(self, text, pos, max_width=300, sent=True):
        font = Fonts.SPEECH_TEXT.value
        lines = self.wrap_text(text, font, max_width)
        color = (0, 200, 0) if sent else (133, 50, 168)

        line_height = font.get_linesize()
        box_height = line_height * len(lines) + 20
        box_width = max_width + 20

        rect = pygame.Rect(0, 0, box_width, box_height)
        rect.center = pos
        pygame.draw.rect(self.window.screen, color, rect, border_radius=15)

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (rect.left + 10, rect.top + 10 + i * line_height)
            self.window.screen.blit(text_surface, text_rect)

        return rect

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

