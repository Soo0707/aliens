import pygame
from os.path import join

from allsprites import *
from player import  *
from xp import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, location, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(groups)
        
        all_sprites_group.change_layer(self, 1)

        self.image = pygame.image.load(join("..", "assets", "enemy", "trapper" , "1.png")).convert_alpha() #need to change this later to fit with animations

        self.rect = self.image.get_rect(center = location)
        
        self.direction = pygame.math.Vector2()
        self.location = location
        self.health = 100

        self.speed = 300 # Enemy
        self.attack = 10 #Enemy attack 
        self.attack_cooldown_primary = 5000 #attack cooldown
        self.attack_cooldown_secondary = 5000 #attack cooldown
        
        self.last_attack_primary = 0
        self.can_attack_primary = True

        self.last_attack_secondary = 0
        self.can_attack_secondary = True

        self.player = player

        self.all_sprites_group = all_sprites_group
        self.xp_group = xp_group
        
        self.xp_texture = xp_texture


    def set_direction(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos)

        if self.direction:
            self.direction = self.direction.normalize()
        
    def move_x(self, dt):
        self.rect.x += self.direction.x * self.speed * dt

    def move_y(self, dt):
        self.rect.y += self.direction.y * self.speed * dt

    def animate(self, dt):
        pass
    
    def secondary(self):
        pass

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
        self.secondary()
