#!/usr/bin/python

import pygame

if __name__ == "__main__":

    pygame.init()
    pygame.key.set_repeat(500, 1)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    width = screen.get_width()
    height = screen.get_height()

    bgimg = pygame.image.load("graphics/sci-fi-level_-_background_layer.png")

    done = False

    px = width / 2
    py = height / 2

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP:
                    py -= 5
                elif event.key == pygame.K_RIGHT:
                    px += 5
                elif event.key == pygame.K_DOWN:
                    py += 5
                elif event.key == pygame.K_LEFT:
                    px -= 5

        screen.blit(bgimg, (0, 0))
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(px), int(py)),
            10
        )

        pygame.display.flip()

    pygame.quit()
