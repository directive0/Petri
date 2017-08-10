import pygame
black = (0,0,0)
pygame.init()
pygame.font.init()

screenSize = (320,240)
modes = pygame.display.list_modes(16)
surface = pygame.display.set_mode(screenSize)

pygame.display.set_caption('Petri Dish Alpha 1')
petrin = pygame.image.load('petrin.png')
class OrganismSprite(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(OrganismSprite,self).__init__()
        self.size=(10,10)
        self.color=(255,255,255)
        self.image = pygame.image.load("petrin.png")
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

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
        print("made it to draw rect")
        rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, rect)

all_sprites_list = pygame.sprite.Group()
        
def subdraw(surface,pop):
    
    #all_sprites_list.clear(surface,black)
    all_sprites_list.empty() 
    surface.fill(black)
    

    
    for x in pop:

        info = x.getstatus()
        petri = OrganismSprite(info["locx"],info["locy"])
        all_sprites_list.add(petri)
        

    all_sprites_list.draw(surface)    
    pygame.display.flip()
