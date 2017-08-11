#petri dish. my attempt a a game of life.
#c.barrett, guidestar interplanetary.
from world import *
from substrate import *
import pygame

pygame.init()

organisms = pygame.sprite.Group()

go = True

status = "startup"



while go:
    
    
    if status == "startup":
        world1 = World()
        status =  "game"
    
    
    pygame.event.get()
    key = pygame.key.get_pressed()

    if key[pygame.K_q]:
        go = False
    
    if key[pygame.K_r]:
        status = "restart"
    
    
    if status == "game":
        print("startup over")
        world1.update(organisms)
        population = world1.getpop()
        subdraw(organisms,population,world1)
        pygame.time.wait(50)
        
    if status == "restart":
        organisms.empty()
        status = "startup"
