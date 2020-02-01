#!/usr/bin/python

import pygame

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    width = screen.get_width()
    height = screen.get_height()

    bgimg = pygame.image.load("graphics/sci-fi-level_-_background_layer.png")

    done = False
    width_index = 0

    while not done:

        width_index -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        screen.blit(bgimg, (width_index, 0))
        pygame.display.flip()

    pygame.quit()
