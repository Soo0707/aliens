import pygame
from player import  *
from enemy import *
from projectiles import Beer

class Drunkard(Enemy):
    def __init__(self, player, state, location, powerups, textures, beer_textures, enemy_projectile_group, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups)
        
        self.speed = 600
        self.images = textures
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = location)
        
        self.beer_textures = beer_textures
        self.image_index = 0
        
        self.enemy_projectile_group = enemy_projectile_group

    def animate(self, dt):
        if self.direction:
            self.image_index += 10 * dt
            self.image = self.images[int(self.image_index) % len(self.images)]
        else:
            self.image_index = 0
            self.image = self.images[0] # the 0th image is always the idle frame
    
    def secondary(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        self_pos = pygame.math.Vector2(self.rect.center)

        direction = (player_pos - self_pos)

        if direction:
            direction = direction.normalize()

        if self.can_attack_secondary:
            Beer(self.beer_textures, self.state, self.rect.center, direction, (self.enemy_projectile_group, self.all_sprites_group))
            self.last_attack_secondary = pygame.time.get_ticks()
            self.can_attack_secondary = False

        
