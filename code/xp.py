import pygame
from os import walk
from os.path import *
from enemy import *


class Orb(pygame.sprite.Sprite):
    def __init__(self, location, groups, xp):
       super().__init__(groups)
       self.image = pygame.image.load(join("..", "assets", "enemy", "xp.png")).convert_alpha() 
       self.rect = self.image.get_frect(center = location)


    
