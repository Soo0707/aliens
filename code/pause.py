import pygame

class Pause:
    def __init__(self): #add powerup as attribute when done
        pygame.font.init()
        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font(None, 40)
        self.left = 640
        self.top = 310
        
        self.bg = pygame.Surface((1280,720))
        self.bg.set_alpha(128)
        
        left_rect = pygame.FRect((self.left - 25), self.top, 35, 100)
        pygame.draw.rect(self.bg, 'light gray', left_rect, 0, 4)
        pygame.draw.rect(self.bg, 'gray', left_rect, 4, 4)
        
        right_rect = pygame.FRect((self.left + 25), self.top, 35, 100)
        pygame.draw.rect(self.bg, 'light gray', right_rect, 0, 4)
        pygame.draw.rect(self.bg, 'gray', right_rect, 4, 4)
        
        pause_text_surf = self.font.render('PAUSE', True, 'light gray')
        pause_text_rect = pause_text_surf.get_frect(center = (640 + 20, 360 + 70))
        self.bg.blit(pause_text_surf, pause_text_rect)
    
    def do_pause(self):
        self.display_surface.blit(self.bg)

