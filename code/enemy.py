import pygame
from os.path import join

from allsprites import *
from player import  *
from xp import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, location, xp, all_sprites, textures, xp_texture, groups):
        super().__init__(groups)
        
        all_sprites.change_layer(self, 1)

        self.textures = textures
        self.image = pygame.image.load(join("..", "assets", "enemy", "trapper" , "1.png")).convert_alpha() #need to change this later to fit with animations

        self.rect = self.image.get_frect(center = location)
        
        self.direction = pygame.math.Vector2()
        self.location = location
        self.health = 100

        self.speed = 150 # Enemy
        self.attack = 10 #Enemy attack 
        self.attack_cooldown = 5000 #attack cooldown
        
        self.last_attack = 0
        self.can_attack = True

        self.player = player

        self.all_sprites = all_sprites
        self.xp = xp
        
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

    def le_attack(self):
        now = pygame.time.get_ticks()

        if self.can_attack and self.rect.colliderect(self.player.rect):
            self.player.health = self.player.health - self.attack
            self.can_attack = False
            self.last_attack = now

    def update(self, dt):
        now = pygame.time.get_ticks()
        
        if self.health <= 0:
            Orb(self.xp_texture, self.rect.center, (self.all_sprites, self.xp))
            self.kill()

        if not self.can_attack and now - self.last_attack >= self.attack_cooldown:
            self.can_attack = True

        self.le_attack()
        self.set_direction()
