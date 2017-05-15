from const import *
from random import randint


class Thing:

    def random_type(self):
        self.thing_type = randint(1, 7)

    def random_color(self):
        self.thing_color = randint(0, len(THING_COLORS)-1)

    def __init__(self, thing_type=0, thing_color=0):
        if thing_type < 0:
            self.random_type()
        else:
            self.thing_type = thing_type

        if thing_color < 0:
            self.random_color()
        else:
            self.thing_color = thing_color

        self.x_line = 0
        self.y_line = 0
        self.need_update = False


