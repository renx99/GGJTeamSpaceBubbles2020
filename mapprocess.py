import pygame
import settings


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.TILE_WIDTH = settings.TILESIZE
        self.TILE_HEIGHT = settings.TILESIZE
        self.tileimgs = {
            '0': {
                "movable": True,
                "tileimg": self.getmaptile("graphics/tiles/0.png", 1, 0)
            },
            'A': {
                "movable": False,
                "tileimg": self.getmaptile("graphics/tiles/ua.png", 1, 0)
            }
        }
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

        returnSurface = pygame.Surface((maxColIndex*self.TILE_WIDTH, maxRowIndex*self.TILE_HEIGHT))

        for rowIndex in range(0, len(self.maplist), 1):
            for colIndex in range(0, len(self.maplist[rowIndex]), 1):
                tile = self.maplist[rowIndex][colIndex]
                returnSurface.blit(
                    self.tileimgs[tile]["tileimg"],
                    (self.TILE_WIDTH*colIndex, self.TILE_HEIGHT*rowIndex)
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
