#! /usr/bin/python
#petri dish. my attempt a a game of life.
#c.barrett, guidestar interplanetary.
from world import *
from substrate import *
import pygame
import os

pygame.init()

organisms = pygame.sprite.Group()
plants = pygame.sprite.Group()

go = True

status = "startup"

gameinfo = {'target': 'desktop','size': (800,480), 'spawnfauna' : 100, 'spawnflora' : 100, 'faplus': ((124,259),(151,286)),'faneg':((92,259),(119,286)),'flplus':((124,320),(151,347)),'flneg':((92,320),(119,347)), 'gbutt' : ((22,415),(60,452)), 'rbutt' : ((99,417),(136,454))}

def printinfo(population):
    os.system("clear")
    popinfo = {"mortality" : 0, "pregs" : 0,"avage":0}
    for x in population:
        information = x.getstatus()
        if information["alive"]:
            popinfo["mortality"] +=1
            if information["pregnant"]:
                popinfo["pregs"] +=1
        
        popinfo["avage"] += information["age"]
    
    average = popinfo["avage"] / len(population)
        
    print("Population: " + str(popinfo["mortality"]))
    print("Pregnancies: " + str(popinfo["pregs"]))
    print("Average Age: " + str(int(average)))
    
    
    


while go:

    if status == "startup":
        world1 = World(gameinfo)
        sub = substrate(gameinfo)
        status =  "game"
    
    
    if status == "game":
        world1.update(organisms,plants)
        population = world1.getpop()
        plantpopulation = world1.getppop()
        status = sub.draw(organisms,plants,population,plantpopulation,world1)
        pygame.time.wait(50)
        
    if status == 'stop':
        pass
        
    if status == "restart":
        organisms.empty()
        plants.empty()
        status = "startup"
        
    if status == 'quit':
        go = False
    
    #printinfo(population)
