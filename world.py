#! /usr/bin/python

from substrate import *
import random
from math import sin, cos, pi, atan2
import pygame as pg

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)

def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))


#the world maintains the location of all organisms, monitors climate and food levels, determines biomass density, and controls updates.
class World(object):
    
    def __init__(self,gameinfo):
        self.gameinfo = gameinfo
        self.stagex, self.stagey = self.gameinfo['size']
        self.started = 1
        self.population = []
        self.plantpop = []
    
    def getppop(self):
        return self.plantpop
            
    def getpop(self):
        return self.population
        
    def checkpop(self):
        deadcheck = 0
        for x in self.population:
            if x.getstatus["alive"]:
                deadcheck += 1
            else:
                pass
        if deadcheck == 0:
            return False
        else:
            return True
            
    def createfauna(self,locx,locy,organisms,plants):
        self.population.append(Fauna(True,10,10,locx,locy,120,10,10,organisms,self.stagex,self.stagey,plants))

    def createflora(self,locx,locy,plants,organisms,start):
        pass
        self.plantpop.append(Flora(True,True,locx,locy,True,plants,self.stagex,self.stagey,start))
            
    def birth(self,locx,locy,organisms,plants):
        litter = random.randint(0,2)
        for x in range(litter):
            self.population.append(Fauna(False,10,10,locx,locy,120,10,10,organisms,self.stagex,self.stagey,plants))
        
    def starter(self,organisms,plants):
        
        if self.gameinfo['spawnfauna']:
            for i in range(self.gameinfo['spawnfauna']):
                self.newlocx = random.randint(160,self.stagex)
                self.newlocy = random.randint(0,self.stagey)
                self.createfauna(self.newlocx,self.newlocy,organisms,plants)
        
        if self.gameinfo['spawnflora'] > 0:
            for i in range(self.gameinfo['spawnflora']):
                self.newlocx = random.randint(160,self.stagex)
                self.newlocy = random.randint(0,self.stagey)
                self.createflora(self.newlocx,self.newlocy,plants,organisms,False)
            
    def update(self,organisms,plants): 
        if self.started == 1:
            self.starter(organisms,plants)
            self.started = 0
        
        for x in self.population:
            x.update(self)
            self.info = x.getstatus()

