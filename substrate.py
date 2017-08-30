#! /usr/bin/python

import pygame
from pygame.locals import *
black = (0,0,0)
pygame.init()
pygame.font.init()
import time 


pygame.key.set_repeat(500,30)
        
#Colour Standards:
white = (255,255,255)
retrogreen = (0,255,50)
retroblue = (136,175,255)

#screenSize = (320,240)
modes = pygame.display.list_modes(16)
#surface = pygame.display.set_mode(screenSize)
backpanel = pygame.image.load("assets/backpanel.png")
plant1 = pygame.image.load("assets/plant1.png")
plant2 = pygame.image.load("assets/plant2.png")
plant3 = pygame.image.load("assets/plant3.png")
plant4 = pygame.image.load("assets/plant4.png")
plant5 = pygame.image.load("assets/plant5.png")
petrinm = pygame.image.load("assets/petrinm.png")
petrinf  = pygame.image.load("assets/petrinf.png")
petrinma = pygame.image.load("assets/petrinma.png")
petrinfa = pygame.image.load("assets/petrinfa.png")
pygame.display.set_caption('Petri Dish Alpha 1')
consoletext = pygame.font.Font("assets/arcade.ttf", 12, bold=False, italic=False)
digitaltext = pygame.font.Font("assets/digital.ttf", 12, bold=False, italic=False)

class FaunaSprite(pygame.sprite.Sprite):

    def __init__(self,x,y,status):
        super(FaunaSprite,self).__init__()
        self.size=(10,10)
        self.color=(255,255,255)
        self.status = status
        self.sex = status["sex"]
        if self.sex == 0:
            self.image = petrinf
        else:
            self.image = petrinm
            
        self.rect = self.image.get_rect()
        
        self.rect.y = y
        self.rect.x = x

    def getsize(self):
        return self.image.get_size()

    def mature(self):
        if self.sex == 0:
            self.image = petrinfa
        else:
            self.image = petrinma

    def test(self):
        return "weeeehaaaaaa"

    def getstatus(self):
        return self.status

    def collide(self,list,mode):
        collisions = pygame.sprite.spritecollide(self, list, False)
        
        if mode == 0:
            for x in collisions:
                targetstatus = x.getstatus()
                if self.sex == 0 and self.sex != targetstatus["sex"]:
                    if self.status["mature"] and targetstatus["mature"]:
                        return True
                    else:
                        return False
        else:
            for x in collisions:
                targetstatus = x.getstatus()
                if targetstatus["fruit"]:
                    targetstatus['fruit'] = False
                    x.waseaten()
                    targetstatus['maturelevel'] = 1
                    self.status['hunger'] = 100
                    print str(self) + " Says: 'I ated the purple berry'"
                    return True
                else:
                    return False

    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y
       
class FloraSprite(pygame.sprite.Sprite):

    def __init__(self,x,y,status,obj):
        super(FloraSprite,self).__init__()
        self.size=(10,10)
        self.color=(255,255,255)
        self.status = status
        self.image = plant1   
        self.rect = self.image.get_rect()
        
        self.rect.y = y
        self.rect.x = x
        
    def getstatus(self):
        return self.status
        
    def getsize(self):
        return self.image.get_size()
        
    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    def waseaten(self):
        self.status['maturelevel'] = 1
        self.mature(1)
        
    def mature(self,level):
        
        #sprout
        if level == 1:
            self.image = plant2 
         
        if level == 2:
            self.image = plant3
        
        if level == 3:
            self.image = plant4
        
        #fully grown with fruit
        if level == 4:
            self.image = plant5
        
class ControlPanel(object):
    def __init__(self,surface,gameinfo):
        self.gameinfo = gameinfo
        self.background = backpanel
        self.panel = Image()
        self.panel.update(self.background,0,0)
        self.surface = surface
        self.label = Label()

        
    def arrangetext(self,population):
        self.popinfo = {"mortality" : 0, "pregs" : 0,"avage":0}
        for x in population:
            information = x.getstatus()
            if information["alive"]:
                self.popinfo["mortality"] +=1
                if information["pregnant"]:
                    self.popinfo["pregs"] +=1
    
            self.popinfo["avage"] += information["age"]
        
        if len(population) > 0:
            average = self.popinfo["avage"] / len(population)
        else:
            average = 0
            
        self.textinfo =(("Population: " + str(self.popinfo["mortality"])),("Pregnancies: " + str(self.popinfo["pregs"])),("Average Age: " + str(int(average))))
    
    def displaylcd(self):
        self.lcd1 = Label()
        self.lcd2 = Label()
        content = str(self.gameinfo['spawnfauna'])

        
        content2 = str(self.gameinfo['spawnflora'])
        self.lcd1.update(content,23,12,261,"assets/digital.ttf",retroblue)
        self.lcd1.draw(self.surface)
        self.lcd2.update(content2,23,12,322,"assets/digital.ttf",retroblue)
        self.lcd2.draw(self.surface)
        
    
    def draw(self,population):
        self.panel.draw(self.surface)
        self.arrangetext(population)
        index = 0
        ypos = 38
        textheight = 16
        for n in self.textinfo:
            self.n = Label()
            self.n.update(self.textinfo[index],13,13,ypos,"assets/arcade.ttf",retrogreen)
            self.n.draw(self.surface)
            ypos += textheight
            index += 1
        self.displaylcd()
        #self.label.update(info,13,13,38,"assets/arcade.ttf",white)
        #self.label.draw(self.surface)

        
