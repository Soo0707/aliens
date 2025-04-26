import pygame
from os import walk
from os.path import join

from allsprites import Collidable
from player import  *
from xp import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, groups, collidables, location, enemies, attack, xp, health, walls,all_sprites):
        super().__init__(groups)
        
        self.image = pygame.image.load(join("..", "assets", "enemy", "Trapper" , "swish_elder_horror 1.png")).convert_alpha() #need to change this later to fit with animations
        self.rect = self.image.get_frect(center = location)


        self.health = health
        self.location = location
        self.speed = 150 # Enemy
        self.attack = 10 #Enemy attack 
        self.attack_cooldown = 5000 #attack cooldown

        self.last_attack = 0
        self.can_attack = True

        self.player = player

        self.old_rect = self.rect.copy()
        
        self.walls = walls
        self.collidables = collidables
        self.enemies = enemies
        self.all_sprites = all_sprites
        self.xp = xp


    def movement(self, dt):
        #Positions

        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos).normalize()

    
    def  Player_Collision(self,dt):

        self.rect.x += self.direction.x * self.speed * dt
        #X-AXIS

        if self.rect.colliderect(self.player.rect):
            if self.rect.right >= self.player.rect.left and self.old_rect.right <= self.player.old_rect.left:
                self.rect.right = self.player.rect.left
            elif self.rect.left <= self.player.rect.right and self.old_rect.left >= self.player.old_rect.right:
                self.rect.left = self.player.rect.right
        
        #Y - AXIS
        self.rect.y += self.direction.y * self.speed * dt
        if self.rect.colliderect(self.player.rect):
            if self.rect.bottom >= self.player.rect.top and self.old_rect.bottom <= self.player.old_rect.top:
                self.rect.bottom = self.player.rect.top
            elif self.rect.top <= self.player.rect.bottom and self.old_rect.top >= self.player.old_rect.bottom:
                self.rect.top = self.player.rect.bottom

         
    def Wall_Collision(self,dt):

        #X-AXIS

        #Wall Collision
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:  
                    self.rect.right = wall.rect.left
                elif self.direction.x < 0:  
                    self.rect.left = wall.rect.right

        
        #Y - AXIS

        # Move on Y axis
        

        # Wall Collision
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.y > 0:  
                    self.rect.bottom = wall.rect.top
                elif self.direction.y < 0:  
                    self.rect.top = wall.rect.bottom


    def Prop_Collision(self,dt):

        #Prop Collision
        for collidable in self.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.direction.x > 0:  
                    self.rect.right = collidable.rect.left
                elif self.direction.x < 0:  
                    self.rect.left = collidable.rect.right

        #Prop Collision
        for collidable in self.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.direction.y > 0: 
                    self.rect.bottom = collidable.rect.top
                elif self.direction.y < 0:  
                    self.rect.top = collidable.rect.bottom

            

        

    def le_attack(self):

        now = pygame.time.get_ticks()

        if self.can_attack and self.rect.colliderect(self.player.rect):
            self.player.health = self.player.health - self.attack
            self.can_attack = False
            self.last_attack = now

        if self.health <= 0:
            Orb(self.rect.center, (self.all_sprites, self.xp))
            self.kill()
        


    def update(self, dt):

        self.old_rect = self.rect.copy()


        now = pygame.time.get_ticks()
        
        if not self.can_attack and now - self.last_attack >= self.attack_cooldown:
            self.can_attack = True

        self.le_attack()
        self.movement(dt)
        self.Player_Collision(dt)
        self.Prop_Collision(dt)
        self.Wall_Collision(dt)
