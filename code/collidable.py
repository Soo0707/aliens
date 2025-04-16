import pygame
from os.path import join

class Collidable(pygame.sprite.Sprite):
    def __init__(self, location, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(join("..", "assets", "collidable.png")).convert_alpha()
        self.rect = self.image.get_frect(center = location)

