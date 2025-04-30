import pygame
from pytmx.util_pygame import load_pygame

from player import *
from enemy import *
from allsprites import *
#from spawner import *
from bomber import *
from drunkard import *
from hooker import *
from poison import *
from trapper import *

from ui import *
from pause import *

import time
import os

class game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.running = True

        # sprite groups, useful for collision detection and camera later on
        self.all_sprites = AllSprites()
        self.collidables = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        #ui 
        self.ui = UI()
        
        #pause
        self.pause = Pause()
       

        self.setup()
    
    def setup(self):
        background = load_pygame(join("..", "assets", "map", "map.tmx"))

        # 32 cause tile size is 32px
        for x, y, texture in background.get_layer_by_name("Ground").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites)

        for x, y, texture in background.get_layer_by_name("Walls").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        for x, y, texture in background.get_layer_by_name("Props").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        #for x, y, texture, in background.get_layer_by_name("Spawners").tiles():
            #Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        self.player = Player((400, 300), self.collidables, self.enemies, self.all_sprites, self.all_sprites)


        hooker = Hooker(
            player = self.player,
            groups = self.all_sprites,
            location = (400, 150),
            collide = self.collidables,
            attack = 10    
        )
        
        trapper = Trapper(
            player = self.player,
            groups = self.all_sprites,
            location = (500, 200),
            collide = self.collidables,
            attack = 10 
        )
        
        bomber = Bomber(
            player = self.player,
            groups = self.all_sprites,
            location = (600, 250),
            collide = self.collidables,
            attack = 10 
        )
        
        drunkard = Drunkard(
            player = self.player,
            groups = self.all_sprites,
            location = (550, 400),
            collide = self.collidables,
            attack = 10 
        )
        
        poison = Poison(
            player = self.player,
            groups = self.all_sprites,
            location = (450, 500),
            collide = self.collidables,
            attack = 10 
        )
        
    '''def pause_menu(self):
        self.pause.draw()
        is_paused = True

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_paused = False
                        
                if event.type == pygame.QUIT:
                    is_paused = False
                    self.running = False'''

    
    def run(self):
        while self.running:
            # quits elegantly, never use this for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            

            self.screen.fill("black")

            dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

            #update
            self.state = 'resume'
            self.all_sprites.update(dt)
            self.ui.update()
            self.pause.update()

            self.all_sprites.draw(self.screen, self.player.rect)
            
            self.ui.draw()
            self.pause.draw()
            
            '''keys = pygame.key.get_just_pressed()
            if keys[pygame.K_ESCAPE]:
                self.pause_menu()'''
                    
                
            pygame.display.flip() # updates screen


        pygame.quit()
        
            
        
    

if __name__ == "__main__":
    gaem = game()
    gaem.run()
