import os
import pygame
import settings


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename=None, maptilesfolder=None):
        self.TILE_WIDTH = settings.TILESIZE
        self.TILE_HEIGHT = settings.TILESIZE
        self.tileimgs = {
            '0': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "0.png"), 1, 0)
            },
            'J': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "J.png"), 1, 0)
            },
            'j': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "j.png"), 1, 0)
            },
            'A': {
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "ua.png"), 1, 0)
            }
        }
        if filename:
            self.loadmap(filename)

    def getmaptile(self, filename, row, col):
        return pygame.image.load(filename).subsurface(
            (
                self.TILE_WIDTH*col,
                self.TILE_HEIGHT*row,
                self.TILE_WIDTH,
                self.TILE_HEIGHT
            )
        )

    def loadmap(self, fileName):

        self.maplist = []

        fileIn = open(fileName, "r")
        row = -1
        for lineIn in fileIn:
            row += 1
            self.maplist.append([])
            line = lineIn.strip()
            tile = None
            for tileIndex in range(0, len(line), 1):
                tile = line[tileIndex]
                self.maplist[row].append(tile)
        fileIn.close()

    def gettilemap(self):

        maxRowIndex = len(self.maplist)
        maxColIndex = 0

        for rowIndex in range(0, len(self.maplist), 1):
            if len(self.maplist[rowIndex]) > maxColIndex:
                maxColIndex = len(self.maplist[rowIndex])

        returnSurface = pygame.Surface(
            (
                maxColIndex*self.TILE_WIDTH,
                maxRowIndex*self.TILE_HEIGHT
            )
        )

        for rowIndex in range(0, len(self.maplist), 1):
            for colIndex in range(0, len(self.maplist[rowIndex]), 1):
                returnSurface.blit(
                    self.tileimgs[self.maplist[rowIndex][colIndex]]["tileimg"],
                    (self.TILE_WIDTH*colIndex, self.TILE_HEIGHT*rowIndex)
                )

        return returnSurface

    def getwallmap(self):
        returnList = []
        for rowIndex in range(0, len(self.maplist), 1):
            for colIndex in range(0, len(self.maplist[rowIndex]), 1):
                if not self.tileimgs[self.maplist[rowIndex][colIndex]]["walkable"]:
                    returnList.append(
                       (
                           self.TILE_WIDTH*colIndex,
                           self.TILE_HEIGHT*rowIndex,
                           self.TILE_WIDTH,
                           self.TILE_HEIGHT
                        )
                    )
        return returnList


class Camera:
    def __init__(self, width, height):

        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(settings.WIDTH / 2)
        y = -target.rect.centery + int(settings.HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - settings.WIDTH), x)  # right
        y = max(-(self.height - settings.HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
