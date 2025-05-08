import pygame
from player import  *
from enemy import *
from projectiles import Beer

class Drunkard(Enemy):
    def __init__(self, player, location, textures, beer_textures, enemy_projectile_group, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, textures, location, xp_texture, xp_group, all_sprites_group, groups)

        self.images = textures
        self.image = self.images[0]
        self.beer_textures = beer_textures
        self.image_index = 0

        self.enemy_projectile_group = enemy_projectile_group

    def secondary(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        self_pos = pygame.math.Vector2(self.rect.center)

        direction = (player_pos - self_pos)

        if direction:
            direction = direction.normalize()

        if self.can_attack_secondary:
            Beer(self.beer_textures, self.rect.center, direction, (self.enemy_projectile_group, self.all_sprites_group))
            self.last_attack_secondary = pygame.time.get_ticks()
            self.can_attack_secondary = False

        
