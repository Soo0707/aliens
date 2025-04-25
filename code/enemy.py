import pygame
from os import walk
from os.path import join
from player import  *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, frames, player, groups, collide, location, attack):
        super().__init__(groups)

        self.image = pygame.image.load(join("..", "assets", "enemy", "Trapper" , "1.png")).convert_alpha() #need to change this later to fit with animations
        self.rect = self.image.get_frect(center = location)
        
        #image
        self.frame, self.frame_index = frames, 0
        self.images = self.frames[self.frame_index]
        self.animation_speed = 6
        folders = list(walk(join('images', 'enemies')))[0]
        print(folders)

        self.speed = 150 
        self.attack = 10 #Enemy attack 
        self.attack_cooldown = 5000

        self.last_attack = 0
        self.can_attack = True

        self.player = player
        self.collidables = collide
        

    def movement(self, dt):
        #Positions
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos).normalize()

        #movement
        #Move on X axis
        self.rect.x += self.direction.x * self.speed * dt
        for collidable in self.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.direction.x > 0:  
                    self.rect.right = collidable.rect.left
                elif self.direction.x < 0:  
                    self.rect.left = collidable.rect.right

        # Move on Y axis
        self.rect.y += self.direction.y * self.speed * dt
        for collidable in self.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.direction.y > 0: 
                    self.rect.bottom = collidable.rect.top
                elif self.direction.y < 0:  
                    self.rect.top = collidable.rect.bottom

        #Player Collisions
        #X-Axis
        if self.rect.colliderect(self.player.rect):
            #self.player.health = self.player.health - self.attack
            if self.direction.x > 0:  
                self.rect.right = self.player.rect.left
            elif self.direction.x < 0:  
                self.rect.left = self.player.rect.right

        #Y-Axis
        if self.rect.colliderect(self.player.rect):
            if self.direction.y > 0:  
                self.rect.bottom = self.player.rect.top
            elif self.direction.y < 0:  
                self.rect.top = self.player.rect.bottom
    

        
    def le_attack(self):

        now = pygame.time.get_ticks()

        if self.can_attack and self.rect.colliderect(self.player.rect):
            self.player.health = self.player.health - self.attack
            self.can_attack = False
            self.last_attack = now



    def update(self, dt):

        now = pygame.time.get_ticks()
        
        if not self.can_attack and now - self.last_attack >= self.attack_cooldown:
            self.can_attack = True


        self.le_attack()
        self.movement(dt)
        print(self.player.health)

