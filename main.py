#petri dish. my attempt a a game of life.
#c.barrett, guidestar interplanetary.
from biomass import *
from world import *
from substrate import *
import pygame

pygame.init()


world1 = World()
go = True

while go:
    pygame.event.get()
    key = pygame.key.get_pressed()

    if key[pygame.K_q]:
        go = False

        
    world1.update()
    population = world1.getpop()
    
    subdraw(surface,population)
