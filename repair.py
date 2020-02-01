#!/usr/bin/python

import pygame

if __name__ == "__main__":

    pygame.init()
    pygame.image.load()

    done = False

    while not done:

        for event pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
