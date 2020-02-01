import pygame

TILE_WIDTH = 32
TILE_HEIGHT = 32

tileimgs = {
    '0': {
        "movable": True,
        "tileimg": pygame.image.load("graphics/tiles/0.png").subsurface((0, TILE_HEIGHT*1, TILE_WIDTH, TILE_HEIGHT))
    },
    'A': {
        "movable": False,
        "tileimg": pygame.image.load("graphics/tiles/ua.png").subsurface((0, TILE_HEIGHT*1, TILE_WIDTH, TILE_HEIGHT))
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
