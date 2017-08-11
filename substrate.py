import pygame
black = (0,0,0)
pygame.init()
pygame.font.init()
import time 
import os

screenSize = (320,240)
modes = pygame.display.list_modes(16)
surface = pygame.display.set_mode(screenSize)
petrinm = pygame.image.load("petrinm.png")
petrinf  = pygame.image.load("petrinf.png")

pygame.display.set_caption('Petri Dish Alpha 1')
petrin = pygame.image.load('petrin.png')
class OrganismSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,sex):
        super(OrganismSprite,self).__init__()
        self.size=(10,10)
        self.color=(255,255,255)
        self.sex = sex
        if self.sex == 0:
            self.image = petrinf
        else:
            self.image = petrinm
            
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def test(self):
        return "weeeehaaaaaa"
       
    def getsex(self):
        return self.sex
            
    def collide(self,list):
        collisions = pygame.sprite.spritecollide(self, list, False)
        
        for x in collisions:
            targetsex = x.getsex()
            if self.sex == 0 and self.sex != targetsex:
                return "mate"


            
    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y
        
class timer(object):

    # Constructor code logs the time it was instantiated.    
    def __init__(self):
        self.timeInit = time.time()

    # The following funtion returns the last logged value.        
    def timestart(self):
        return self.timeInit
        
    # the following function updates the time log with the current time.
    def logtime(self):
        self.lastTime = time.time()

    # the following function returns the interval that has elapsed since the last log.        
    def timelapsed(self):
        self.timeLapse = time.time() - self.lastTime
        #print(self.timeLapse)
        return self.timeLapse
        
class Box(object):
    def __init__(self):
        self.x=0
        self.y=0
        self.size=(10,10)
        self.color=(255,255,255)
        
    def update(self,x,y):
        self.x += x
        self.y += y

    
    def draw(self, surface):
        rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, rect)


tock = timer()

def subdraw(organisms,pop,world):
    
    #all_sprites_list.clear(surface,black)
    surface.fill(black)
    
    for x in pop:
        x.update(world)
        
    

        

    organisms.draw(surface)    
    pygame.display.flip()
    #pygame.time.wait(50)
    os.system("clear")
    