class Image(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.Img = backpanel
        
    def update(self, image, nx, ny):
        self.x = nx
        self.y = ny
        self.Img = image

        
    def draw(self, surface):
        surface.blit(self.Img, (self.x,self.y))
        
class Label(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = white
        self.fontSize = 33
        self.myfont = pygame.font.Font("assets/arcade.ttf", self.fontSize)
        
    def update(self, content, fontSize, nx, ny, fontType, color):
        self.x = nx
        self.y = ny
        self.content = content
        self.fontSize = fontSize
        self.myfont = pygame.font.Font(fontType, self.fontSize)
        self.color = color
        
    def draw(self, surface):
        label = self.myfont.render(self.content, 1, self.color)
        surface.blit(label, (self.x, self.y))

class Timer(object):

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
        
    def update(self,x,y,size):
        self.x += x
        self.y += y
        self.size = size

    
    def draw(self, surface):
        rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, rect)
        
def getmouse():
    mpress = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    return mpos,mpress

def getevents():
    pygame.event.get()
    
    key = pygame.key.get_pressed()
    return key

    
tock = Timer()

class substrate(object):
    def __init__(self,gameinfo):
        self.gameinfo = gameinfo
        self.screenSize = self.gameinfo['size']
        
        if gameinfo['target'] == 'desktop':
            self.surface = pygame.display.set_mode(self.screenSize)
        elif gameinfo['target'] == 'pandora':
            self.surface = pygame.display.set_mode(self.screenSize,pygame.FULLSCREEN)
            #pygame.event.set_blocked(pygame.MOUSEMOTION)
            #pygame.mouse.set_visible(0)
    
        self.sidepanel = ControlPanel(self.surface,gameinfo)
        self.status = 'game'

    def clickcheck(self,mouse,corl,corr):
        mx,my = mouse
        
        if mx >= corl[0] and mx <= corr[0]:
            if my >= corl[1] and my <= corr[1]:
                return True
    
    def clicked(self):
        status = 'game'        
        
        pressed = pygame.key.get_pressed()
        
      
        events = pygame.event.get()

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.status = "quit"
                elif e.key == K_DOWN:
                    self.gameinfo['spawnflora'] -= 1
                elif e.key == K_UP:
                    self.gameinfo['spawnflora'] += 1
                elif e.key == K_LEFT:
                    self.gameinfo['spawnfauna'] -= 1
                elif e.key == K_RIGHT:
                    self.gameinfo['spawnfauna'] += 1
                elif e.key == K_UP and e.key == K_RIGHT:
                    self.gameinfo['spawnfauna'] += 1
                    self.gameinfo['spawnflora'] += 1
                elif e.key == K_r:
                    status = "restart"
                elif e.key == K_q:
                    status = "quit"
                  
        mouse,mbutt = getmouse()
        
        if mbutt == (1,0,0):

            fapl,fapr = self.gameinfo['faplus']
            fanl,fanr = self.gameinfo['faneg']
            flpl,flpr = self.gameinfo['flplus']
            flnl,flnr = self.gameinfo['flneg']
            gbutl,gbutr = self.gameinfo['gbutt']
            rbutl,rbutr = self.gameinfo['rbutt']
            
            if self.clickcheck(mouse,fapl,fapr):
                self.gameinfo['spawnfauna'] += 1

            if self.clickcheck(mouse,fanl,fanr):
                self.gameinfo['spawnfauna'] -= 1
                
            if self.clickcheck(mouse,flpl,flpr):
                self.gameinfo['spawnflora'] += 1

            if self.clickcheck(mouse,flnl,flnr):
                self.gameinfo['spawnflora'] -= 1
                
            if self.clickcheck(mouse,gbutl,gbutr):
                status = 'restart'
            
            if self.clickcheck(mouse,rbutl,rbutr):
                status = 'quit'
            
        if self.gameinfo["spawnflora"] < 0:
            self.gameinfo["spawnflora"] = 0
        
        if self.gameinfo["spawnfauna"] < 0:
            self.gameinfo["spawnfauna"] = 0
                    
        return status
        
        
    def draw(self,organisms,plants,pop,ppop,world):
        
        self.surface.fill(black)

        for x in pop:
            x.update(world)

        for x in ppop:
            x.update(world)

        self.status = self.clicked()

 
            
            

        
        plants.draw(self.surface)
        organisms.draw(self.surface)
        self.sidepanel.draw(pop)
        pygame.display.flip()
        return self.status
    
    
class menu(object):
    pass
