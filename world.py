import biomass
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
            
    def birth(self,locx,locy):
        print("birthing a new organism at " + str(locx) + " and " + str(locy))
        self.population.append(organism("meat",10,10,locx,locy,10,10,10))
        
    def starter(self):
        for i in range(2):
            self.newlocx = random.randint(0,self.stagex)
            self.newlocy = random.randint(0,self.stagey)
            self.birth(self.newlocx,self.newlocy)
            
    def update(self): 
        if self.started == 1:
            print("initial birth begun")
            self.starter()
            self.started = 0
        
        for x in self.population:
            x.update()
            self.info = x.getstatus()
            print(self.info)
            
class organism(object):

    def __init__(self,type,span,food,locationx,locationy,burn,attack,defend):
        self.genes={'type':type, 'span':span,'food':food,'burn':burn,'attack':attack,'defend':defend}
        self.genes['state']= 'defined'
        self.x = locationx
        self.y = locationy
        self.direction = 0
        self.haschosen = False
        self.distance = 0
        self.sex = random.randint(0,1)
        self.status = {'alive' : True, 'pregnant': False, 'sick': False, 'age' : 0, 'sex' : self.sex, "locx" : self.x, "locy" : self.y }
        #organism chooses a direction and a distance, moves in that direction for a distance and then stops and redos.
    def randomove(self):
        if self.haschosen:
            if self.distance >= 0:
                self.location += self.rate
        else:
            self.direction = random.randint(0, 360)
            self.distance = random.randint(0,10)
            
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
            if not self.pregnant:
                self.pregnant=random.randint(0,1)
            else:
                self.gestation = 20
                self.status = {pregnant : True}

    def update(self):
        print("updating organism" + str(self))
        
        if self.status['alive']:
            
            print("made it to update")
            randomx = random.randint(0,1)
            randomy = random.randint(0,1)
            
            print(randomx)
            
            if randomx == 0:
                self.x += 1
            else:
                self.x -= 1
                
            if randomy == 0:
                self.y += 1
            else:
                self.y -= 1
            
            if self.x >= 310:
                self.x = 310
            
            if self.x <= 0:
                self.x =0
            
            if self.y >= 230:
                self.y = 230
            
            if self.y <= 0:
                self.y = 0
                
            self.status["age"] += .1
                
            
            if self.status["pregnant"]:
                self.gestation -= 1
                
                if self.gestation == 0:
                    World.birth() 
        else:
            pass
            
class vegetation(object,):
    
    def __init__(self,type,span,location,burn,attack,defend):
        pass
    
    def grow(self):
        pass
        
    def die(self):
        pass
    
    def waseaten(self):   
        pass

