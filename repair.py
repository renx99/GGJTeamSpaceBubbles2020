from mapprocess import loadmap
from mapprocess import gettilemap

import pygame

if __name__ == "__main__":

    tilemaplist = loadmap("test1.map")
    tilemap = gettilemap(tilemaplist)

    pygame.init()
    pygame.key.set_repeat(500, 1)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = screen.get_width()
    height = screen.get_height()


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
                    py -= 1
                elif event.key == pygame.K_RIGHT:
                    px += 1
                elif event.key == pygame.K_DOWN:
                    py += 1
                elif event.key == pygame.K_LEFT:
                    px -= 1

        screen.blit(tilemap, (0, 0))
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(px), int(py)),
            10
        )

        pygame.display.flip()

    pygame.quit()
