from main import *

class UI:
    def __init__(self): #add powerup as attribute when done
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = 1280 / 2 
        self.top = 720 /2
        #self.powerup = powerup
        
    def general(self):
        print('general')
    
    def draw(self):
        self.general()