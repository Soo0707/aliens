import pygame
from os import walk
from os.path import join
from player import  *
from xp import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, groups, collide, location, enemies, attack, xp, health, all_sprites):
        super().__init__(groups)
        
        self.image = pygame.image.load(join("..", "assets", "enemy", "Trapper" , "1.png")).convert_alpha() #need to change this later to fit with animations
        self.rect = self.image.get_frect(center = location)


        self.location = (500,500)
        self.health = health

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


    def movement(self, dt):
        #Positions

        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos).normalize()

        #movement

        collision_list = [collidable.rect for collidable in self.collidables] + [self.player.rect]

        #X-AXIS
        self.rect.x += self.direction.x * self.speed * dt

        #Map Collision
        for collidable in self.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.direction.x > 0:  
                    self.rect.right = collidable.rect.left
                elif self.direction.x < 0:  
                    self.rect.left = collidable.rect.right

        #Player Collisions
        if self.rect.colliderect(self.player.rect):
            if self.direction.x > 0:  
                self.rect.right = self.player.rect.left
            elif self.direction.x < 0:  
                self.rect.left = self.player.rect.right



        #Enemy Collision
        for nemesis in self.enemies:
            if nemesis == self:
                continue  # Skip self

            if self.rect.colliderect(nemesis.rect):
                if self.direction.x > 0:  
                    self.rect.right = nemesis.rect.left
                elif self.direction.x < 0:  
                    self.rect.left = nemesis.rect.right


        #Y - AXIS


        # Move on Y axis
        self.rect.y += self.direction.y * self.speed * dt
        for collidable in self.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.direction.y > 0: 
                    self.rect.bottom = collidable.rect.top
                elif self.direction.y < 0:  
                    self.rect.top = collidable.rect.bottom

        if self.rect.colliderect(self.player.rect):
            if self.direction.y > 0:  
                self.rect.bottom = self.player.rect.top
            elif self.direction.y < 0:  
                self.rect.top = self.player.rect.bottom

        #Enemy Collisions
        for nemesis in self.enemies:
            if nemesis == self:
                continue  # Skip self

            # Y-Axis collision
            if self.rect.colliderect(nemesis.rect):
                if self.direction.y > 0:  
                    self.rect.bottom = nemesis.rect.top
                elif self.direction.y < 0:  
                    self.rect.top = nemesis.rect.bottom


        

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

        now = pygame.time.get_ticks()
        
        if not self.can_attack and now - self.last_attack >= self.attack_cooldown:
            self.can_attack = True

        self.le_attack()
        self.movement(dt)
        print(self.health)