class Fauna(object):


    def __init__(self,predator,span,food,locationx,locationy,burn,attack,defend,organismlist,stagex,stagey,plantlist):
        
        # generates a genetic marker set
        self.genes={'type':type, 'span':span,'food':food,'burn':burn,'attack':attack,'defend':defend,"gestation":20}
        
        # places organism at location defined
        self.x = locationx
        self.y = locationy
        
        # size of play field
        self.stagex = stagex
        self.stagey = stagey
        
        # lifespan randomization
        burnadjust = random.randint(-100,100)
        self.burn = burn + burnadjust
        
        # assigns sex
        self.sex = random.randint(0,1)
        
        #assigns deviation
        self.deviate = random.randint(-15,15)
        
        # assigns organisms state
        self.status = {'alive' : True, 'pregnant': False, 'sick': False, 'age' : 0, 'sex' : self.sex, "locx" : self.x, "locy" : self.y, "mature" : False,'hunger' : 50, 'found' : False }        
        # variable controls distance to be walked per direction decision
        self.randomdist = 0
        
        # creates a sprite object for this organism and passes it the status to help with collisions
        self.sprite = FaunaSprite(self.x,self.y,self.status)
        
        # adds organism to sprite list
        organismlist.add(self.sprite)
        
        # adds the organismlist to this object for further use
        self.organismlist = organismlist
        self.plantlist = plantlist
        self.sizesprite()
        self.speed = random.randint(1,3)
        
        
    
    def sizesprite(self):    
        # reads the size of the sprite (for boundries)
        self.sizex,self.sizey = self.sprite.getsize()
        

    # moves the organism randomly
    def randomove(self):
    #organism chooses a direction and a distance, moves in that direction for a distance and then stops and redos.
    
        if self.randomdist == 0:
            self.randomx = random.randint(0,2)
            self.randomy = random.randint(0,2)
            self.randomdist = random.randint(1,100)
        
        if self.randomdist != 0:
            if self.randomx == 0:
                self.x += 1
            
            if self.randomx == 1:
                self.x -= 1
                
            if self.randomy == 0:
                self.y += 1
            
            if self.randomy == 1:
                self.y -= 1

        
            if self.x >= self.stagex - self.sizex:
                self.x = self.stagex - self.sizex
        
            if self.x <= 160:
                self.x =160
        
            if self.y >= self.stagey - self.sizey:
                self.y = self.stagey - self.sizey
        
            if self.y <= 0:
                self.y = 0
            
            self.randomdist -= 1
            
        self.sprite.update(self.x,self.y)
    
    # will handle sleeping and unconciousness
    def sleep(self):
        pass
    
    # returns the genetic markers for this organism
    def getgenes(self):
        return self.genes
    
    # returns the status of this organism
    def getstatus(self):
        return self.status 
        
    # processes the initialization of pregnancy
    def mate(self):
        if self.sex == 0:
            if self.status["pregnant"] == True:
                pass
            else:
                self.gestation = self.genes["gestation"]
                self.status["pregnant"]= True

    # updates the organisms various functions. Like a clock tick.
    def mature(self):
    # Assigns sexual maturity
        if self.sex == 0:
            if self.status["age"] >= (25 + self.deviate) and self.status["age"] <= (180 + self.deviate):
                self.status["mature"] = True
                self.sprite.mature()
                self.sizesprite()
        else:
            if self.status["age"] >= (30 + self.deviate):
                self.status["mature"] = True
                self.sprite.mature() 
                self.sizesprite()
    
    def gestate(self,world):
        
        # Handles gestation.
        if self.status["pregnant"]:
            self.gestation -= 1
            
            if self.gestation == 0:
                self.status["pregnant"] = False
                world.birth(self.x,self.y,self.organismlist,self.plantlist) 

    def collide(self,list,mode):
        #checks to see if a collision with a male occured
        if mode == 0:
            if self.sprite.collide(list,mode):
                self.mate()
        else:
            if self.sprite.collide(list,mode):
                self.feed
                
    def feed(self,list):
        pass
    
    def findfood(self):
        
        #print "notfound"
        freshlist = []
        freshdist = []
        
        # find the nearest plant
        # go to it
        for x in self.plantlist:
            xstatus = x.getstatus()
            
            if xstatus['fruit']:
                freshlist.append(x)
        
        #print freshlist
        for x in freshlist:
            xstatus = x.getstatus()
            
            diffx = abs(self.x - xstatus['locx'])
            diffy = abs(self.y - xstatus['locy'])
            freshdist.append((diffx+diffy))
            
        #print freshlist
        if len(freshdist) >=1:
            targetindex = int(freshdist.index(min(freshdist)))
            #print targetindex
            self.status['target'] = freshlist[targetindex]
            
    
            self.tarfood = self.status['target']
            self.tarstat = self.tarfood.getstatus()
            self.targety = self.tarstat['locy']
            self.targetx = self.tarstat['locx']
            self.target_pos = self.targetx,self.targety
            return True
        else:
            return False
        
    def gotofood(self):
        if self.tarstat['fruit']:
            self.pos = self.x,self.y
            self.angle = get_angle(self.pos, self.target_pos)
            self.pos = project(self.pos, self.angle, self.speed)
            self.x,self.y = self.pos
            self.sprite.update(self.x,self.y)
        else:
            self.status['found'] = False
        #if self.tarstat['fruit']:
            
            #if self.y < self.targety:
                #self.y += 1
    
            #if self.y > self.targety:
                #self.y -= 1
    
            #if self.x < self.targetx:
                #self.x += 1
    
            #if self.x > self.targetx:
                #self.x -= 1
    
            #self.sprite.update(self.x,self.y)
    
            ##if self.x == self.targetx and self.y == self.targety:
                ##return True
            ##else:
                ##return False
        #else:
            #self.status['found'] = False
        

        
    
    def age(self):
        self.status["age"] += .1
        
    def update(self,world):
        
        # checks to see if organism has reached its incept date
        #if self.status['age'] >= self.burn:
        #    self.status['alive'] = False
        if self.status['hunger'] <= 0:
            self.status['alive'] = False
        else:
            self.status['hunger'] -= .1
        
        # Runs the standard life routine
        if self.status['alive']:
            
            self.age()

            self.mature()
            
            self.gestate(world)


        
            if self.status['hunger'] >= 40:
                #print "randomove"
                self.randomove()
                self.collide(self.organismlist,0)
            else:
                #print("need noms!")
                if self.findfood():
                    #print "found a target"
                    self.status['found'] = True
                else:
                    self.randomove()
                
                if self.status['found']:
                    self.gotofood()
                    if self.collide(self.plantlist,1):
                        #print "I ated the purple berry"
                        self.status['hunger']=100
                        self.status['found'] = False
        else:
            # if dead remove sprite
            self.organismlist.remove(self.sprite)

