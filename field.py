from const import *
from thing import Thing


class Field:

    def __init__(self, pg, surface, clock):
        self.pygame = pg
        self.surface = surface
        self.clock = clock
        self.grid = {}
        for x in range(1, GRID_X + 1):
            for y in range(1, GRID_Y + 1):
                self.grid[x, y] = Thing()

    def cell_rect(self, x, y, padding=0, x_padding=0, y_padding=0):
        cell_x = GRID_PADDING_X + (x - 1) * GRID_CELL_SIZE + padding + x_padding
        cell_y = GRID_PADDING_Y + (GRID_Y - y) * GRID_CELL_SIZE + padding + y_padding
        return [cell_x, cell_y, GRID_CELL_SIZE - padding * 2, GRID_CELL_SIZE - padding * 2]

    def draw_grid(self, redraw_things=True):
        for x in range(1, GRID_X + 1):
            for y in range(1, GRID_Y + 1):
                self.pygame.draw.rect(self.surface, BROWN, self.cell_rect(x, y), GRID_LINE_WIDTH)
                if redraw_things:
                    self.draw_thing(x, y)

    def fill_line(self, y):
        inserted = False
        for x in range(1, GRID_X + 1):
            if self.grid[x, y].thing_type == 0:
                self.grid[x, y] = Thing(1, -1)
                inserted = True
        return inserted

    def drop_things(self):
        res = False
        for y in range(1, GRID_Y):
            for x in range(1, GRID_X + 1):
                if self.grid[x, y].thing_type == 0:
                    if self.grid[x, y + 1].thing_type != 0:
                        t = self.grid[x, y]
                        self.grid[x, y] = self.grid[x, y + 1]
                        self.grid[x, y + 1] = t
                        self.grid[x, y].need_update = True
                        res = True
        if res:
            for dy in range(1, GRID_CELL_SIZE, THING_SPEED):
                self.surface.fill(DARK_BLUE)
                self.draw_grid(False)
                for y in range(1, GRID_Y+1):
                    for x in range(1, GRID_X + 1):
                        if self.grid[x, y].need_update:
                            self.draw_thing(x, y, 0, dy - GRID_CELL_SIZE)
                        else:
                            self.draw_thing(x, y)
                self.pygame.display.update()
                self.clock.tick(CLOCK_TICK)
            for y in range(1, GRID_Y+1):
                for x in range(1, GRID_X + 1):
                    self.grid[x, y].need_update = False

        return res

    def draw_thing(self, x, y, x_padding=0, y_padding=0):
        if self.grid[x, y].thing_type != 0:
            self.pygame.draw.rect(self.surface, THING_COLORS[self.grid[x, y].thing_color],
                                  self.cell_rect(x, y, THING_PADDING, x_padding, y_padding), THING_LINE_HEIGHT)

    def kaboom_things(self):
        # search for horizontal line
        line_len = 0
        prev_thing = Thing()
        collected_thing = []

        for y in range(1, GRID_Y + 1):
            for x in range(1, GRID_X + 1):
                if self.grid[x, y].thing_type != 0:
                    if prev_thing.thing_color == self.grid[x, y].thing_color:
                        line_len += 1
                        collected_thing.append(self.grid[x, y])
                    else:
                        if line_len > 1:
                            # 3 or more in a row
                            for t in collected_thing:
                                t.x_line = line_len
                        line_len = 0
                        prev_thing = self.grid[x, y]
                        collected_thing = [self.grid[x, y]]
            prev_thing = Thing()

        # search for vertical line
        line_len = 0
        prev_thing = Thing()
        collected_thing = []

        for x in range(1, GRID_X + 1):
            for y in range(1, GRID_Y + 1):
                if self.grid[x, y].thing_type != 0:
                    if prev_thing.thing_color == self.grid[x, y].thing_color:
                        line_len += 1
                        collected_thing.append(self.grid[x, y])
                    else:
                        if line_len > 1:
                            # 3 or more in a row
                            for t in collected_thing:
                                t.y_line = line_len
                        line_len = 0
                        prev_thing = self.grid[x, y]
                        collected_thing = [self.grid[x, y]]
            prev_thing = Thing()

        for y in range(1, GRID_Y + 1):
            for x in range(1, GRID_X + 1):
                if self.grid[x, y].x_line > 0 or self.grid[x, y].y_line:
                    self.grid[x, y] = Thing()
