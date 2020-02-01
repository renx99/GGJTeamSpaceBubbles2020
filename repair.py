from mapprocess import loadmap
from mapprocess import gettilemap

import pygame

MAP_WIDTH_THRESH = 32
MAP_HEIGHT_THRESH = 32

if __name__ == "__main__":

    tilemaplist = loadmap("test2.map")
    tilemap = gettilemap(tilemaplist)

    pygame.init()
    pygame.key.set_repeat(500, 1)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    done = False

    px = screen.get_width() / 2
    py = screen.get_height() / 2

    mapx = -(tilemap.get_width() / 2)
    mapy = -(tilemap.get_height() / 2)

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

        if px < 0:
            px = 0
        elif px > tilemap.get_width():
            px = tilemap.get_width()

        if py < 0:
            py = 0
        elif py > tilemap.get_height():
            py = tilemap.get_height()

        # Does not stop in other direction
        if screen.get_width() > (tilemap.get_width() + mapx):
            mapx = tilemap.get_width() - screen.get_width()
            px = screen.get_width() - MAP_WIDTH_THRESH
        
        # Does not stop in other direction
        if screen.get_height() > (tilemap.get_height() + mapy):
            mapy = tilemap.get_height() - screen.get_height()
            py = screen.get_height() - MAP_HEIGHT_THRESH

        if px < MAP_WIDTH_THRESH:
            mapx += (MAP_WIDTH_THRESH - px)
            px = MAP_WIDTH_THRESH
        elif px > (screen.get_width() - MAP_WIDTH_THRESH):
            mapx -= ((MAP_WIDTH_THRESH + px) - screen.get_width())
            px = (screen.get_width() - MAP_WIDTH_THRESH)

        if py < MAP_HEIGHT_THRESH:
            mapy += (MAP_HEIGHT_THRESH - py)
            py = MAP_HEIGHT_THRESH
        elif py > (screen.get_height() - MAP_HEIGHT_THRESH):
            mapy -= ((MAP_HEIGHT_THRESH + py) - screen.get_height())
            py = (screen.get_height() - MAP_HEIGHT_THRESH)


        screen.blit(tilemap, (int(mapx), int(mapy)))
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(px), int(py)),
            16
        )

        pygame.display.flip()

    pygame.quit()
