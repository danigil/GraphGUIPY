from pygame import *

from typing import List
from Button import Button
from constants import button_width, button_height, padding, screen_size


class MenuItem:
    def __init__(self, button: Button, buttons: List[Button]):
        self._button = button
        self._buttons = buttons
        self.define_button_pos()

    def get_button(self):
        return self._button

    def get_buttons(self):
        return self._buttons

    def check_rect(self, mouse_pos):
        if len(self._buttons) != 0:
            left_corner = self._buttons[-1].get_pos()
        else:
            left_corner= self._button.get_pos()

        right_corner = (button_width, (button_height * (len(self._buttons) + 1)) + (len(self._buttons) * padding))
        algo_rec = Rect(left_corner, right_corner)
        mouse_pos = mouse_pos

        if algo_rec.collidepoint(mouse_pos):
            return True
        else:
            return False

    def define_button_pos(self):
        for i in range(len(self._buttons)):
            self._buttons[i].set_pos(self._button.pos[0], screen_size - ((i+2) * (button_height + padding)))