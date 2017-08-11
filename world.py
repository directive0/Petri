import biomass
from substrate import *
import random
#the world maintains the location of all organisms, monitors climate and food levels, determines biomass density, and controls updates.
class World(object):
    
    def __init__(self):
        self.stagex = 320
        self.stagey = 240
        self.started = 1
        self.population = []
        
    def getpop(self):
        return self.population
            
    def birth(self,locx,locy,organisms):
        print("birthing a new organism at " + str(locx) + " and " + str(locy))
        self.population.append(organism("meat",10,10,locx,locy,120,10,10,organisms))
        
    def starter(self,organisms):
        for i in range(5):
            self.newlocx = random.randint(0,self.stagex)
            self.newlocy = random.randint(0,self.stagey)
            self.birth(self.newlocx,self.newlocy,organisms)
            
    def update(self,organisms): 
        if self.started == 1:
            self.starter(organisms)
            self.started = 0
        
        for x in self.population:
            x.update(self)
            self.info = x.getstatus()

class organism(object):

    def __init__(self,type,span,food,locationx,locationy,burn,attack,defend,organismlist):
        self.genes={'type':type, 'span':span,'food':food,'burn':burn,'attack':attack,'defend':defend}
        self.genes['state']= 'defined'
        self.x = locationx
        self.y = locationy
        burnadjust = random.randint(-100,100)
        self.burn = burn + burnadjust
        self.sex = random.randint(0,1)
        self.status = {'alive' : True, 'pregnant': False, 'sick': False, 'age' : 0, 'sex' : self.sex, "locx" : self.x, "locy" : self.y }
        self.randomdist = 0
        self.sprite = OrganismSprite(self.x,self.y,self.sex)
        organismlist.add(self.sprite)
        self.organismlist = organismlist
                #organism chooses a direction and a distance, moves in that direction for a distance and then stops and redos.
            
    def eat(self):
        pass

    def sleep(self):
        pass

    def getgenes(self):
        return self.genes
        
    def getstatus(self):
        self.statsforsend = {'alive' : self.status['alive'], 'pregnant': self.status['pregnant'], 'sick': self.status['sick'], 'age' : self.status['age'], 'sex' : self.sex, "locx" : self.x, "locy" : self.y }
        return self.statsforsend  
        
    def mate(self):
        if self.sex == 0:
            if self.status["pregnant"] == True:
                pass
            else:
                self.gestation = 200
                self.status["pregnant"]= True

    def update(self,world):

        
        if self.status['age'] >= self.burn:
            self.status['alive'] = False
        
        if self.status['alive']:
            
            if self.randomdist == 0:
                self.randomx = random.randint(0,2)
                self.randomy = random.randint(0,2)
                self.randomdist = random.randint(1,20)
            
            if self.randomdist != 0:
                if self.randomx == 0:
                    self.x += 1
                
                if self.randomx == 1:
                    self.x -= 1
                    
                if self.randomy == 0:
                    self.y += 1
                
                if self.randomy == 1:
                    self.y -= 1

            
                if self.x >= 310:
                    self.x = 310
            
                if self.x <= 0:
                    self.x =0
            
                if self.y >= 230:
                    self.y = 230
            
                if self.y <= 0:
                    self.y = 0
                
                self.randomdist -= 1
                
            self.status["age"] += .1
                
            self.sprite.update(self.x,self.y)
            
            if self.status["pregnant"]:
                self.gestation -= 1
                
                if self.gestation == 0:
                    self.status["pregnant"] = False
                    world.birth(self.x,self.y,self.organismlist) 
                    
            if self.sprite.collide(self.organismlist) == "mate":
                self.mate()
                print("mated!")
        else:
            self.organismlist.remove(self.sprite)
        

            
class vegetation(object,):
    
    def __init__(self,type,span,location,burn,attack,defend):
        pass
    
    def grow(self):
        pass
        
    def die(self):
        pass
    
    def waseaten(self):   
        pass

