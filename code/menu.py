import pygame
pygame.font.init()
from main import *

class MENU:
    def __init__(self): #add powerup as attribute when done
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 40)
        self.left = 640
        self.top = 310
        #self.powerup = powerup
        
        #control
        self.state = 'resume'
        
    def input(self):
        #The codes below are for knowing which "button" we are on
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = 'pause'
        elif keys[pygame.K_SPACE]:
            self.state = 'resume'
        
    def general(self):
        bg = pygame.Surface((1280,720))
        bg.set_alpha(128)
        bg.fill((0, 0, 0))
        self.display_surface.blit(bg, (0,0))
        
        
        left_rect = pygame.FRect((self.left - 25), self.top, 35, 100)
        pygame.draw.rect(self.display_surface, 'light gray', left_rect, 0, 4)
        pygame.draw.rect(self.display_surface, 'gray', left_rect, 4, 4)
        
        right_rect = pygame.FRect((self.left + 25), self.top, 35, 100)
        pygame.draw.rect(self.display_surface, 'light gray', right_rect, 0, 4)
        pygame.draw.rect(self.display_surface, 'gray', right_rect, 4, 4)
        
        pause_text_surf = self.font.render('PAUSE', True, 'light gray')
        pause_text_rect = pause_text_surf.get_frect(center = (640 + 20, 360 + 70))
        self.display_surface.blit(pause_text_surf, pause_text_rect)
        

                
    def update(self):
        self.input()            
                
        
    def draw(self):
        match self.state:
            case 'pause': self.general()