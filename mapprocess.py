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

            # TODO numerical order 0-9 then Uppercase A-a done alpabetically A-a---Z-z
            '0': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "dirt1tile.png"), 0, 0)
            },
            '1': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "junkpile1.png"), 0, 0)
            },
            '2': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "junkpile2.png"), 0, 0)
            },
            '3': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "junkpile3.png"), 0, 0)
            },
            '4': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "junkpile4.png"), 0, 0)
            },
            '5': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "junkpile5.png"), 0, 0)
            },
            '6': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "junkpile6.png"), 0, 0)
            },
            'A': { # TODO
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "ua.png"), 1, 0)
            },
            'C': { # chainlink
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "chainlink.png"), 0, 0)
            },
            'c': {  # TODO
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "carpile.png"), 1, 0)
            },
            'D': { # Dirt
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "dirtandgrasses.png"), 0, 0)
            },
            'd': {  # Dirt
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "dirtandgrasses.png"), 1, 1)
            },
            'E': { # grass1edges
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "grass1edges.png"), 0, 0)
            },
            'e': {# grass1edges
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "grass1edges.png"), 1, 0)
            },
            'F': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "grass1edges.png"), 1, 1)
            },
            'f': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "grass1edges.png"), 0, 1)
            },
            'G': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "grasses.png"), 1, 0)
            },
            'g': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "dirtandgrasses.png"), 0, 1)
            },
            'J': {
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "midjunkpile3.png"), 1, 0)
            },
            'j': {
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "dirt1tile.png"), 0, 0)
            },
            'P': {  # Carpile
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "carpile.png"), 0, 0)
            },
            'p': {  # Carpile
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "carpile.png"), 1, 0)
            },
            'Q': {  # Carpile
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "carpile.png"), 0, 1)
            },
            'q': {  # Carpile
                "walkable": False,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "carpile.png"), 1, 1)
            },
            'S': { # Spawn
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "grasses.png"), 1, 0)
            },
            'z': { # End place holder
                "walkable": True,
                "tileimg": self.getmaptile(os.path.join(maptilesfolder, "door.png"), 0, 0)
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
