import pygame
from player import  *
from enemy import *

class Hooker(Enemy):
    def __init__(self, player, location, textures, xp_textures, xp_group, all_sprites_group, groups):
        super().__init__(player, location, xp_texture, xp_group, all_sprites_group, groups)

        self.images = textures
        self.image = self.images[0]
        self.image_index = 0
