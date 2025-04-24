import pygame
from os.path import join

class Spawner(pygame.sprite.Sprite):
    def __init__(self, location, texture, groups):
        super().__init__(groups)
        
        self.image = texture
        self.rect = self.image.get_rect(center = location)

    def update(self):
        pass
