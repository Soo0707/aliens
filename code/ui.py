import pygame
pygame.font.init()
from main import *

class UI:
    def __init__(self): #add powerup as attribute when done
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 40)
        self.left = 215
        self.top = 85
        #self.powerup = powerup
        
    def general(self):
        #background
        rect = pygame.FRect(self.left, self.top, 850, 550)
        pygame.draw.rect(self.display_surface, 'white', rect, 0, 4)
        pygame.draw.rect(self.display_surface, 'gray', rect, 4, 4)
        
        #menu
        cols, rows = 1, 2
        for col in range(cols):
            for row in range(rows):
                x = rect.left + rect.width / 4 
                y = rect.top + (rect.height / 4) + (rect.height / 2) * row
                text_surf = self.font.render('option', True, 'black')
                text_rect = text_surf.get_frect(center = (x,y))
                self.display_surface.blit(text_surf, text_rect)
                
                
        
    def draw(self):
        self.general()