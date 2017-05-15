import pygame
from field import Field

from const import *

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Infinity Gems')
clock = pygame.time.Clock()


def main():

    game_over = False
    field = Field(pygame, surface, clock)
    field.fill_line(GRID_Y)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    field = Field(pygame, surface, clock)

                if event.key == pygame.K_q:
                    game_over = True

        f = True
        while f:
            f = field.fill_line(GRID_Y)
            f = f or field.drop_things()
            surface.fill(DARK_BLUE)
            field.draw_grid()
            pygame.display.update()
            clock.tick(CLOCK_TICK)

        field.kaboom_things()

        surface.fill(DARK_BLUE)
        field.draw_grid()
        pygame.display.update()
        clock.tick(CLOCK_TICK)


main()
pygame.quit()
quit()

