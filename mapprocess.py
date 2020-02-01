import pygame

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

def gettileimg(tile):
    tileimg = None
    if tile == '0':
        tileimg = pygame.image.load("graphics/tiles/0.png").subsurface((0, 32, 32, 32))
    elif tile == 'A':
        tileimg = pygame.image.load("graphics/tiles/ua.png").subsurface((0, 32, 32, 32))
    return tileimg

def blittilemap(screen, maplist):

    for rowIndex in range(0, len(maplist), 1):
        for colIndex in range(0, len(maplist[rowIndex]), 1):
            tile = maplist[rowIndex][colIndex]
            screen.blit(
                gettileimg(tile),
                (32*colIndex, 32*rowIndex)
            )
