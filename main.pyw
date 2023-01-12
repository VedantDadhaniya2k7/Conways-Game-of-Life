# IMPORTS
import pygame
import time


# CONSTANTS
WORLD_SZ = (100, 100)
TILE_SZ = 9


# WORLD INITIALIZATION
world = pygame.display.set_mode((WORLD_SZ[0] * TILE_SZ + WORLD_SZ[0] + 1, WORLD_SZ[1] * TILE_SZ + WORLD_SZ[1] + 1))
pygame.display.set_caption("Conway's Game of Life")
x, y = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()

# Creates a 2D binary list to conatin cell information ( True is alive, False is Dead )
env = [[False for c in range(WORLD_SZ[0])] for r in range(WORLD_SZ[1])]



# FUNCTIONS
def livenCell(tile_pos):
    """
    Converts the given tile to a live one
    """
    
    env[tile_pos[1]][tile_pos[0]] = True

def killCell(tile_pos):
    """
    Converts the given tile to a dead one
    """
    
    env[tile_pos[1]][tile_pos[0]] = False

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
            
def fate(tile_pos):
    """
    Return True if the tile at the given position needs to be flipped ( Alive <---> Dead )
    False otherwise
    """
    
    aliveNeighbours = 0
    for cell in get_neighbours(tile_pos):
        if 0 <= cell[1] < len(env):
            if 0 <= cell[0] < len(env[cell[1]]):
                if env[cell[1]][cell[0]] == True:
                    aliveNeighbours += 1
        else:
            pass

    if env[tile_pos[1]][tile_pos[0]]:
        if 2 <= aliveNeighbours <= 3:
            # Tile remains alive
            return False
        else :
            # Tile dies
            return True
    else:
        if aliveNeighbours == 3:
            # Tile becomes alive 
            return True
        else:
            # Tile remains dead
            return False

def nextGen():
    """
    Comences the next generation
    """

    # a list to record cells who's identity(dead/alive) needs to be flipped
    newFate = []

    for r in range(len(env)):
        for c in range(len(env[r])):
            if fate((c,r)) == True:
                newFate.append((c,r))
            else:
                pass

    # flips the identity of all cell in the newFate list
    for pos in newFate:
        if env[pos[1]][pos[0]]:
            killCell(pos)
        else:
            livenCell(pos)

def drawWorld(win):
    """
    Updates the pygame window to all changes to the environment
    """
    world.fill((250, 248, 239))

    # Draws all vertical grid lines
    a = 0
    for i in range(0, x):
        if (a%(TILE_SZ + 1) == 0):
            pygame.draw.line(world, (150, 175, 200), (i,0), (i, y-1))
        a += 1

    # Draws all horizontal grid lines
    b = 0
    for j in range(0, y):
        if (b%(TILE_SZ + 1) == 0):
            pygame.draw.line(world, (150, 175, 200), (0,j), (x-1, j))
        b += 1

    # Draws all live cells in the environment
    for r in range(len(env)):
        for c in range(len(env[r])):
            if env[r][c]:
                pygame.draw.rect(win, (0,0,0), (((c*TILE_SZ)+c+1), ((r*TILE_SZ)+r+1), TILE_SZ, TILE_SZ))
    

# MAIN
run = True
playSim = False

# Time gap between two generations
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
                    # Turn off the simulation 
                    playSim = False
                    
                elif event.button == 4 and phaseTime >= 0.05:
                    # Increses the simulation speed
                    phaseTime -= .05
                    
                elif event.button == 5:
                    # Decreases the simulation speed
                    phaseTime += .05

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 1:
                    # Turns te tile at given mouse position to a live one
                    
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0]//(TILE_SZ+1), pos[1]//(TILE_SZ+1))
                    livenCell(pos)
                    
                elif event.button == 3:
                    # Turns te tile at given mouse position to a dead one
                    
                    pos = pygame.mouse.get_pos()
                    pos = (pos[0]//(TILE_SZ+1), pos[1]//(TILE_SZ+1))
                    killCell(pos)
                    
                elif event.button == 2:
                    # Turn on the simulation
                    
                    playSim = True
                    
                elif event.button == 4 and phaseTime >= 0.05:
                    # Increses the simulation speed
                    
                    phaseTime -= .05
                    
                elif event.button == 5:
                    # Decreases the simulation speed
                    
                    phaseTime += .05

    drawWorld(world)
    pygame.display.update()

pygame.display.quit()
