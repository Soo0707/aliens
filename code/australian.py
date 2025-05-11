import pygame
from player import  *
from enemy import *

class Australian(Enemy):
    def __init__(self, player, state, location, powerups, textures, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups)
        self.speed = 500
        self.images = textures
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = location)
        self.image_index = 0
    
    def animate(self, dt):
        if self.direction:
            self.image_index += 10 * dt
            self.image = self.images[int(self.image_index) % len(self.images)]
        else:
            self.image_index = 0
            self.image = self.images[0] # the 0th image is always the idle frame
