import pygame
pygame.font.init()
from main import *
from ui import *

class ESC(UI):
    def __init__(self): #add powerup as attribute when done
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 40)
        self.left = 215
        self.top = 85
        #self.powerup = powerup
        
        #control
        self.general_options = ['option 1', 'option 2', 'option 3']
        self.general_index = {'col': 0, 'row': 0}
        self.state = 'general'