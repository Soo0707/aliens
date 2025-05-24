import pygame
from player import  *
from enemy import *

class Trapper(Enemy):
    def __init__(self, player, state, location, powerups, textures, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups)
        self.speed = 600
        self.images = textures
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = location)
        self.image_index = 0

        self.attack = 10

    def animate(self, dt):
        if self.direction:
            self.image_index += 50 * dt
            self.image = self.images[int(self.image_index) % len(self.images)]
        else:
            self.image_index = 0
            self.image = self.images[0]

    def update(self, dt):
        now = pygame.time.get_ticks()
        
        if self.health <= 0:
            Orb(self.xp_texture, self.rect.center, (self.all_sprites_group, self.xp_group))
            self.kill()

        if not self.can_attack_primary and now - self.last_attack_primary >= self.attack_cooldown_primary:
            self.can_attack_primary = True

        if not self.can_attack_secondary and now - self.last_attack_secondary >= self.attack_cooldown_secondary:
            self.can_attack_secondary = True
        
        self.set_direction()
        self.animate(dt)
    
