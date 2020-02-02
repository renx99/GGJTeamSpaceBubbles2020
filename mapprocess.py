import os
import pygame
import settings


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class Map:
    def __init__(self, filename=None, maptilesfolder=None):
        map_t = lambda t, x, y : self.getmaptile(os.path.join(maptilesfolder, t), x, y)
        self.TILE_WIDTH = settings.TILESIZE
        self.TILE_HEIGHT = settings.TILESIZE
        self.tileimgs = {
            # TODO numerical order 0-9 then Uppercase A-a done alpabetically A-a---Z-z
            '0': {'walkable': True, 'tileimg': map_t('dirt1tile.png', 0, 0)},
            '1': {'walkable': True, 'tileimg': map_t('junkpile1.png', 0, 0)},  # Used
            '2': {'walkable': True, 'tileimg': map_t('junkpile2.png', 0, 0)},  # Used
            '3': {'walkable': True, 'tileimg': map_t('junkpile3.png', 0, 0)},  # Used
            '4': {'walkable': True, 'tileimg': map_t('junkpile4.png', 0, 0)},  # Used
            '5': {'walkable': True, 'tileimg': map_t('junkpile5.png', 0, 0)},  # Used
            '6': {'walkable': True, 'tileimg': map_t('junkpile6.png', 0, 0)},  # Used
            'A': {'walkable': True, 'tileimg': map_t('ua.png', 1, 0)},  # TODO
            'C': {'walkable': False, 'tileimg': map_t('chainlink.png', 0, 0)},  # chainlink Used
            'c': {'walkable': False, 'tileimg': map_t('carpile.png', 1, 0)},  # TODO
            'D': {'walkable': True, 'tileimg': map_t('dirtandgrasses.png', 0, 0)},  # Dirt Used
            'd': {'walkable': True, 'tileimg': map_t('dirtandgrasses.png', 1, 1)},  # Dirt? Used
            'E': {'walkable': True, 'tileimg': map_t('grass1edges.png', 0, 0)},  # grass1edges
            'e': {'walkable': True, 'tileimg': map_t('grass1edges.png', 1, 0)}, #  grass1edges  Used
            'F': {'walkable': True, 'tileimg': map_t('grass1edges.png', 1, 1)},  # Used
            'f': {'walkable': True, 'tileimg': map_t('grass1edges.png', 0, 1)},
            'G': {'walkable': True, 'tileimg': map_t('grasses.png', 1, 0)},  # Used
            'g': {'walkable': True, 'tileimg': map_t('dirtandgrasses.png', 0, 1)},  # Used
            'J': {'walkable': False, 'tileimg': map_t('midjunkpile3.png', 1, 0)},
            'j': {'walkable': True, 'tileimg': map_t('dirt1tile.png', 0, 0)},  # Used
            'M': {'walkable': True, 'tileimg': map_t('door.png', 0, 0)},  # Mob, large (guard)
            'm': {'walkable': True, 'tileimg': map_t('door.png', 0, 0)},  # Mob, small (dog)
            'P': {'walkable': False, 'tileimg': map_t('carpile.png', 0, 0)},  # Car pile Used
            'p': {'walkable': False, 'tileimg': map_t('carpile.png', 1, 0)},  # Car pile Used
            'Q': {'walkable': False, 'tileimg': map_t('carpile.png', 0, 1)},  # Car pile Used
            'q': {'walkable': False, 'tileimg': map_t('carpile.png', 1, 1)},  # Car pile Used
            'S': {'walkable': True, 'tileimg': map_t('door.png', 0, 0)},  # Spawn Used
            'x': {'walkable': False, 'tileimg': map_t('Golem_3d_paint.png', 0, 0)},  # Golem Used
            'y': {'walkable': False, 'tileimg': map_t('Golem_3d_paint.png', 0, 0)},  # Golem part Used
            'Z': {'walkable': True, 'tileimg': map_t('door.png', 0, 0)},  # Entrance
            'z': {'walkable': True, 'tileimg': map_t('door.png', 0, 0)}  # Exit

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
