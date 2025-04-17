import pygame
from os import walk
from os.path import join
from player import  *



class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, groups, frame, frames, location):
        super().__init__(groups)

        self.image = pygame.image.load(join("..", "assets", "enemy", "Trapper" , "1.png")).convert_alpha() #need to change this later to fit with animations
        self.rect = self.image.get_frect()

        self.speed = 150
        self.player = player
    def movement(self, dt):

        #Positions

        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos).normalize()

        #movement

        self.rect.center += self.direction * self.speed *dt

    def update(self, dt):
        self.movement(dt)
