import pygame
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        TILE_WIDTH, TILE_HEIGHT = TILE_SIZE
        tileimgs = {
            '0': {
                "movable": True,
                "tileimg": pygame.image.load("graphics/tiles/0.png").subsurface((TILE_WIDTH*0, TILE_HEIGHT*1, TILE_WIDTH, TILE_HEIGHT))
            },
            'A': {
                "movable": False,
                "tileimg": pygame.image.load("graphics/tiles/ua.png").subsurface((TILE_WIDTH*0, TILE_HEIGHT*1, TILE_WIDTH, TILE_HEIGHT))
            }
        }

    def loadmap(fileName):

        returnList = []

        fileIn = open(fileName, "r")
        row = -1
        for lineIn in fileIn:
            row += 1
            returnList.append([])
            line = lineIn.strip()
            tile = None
            for tileIndex in range(0, len(line), 1):
                tile = line[tileIndex]
                returnList[row].append(tile)
        fileIn.close()

        return returnList

    def gettilemap(maplist):

        maxRowIndex = len(maplist)
        maxColIndex = 0

        for rowIndex in range(0, len(maplist), 1):
            if len(maplist[rowIndex]) > maxColIndex:
                maxColIndex = len(maplist[rowIndex])

        returnSurface = pygame.Surface((maxColIndex*TILE_WIDTH, maxRowIndex*TILE_HEIGHT))

        for rowIndex in range(0, len(maplist), 1):
            for colIndex in range(0, len(maplist[rowIndex]), 1):
                tile = maplist[rowIndex][colIndex]
                returnSurface.blit(
                    tileimgs[tile]["tileimg"],
                    (TILE_WIDTH*colIndex, TILE_HEIGHT*rowIndex)
                )
        
        return returnSurface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
