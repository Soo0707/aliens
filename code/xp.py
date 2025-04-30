import pygame

class Orb(pygame.sprite.Sprite):
    def __init__(self, texture, location, groups): 
       super().__init__(groups)
       self.image = texture
       self.rect = self.image.get_frect(center = location)



    
