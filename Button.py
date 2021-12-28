from pygame import *

import pygame
from typing import Tuple

from constants import *
pygame.init()
arial_font = font.SysFont('Arial', 15, bold=True)


class Button:
    def __init__(self, title: str, size: Tuple[int, int], color=Color(79, 84, 79), x=0, on_click_func=None) -> None:
        self.title = title
        self.size = size
        self.color = color
        self.rect = Rect((0, 0), size)
        self.on_click = on_click_func
        self.is_visible = False
        self.pos = (x, screen_size - size[1] - padding)

    def set_color(self, tuple: tuple):
        self.color = tuple

    def set_pos(self, x, new_y):
        self.pos = (x, new_y)

    def get_pos_x(self):
        return self.pos[0]

    def get_pos_y(self):
        return self.pos[1]

    def get_pos(self):
        return self.pos

    def render(self, surface: Surface):
        if not self.is_visible:
            return
        self.rect.topleft = self.pos

        title_srf = arial_font.render(self.title, True, Color(255, 255, 255))
        title_rect = title_srf.get_rect(center=self.rect.center)
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(title_srf, title_rect)

    def check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            clicked, _, _ = pygame.mouse.get_pressed()
            if clicked and self.is_visible:
                self.on_click()

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def show(self):
        self.is_visible = True

    def hide(self):
        self.is_visible = False

    def set_x(self, x):
        self.pos = (x, self.pos[1])

    def get_x(self):
        return self.pos[0]
