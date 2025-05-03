import pygame
pygame.font.init()
from main import *

class Powerup_Menu:
    def __init__(self): #add powerup as attribute when done
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 40)
        self.left = 215
        self.top = 85
        #self.powerup = powerup
        
        #control
        self.general_options = ['powerup 1', 'powerup 2', 'powerup 3']
        self.general_index = {'col': 0, 'row': 0}
        self.state = 'general'
        
    def input(self):
        #The codes below are for knowing which "button" we are on
        keys = pygame.key.get_just_pressed()
        self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % 3
        self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % 1
        if keys[pygame.K_SPACE]:
            self.state = self.general_options[self.general_index['row']] # this equation will change depending on the equation for index
            
        
    def general(self):
        #background
        bg = pygame.Surface((1280,720))
        bg.set_alpha(128)
        bg.fill((0, 0, 0))
        self.display_surface.blit(bg, (0,0))
        rect = pygame.FRect(self.left, self.top, 850, 550)
        pygame.draw.rect(self.display_surface, 'light gray', rect, 0, 4)
        pygame.draw.rect(self.display_surface, 'gray', rect, 4, 4)
        
        #menu
        cols, rows = 1, 3
        for col in range(cols):
            for row in range(rows):
                x = rect.left + rect.width / 5
                y = rect.top + (rect.height / 4) + (rect.height / 4) * row
                i = row     #the equation for i/index will change depending on the amount of rows and columns
                if col == self.general_index['col'] and row == self.general_index['row']: 
                    color = pygame.Color(190, 190, 190, 255)
                else: 
                    color = pygame.Color(0, 0, 0, 255),
                
                text_surf = self.font.render(self.general_options[i], True, color)
                text_rect = text_surf.get_frect(center = (x,y))
                self.display_surface.blit(text_surf, text_rect)
                
    def update(self):
        self.input()            
                
        
    def draw(self):
        match self.state:
            case 'general': self.general()