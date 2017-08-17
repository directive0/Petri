import biomass
from substrate import *
import random
#the world maintains the location of all organisms, monitors climate and food levels, determines biomass density, and controls updates.
class World(object):
    
    def __init__(self,gameinfo):
        self.gameinfo = gameinfo
        self.stagex, self.stagey = self.gameinfo['size']
        self.started = 1
        self.population = []
        
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
            
    def createfauna(self,locx,locy,organisms):
        self.population.append(Fauna(True,10,10,locx,locy,120,10,10,organisms,self.stagex,self.stagey))

    def createflora(self,locx,locy,organisms):
        self.population.append(Flora(True,True,locx,locy,True))
            
    def birth(self,locx,locy,organisms):
        litter = random.randint(0,2)
        for x in range(litter):
            self.population.append(Fauna(False,10,10,locx,locy,120,10,10,organisms,self.stagex,self.stagey))
        
    def starter(self,organisms):
        for i in range(self.gameinfo['spawnfauna']):
            self.newlocx = random.randint(160,self.stagex)
            self.newlocy = random.randint(0,self.stagey)
            self.createfauna(self.newlocx,self.newlocy,organisms)
            
        #for i in range(self.gameinfo['spawnflora']):
            #self.newlocx = random.randint(160,self.stagex)
            #self.newlocy = random.randint(0,self.stagey)
            #self.createfauna(self.newlocx,self.newlocy,organisms)
            
    def update(self,organisms): 
        if self.started == 1:
            self.starter(organisms)
            self.started = 0
        
        for x in self.population:
            x.update(self)
            self.info = x.getstatus()

class Fauna(object):


    def __init__(self,predator,span,food,locationx,locationy,burn,attack,defend,organismlist,stagex,stagey):
        
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
        self.status = {'alive' : True, 'pregnant': False, 'sick': False, 'age' : 0, 'sex' : self.sex, "locx" : self.x, "locy" : self.y, "mature" : False }
        
        # variable controls distance to be walked per direction decision
        self.randomdist = 0
        
        # creates a sprite object for this organism and passes it the status to help with collisions
        self.sprite = FaunaSprite(self.x,self.y,self.status)
        
        # adds organism to sprite list
        organismlist.add(self.sprite)
        
        # adds the organismlist to this object for further use
        self.organismlist = organismlist
        self.sizesprite()
    
    def sizesprite(self):    
        # reads the size of the sprite (for boundries)
        self.sizex,self.sizey = self.sprite.getsize()
        

    # moves the organism randomly
    def randomove(self):
    #organism chooses a direction and a distance, moves in that direction for a distance and then stops and redos.
    
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
                world.birth(self.x,self.y,self.organismlist) 

    def collide(self):
        #checks to see if a collision with a male occured
        if self.sprite.collide(self.organismlist) == "mate":
            self.mate()
    
    def age(self):
        self.status["age"] += .1
        
    def update(self,world):
        
        # checks to see if organism has reached its incept date
        if self.status['age'] >= self.burn:
            self.status['alive'] = False
        
        
        # Runs the standard life routine
        if self.status['alive']:
            
            self.age()
            
            self.randomove()
            
            self.mature()
                    
            self.gestate(world)

            self.collide()
            
        else:
            # if dead remove sprite
            self.organismlist.remove(self.sprite)

# vegetation to be worked out.
class Flora(object,):
    
    def __init__(self,kind,span,location,fruit):
        # generates a genetic marker set
        self.genes={'kind':kind,'span':span,'fruit':fruit}

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
        self.status = {'alive' : True, 'pregnant': False, 'sick': False, 'age' : 0, 'sex' : self.sex, "locx" : self.x, "locy" : self.y, "mature" : False }
        
        self.sprite = OrganismSprite(self.x,self.y,self.status)
        
        # adds organism to sprite list
        organismlist.add(self.sprite)
        
        # adds the organismlist to this object for further use
        self.organismlist = organismlist

    def update(self):
        #runs the main alive routine every cycle
        if self.state:
            pass

    def sprout(self):
        pass

    def die(self):
        pass

    def waseaten(self):   
        pass


