from enum import Enum
import pygame

pygame.font.init()

class Fonts(Enum):
    WELCOME = pygame.font.Font('assets/fonts/Nunito-Regular.ttf', 80)
    TITLE = pygame.font.Font('assets/fonts/Nunito-Regular.ttf', 50)
    BTN = pygame.font.Font('assets/fonts/Nunito-Light.ttf', 20)
    INPUT = pygame.font.Font('assets/fonts/Nunito-Regular.ttf', 24)
    MENU_BTN_TEXT = pygame.font.Font('assets/fonts/Nunito-ExtraBold.ttf', 20)
    BTN_TEXT = pygame.font.Font('assets/fonts/Nunito-Regular.ttf', 25)
    SPEECH_TEXT = pygame.font.Font('assets/fonts/Nunito-Light.ttf', 20)
    SCENE_TEXT = pygame.font.Font('assets/fonts/Nunito-Regular.ttf', 32)
    FAQ_ANSWER_TEXT = pygame.font.Font('assets/fonts/Nunito-Regular.ttf', 18)
    FAQ_TEXT = pygame.font.Font('assets/fonts/Nunito-ExtraBold.ttf', 24)
