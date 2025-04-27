import pygame
from os.path import join

from player import Player
from xp import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, collide, location, enemies, xp, all_sprites, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(join("..", "assets", "enemy", "trapper" , "1.png")).convert_alpha() #need to change this later to fit with animations
        self.rect = self.image.get_frect(center = location)
        self.old_rect = self.rect.copy()

        self.direction = pygame.math.Vector2()
        self.location = location
        self.health = 100

        self.speed = 150 # Enemy
        self.attack = 10 #Enemy attack 
        self.attack_cooldown = 5000 #attack cooldown

        self.last_attack = 0
        self.can_attack = True

        self.player = player

        self.collidables = collide
        self.enemies = enemies
        self.all_sprites = all_sprites
        self.xp = xp

    def collision_x_nonmoving(self, target):
        for collidable in target:
            if self.rect.colliderect(collidable.rect):
                if self.direction.x > 0:  
                    self.rect.right = collidable.rect.left
                elif self.direction.x < 0:  
                    self.rect.left = collidable.rect.right

    def collision_y_nonmoving(self, target):
        for collidable in target:
            if self.rect.colliderect(collidable):
                if self.direction.y > 0:
                    self.rect.bottom = collidable.rect.top
                elif self.direction.y < 0:
                    self.rect.top = collidable.rect.bottom
    
    def collision_x_moving(self, target, iterable):
        if iterable:
            for collidable in target:
                if collidable == self:
                    continue

                if self.rect.colliderect(collidable.rect):
                    self.direction.x = 0
                    self.direction.y = 0
                    if self.old_rect.x <= collidable.old_rect.x and self.rect.x >= collidable.rect.x:
                        self.rect.right = self.old_rect.right
                    elif self.old_rect.x >= collidable.old_rect.x and self.rect.x <= collidable.rect.x:
                        self.rect.left = self.old_rect.left
        else:
            if self.rect.colliderect(target.rect):
                self.direction.x = 0
                self.direction.y = 0
                if self.old_rect.x <= target.old_rect.x and self.rect.x >= target.rect.x:
                    self.rect.right = self.old_rect.right
                elif self.old_rect.x >= target.old_rect.x and self.rect.x <= target.rect.x:
                    self.rect.left = self.old_rect.left


    def collision_y_moving(self, target, iterable):
        if iterable:
            for collidable in target:
                if collidable == self:
                    continue

                if self.rect.colliderect(collidable.rect):
                    self.direction.x = 0
                    self.direction.y = 0
                    if self.old_rect.y <= collidable.old_rect.y and self.rect.y >= collidable.rect.y:
                        self.rect.bottom = self.old_rect.bottom
                    elif self.old_rect.y >= collidable.old_rect.y and self.rect.y <= collidable.rect.y:
                        self.rect.top = self.old_rect.top

        else: 
            if self.rect.colliderect(target.rect):
                self.direction.x = 0
                self.direction.y = 0
                if self.old_rect.y <= target.old_rect.y and self.rect.y >= target.rect.y:
                    self.rect.bottom = self.old_rect.bottom
                elif self.old_rect.y >= target.old_rect.y and self.rect.y <= target.rect.y:
                    self.rect.top = self.old_rect.top


    def movement(self, dt):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos)

        if self.direction:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * self.speed * dt
        
        self.collision_x_moving(self.enemies, True)
        self.collision_x_moving(self.player, False)
        
        for group in self.collidables:
            self.collision_x_nonmoving(group)
 

        self.rect.y += self.direction.y * self.speed * dt
        
        self.collision_y_moving(self.enemies, True)
        self.collision_y_moving(self.player, False)

        for group in self.collidables:
            self.collision_y_nonmoving(group)


    def le_attack(self):

        now = pygame.time.get_ticks()

        if self.can_attack and self.rect.colliderect(self.player.rect):
            self.player.health = self.player.health - self.attack
            self.can_attack = False
            self.last_attack = now



    def update(self, dt):
        now = pygame.time.get_ticks()

        if self.health <= 0:
            Orb(self.rect.center, (self.all_sprites, self.xp))
            self.kill()

        if not self.can_attack and now - self.last_attack >= self.attack_cooldown:
            self.can_attack = True

        self.old_rect = self.rect.copy()

        self.le_attack()
        self.movement(dt)
