import pygame
from pytmx.util_pygame import load_pygame
from random import choice

from projectile import *
from player import *
from enemy import *
from xp import *
from allsprites import *

class game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.running = True

        # sprite groups, useful for collision detection and camera later on
        self.all_sprites = AllSprites()
        self.enemies = pygame.sprite.Group()
        self.xp = pygame.sprite.Group()
        self.collidables = pygame.sprite.Group()


        #enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_position = []

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

        for x, y, texture, in background.get_layer_by_name("Spawners").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))
            self.spawn_position.append((x * 32, y * 32))

        self.player = Player((400, 300), self.collidables, self.enemies, self.all_sprites, self.all_sprites)


    
        enemy = Enemy(
                
            player = self.player,
            enemies = self.enemies,
            health = 100,
            all_sprites = self.all_sprites,
            groups = (self.all_sprites, self.enemies),
            location = choice(self.spawn_position),
            collide = self.collidables,
            attack = 10,
            xp = self.xp
        )


    def run(self):
        while self.running:
            # quits elegantly, never use this for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(
                        player=self.player,
                        enemies=self.enemies,
                        health=100,
                        all_sprites=self.all_sprites,
                        groups=(self.all_sprites, self.enemies),
                        location=choice(self.spawn_position),
                        collide=self.collidables,
                        attack=10,
                        xp=self.xp
                    )


            self.screen.fill("black")

            dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

            self.all_sprites.update(dt)
 
            self.all_sprites.draw(self.screen, self.player.rect)

            pygame.display.flip() # updates screen


        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()
