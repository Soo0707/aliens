import pygame
from player import  *
from enemy import *

class Australian(Enemy):
    def __init__(self, player, location, textures, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, location, xp_texture, xp_group, all_sprites_group, groups)

        self.images = textures
        self.image = self.images[0]
        self.image_index = 0
    
    def animate(self, dt):
        if self.direction:
            self.image_index += 10 * dt
            self.image = self.images[int(self.image_index) % len(self.images)]
        else:
            self.image_index = 0
            self.image = self.images[0] # the 0th image is always the idle frame
