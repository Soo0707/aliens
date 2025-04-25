import pygame
from os import walk
from os.path import join
from player import  *
from enemy import *

class Poison(Enemy):
    def __init__(self, player, groups, collide, location, attack):
        super().__init__(player, groups, collide, location, attack)
        
        self.image = pygame.image.load(join("..", "assets", "enemy", "Poison" , "1.png")).convert_alpha() #need to change this later to fit with animations