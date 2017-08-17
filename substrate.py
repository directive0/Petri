import pygame
black = (0,0,0)
pygame.init()
pygame.font.init()
import time 

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

petrinm = pygame.image.load("petrinm.png")
petrinf  = pygame.image.load("petrinf.png")
petrinma = pygame.image.load("petrinma.png")
petrinfa = pygame.image.load("petrinfa.png")
pygame.display.set_caption('Petri Dish Alpha 1')
consoletext = pygame.font.Font("assets/arcade.ttf", 10, bold=False, italic=False)
digitaltext = pygame.font.Font("assets/digital.ttf", 10, bold=False, italic=False)

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

    def collide(self,list):
        collisions = pygame.sprite.spritecollide(self, list, False)

        for x in collisions:
            targetstatus = x.getstatus()
            if self.sex == 0 and self.sex != targetstatus["sex"]:
                if self.status["mature"] and targetstatus["mature"]:
                    return "mate"

    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y
       
class FloraSprite(pygame.sprite.Sprite):

    def __init__(self,x,y,status):
        super(FloraSprite,self).__init__()
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

        average = self.popinfo["avage"] / len(population)
    
        self.textinfo =(("Population: " + str(self.popinfo["mortality"])),("Pregnancies: " + str(self.popinfo["pregs"])),("Average Age: " + str(int(average))))
    
    def displaylcd(self):
        self.lcd1 = Label()
        content = str(self.gameinfo['spawnfauna'])
        self.lcd1.update(content,23,12,264,"assets/digital.ttf",retroblue)
        self.lcd1.draw(self.surface)
    
    def draw(self,population):
        self.panel.draw(self.surface)
        self.arrangetext(population)
        index = 0
        ypos = 38
        textheight = 16
        print(self.textinfo)
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
    
        self.sidepanel = ControlPanel(self.surface,gameinfo)
        self.status = 'game'

    def draw(self,organisms,pop,world):
        #all_sprites_list.clear(surface,black)
        self.surface.fill(black)
    
        for x in pop:
            x.update(world)
        
        key = getevents()
        
        if key[pygame.K_q]:
            self.status = 'quit'
    
        if key[pygame.K_r]:
            self.status = "restart"
        
        mouse,mbutt = getmouse()
        
        if mbutt == (1,0,0):
            mx,my = mouse
            if mx > 22 and mx < 60:
                if my > 415 and my < 452:
                    self.gameinfo['spawnfauna'] += 1
            
        
        organisms.draw(self.surface)
        self.sidepanel.draw(pop)
        pygame.display.flip()
        return self.status
        #pygame.time.wait(50))
    
    
    
class menu(object):
    pass