# vegetation to be worked out.
class Flora(object,):
    
    def __init__(self,kind,span,locationx,locationy,fruit,plantlist,stagex,stagey,start):
        # generates a genetic marker set
        self.genes={'kind':kind,'span':span,'fruit':fruit}
            
        # places organism at location defined
        self.x = locationx
        self.y = locationy
        self.stagex = stagex
        self.stagey = stagey
        # assigns sex
        self.sex = random.randint(0,1)

        #assigns deviation
        self.deviate = random.randint(-15,15)

        # assigns organisms state
        self.status = {'alive' : True, 'age' : 0, 'sex' : self.sex, "locx" : self.x, "locy" : self.y, "mature" : False, 'fruit' : False, 'start' : start }
        
        self.sprite = FloraSprite(self.x,self.y,self.status,self)
        
        # adds organism to sprite list
        plantlist.add(self.sprite)
        
        # adds the organismlist to this object for further use
        self.plantlist = plantlist
        self.status['maturetick'] = 0
        self.status['maturescaler'] = random.randint(2,20)
        self.status['maturelevel'] = 0
        self.sizesprite()
        self.bound()
        
        if start:
            self.status['mature'] = True
            self.status['fruit'] = True
            self.sprite.mature(4)

    def sizesprite(self):    
        # reads the size of the sprite (for boundries)
        self.sizex,self.sizey = self.sprite.getsize()

    def bound(self):
        if self.x >= self.stagex - self.sizex:
            self.x = self.stagex - self.sizex

        if self.x <= 160:
            self.x =160

        if self.y >= self.stagey - self.sizey:
            self.y = self.stagey - self.sizey

        if self.y <= 0:
            self.y = 0

        self.sprite.update(self.x,self.y)

    def getstatus(self):
        return self.status()
        pass

    def update(self,world):

        #runs the main alive routine every cycle
        self.sizesprite()
        self.bound()

        if self.status['alive']:
            self.status['age'] += .1
        
        if self.status['maturelevel'] < 4:
            self.status['maturetick'] += .1


        if self.status['maturetick'] > self.status['maturescaler']:
            self.status['maturetick'] = 0 
            self.status['maturelevel'] += 1
            self.sprite.mature(self.status['maturelevel'])
        
        if self.status['maturelevel'] == 4:
            self.status['maturetick'] = 0 
            self.status['fruit'] = True


        
        #if self.status['alive']:
            #self.status['age'] += .1
            
            #if self.status['maturelevel'] == 4:
                #self.status['maturetick'] += .1


        
        

    def sprout(self):
        pass

    def die(self):
        pass

    def waseaten(self):   
        self.status['maturelevel'] = 1
        self.status['fruit'] = False
        


