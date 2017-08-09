import random
import time
from world import *

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
        self.status = {'alive' : True, 'pregnant': False, 'sick': False, 'age' : 0, 'sex' : self.sex, }
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
        return self.status
        
    def getlocation(self):
        return self.location
        
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

