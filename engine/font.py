from enum import Enum
import pygame

pygame.font.init()

class Fonts(Enum):
    TITLE = pygame.font.SysFont('arial', 90)
    BTN = pygame.font.SysFont('arial', 20)
    INPUT = pygame.font.SysFont('arial', 20)
    BTN_TEXT = pygame.font.SysFont('arial', 20)