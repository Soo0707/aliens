import pygame
from os import walk
from os.path import join
from player import  *
from enemy import *

class Trapper(Enemy):
    def __init__(self, player, groups, collide, location, attack):
        super().__init__(player, groups, collide, location, attack)