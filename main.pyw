# IMPORTS
import pygame
import time


# CONSTANTS
WORLD_SZ = (100, 100)
TILE_SZ = 9


# WORLD INITIALIZATION
world = pygame.display.set_mode((WORLD_SZ[0] * TILE_SZ + WORLD_SZ[0] + 1, WORLD_SZ[1] * TILE_SZ + WORLD_SZ[1] + 1))
pygame.display.set_caption("Conway's Game of Life")

env = [[False for c in range(WORLD_SZ[0])] for r in range(WORLD_SZ[1])]

x, y = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()


# FUNCTIONS
def livenCell(pos):
    """
    Converts the tile at a given mouse position to a live one
    """
    
    env[pos[1]][pos[0]] = True

def killCell(pos):
    """
    Converts the tile at a givens position to a dead one
    """
    
    env[pos[1]][pos[0]] = False

def get_neighbours(pos):
    """
    Returns a list of positions of tiles which may exist relative to the give tile
    """
    
    return ((pos[0]-1, pos[1]-1),
            (pos[0], pos[1]-1),
            (pos[0]+1, pos[1]-1),
            (pos[0]-1, pos[1]),
            (pos[0]+1, pos[1]),
            (pos[0]-1, pos[1]+1),
            (pos[0], pos[1]+1),
            (pos[0]+1, pos[1]+1))
            
def fate(pos):
    """
    Return True if the tile at the given position needs to be flipped ( Alive <---> Dead )
    False otherwise
    """
    
    aliveNeighbours = 0
    for cell in get_neighbours(pos):
        try:
            if env[cell[1]][cell[0]] == True:
                aliveNeighbours += 1
        except:
            pass

    if env[pos[1]][pos[0]]:
        if 2 <= aliveNeighbours <= 3:
            return False
        else :
            return True
    else:
        if aliveNeighbours == 3:
            return True
        else:
            return False

def nextGen():
    """
    Comences the next generation
    """

    newFate = []

    for r in range(len(env)):
        for c in range(len(env[r])):
            if fate((c,r)) == True:
                newFate.append((c,r))
            else:
                pass

    for pos in newFate:
        if env[pos[1]][pos[0]]:
            killCell(pos)
        else:
            livenCell(pos)

def drawWorld(win):
    world.fill((250, 248, 239))

    a = 0
    for i in range(0, x):
        if (a%(TILE_SZ + 1) == 0):
            pygame.draw.line(world, (150, 175, 200), (i,0), (i, y-1))
        a += 1
    b = 0
    for j in range(0, y):
        if (b%(TILE_SZ + 1) == 0):
            pygame.draw.line(world, (150, 175, 200), (0,j), (x-1, j))
        b += 1
    for r in range(len(env)):
        for c in range(len(env[r])):
            if env[r][c]:
                pygame.draw.rect(win, (0,0,0), (((c*TILE_SZ)+c+1), ((r*TILE_SZ)+r+1), TILE_SZ, TILE_SZ))
    

# MAIN
run = True
playSim = False
phaseTime = 0.25

while run:
    time.sleep(phaseTime)
    if playSim == True:
        nextGen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 2:
                    playSim = False
                elif event.button == 4 and phaseTime != 0:
                    phaseTime -= .05
                elif event.button == 5:
                    phaseTime += .05

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0]//(TILE_SZ+1), pos[1]//(TILE_SZ+1))
                    livenCell(pos)
                elif event.button == 3:
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0]//(TILE_SZ+1), pos[1]//(TILE_SZ+1))
                    killCell(pos)
                elif event.button == 2:
                    playSim = True
                elif event.button == 4 and phaseTime <= .06:
                    phaseTime -= .05
                elif event.button == 5:
                    phaseTime += .05

    drawWorld(world)
    pygame.display.update()

pygame.display.quit()
