import pygame
from pytmx.util_pygame import load_pygame
from random import choice

from projectiles import *
from player import *
from enemy import *
from xp import *
from allsprites import *

class game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.running = True

        self.powerup_list = ["greenbull", "aussie"] # all possible powerup keys here
        self.powerups = {} # key would be powerup name, value can be whatever you deem necessary to make it work, we'd add powerups to this dict using a ui
        self.powerup_timers = {} # key = powerup name, value = expiry (tick now + duration) in ticks
        
        # sprite groups, useful for collision detection and camera later on
        self.all_sprites = AllSprites(self.powerups)
        self.enemies = pygame.sprite.LayeredUpdates()
        self.xp = pygame.sprite.LayeredUpdates()
        self.collidables = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
       
        self.num_xp = 0

        self.setup()

    
    def setup(self):
        background = load_pygame(join("..", "assets", "map", "map.tmx"))


        # 32 cause tile size is 32px
        for x, y, texture in background.get_layer_by_name("Ground").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites)

        for x, y, texture in background.get_layer_by_name("Walls").tiles():
            Walls((x * 32, y * 32), texture, (self.all_sprites, self.walls))

        for x, y, texture in background.get_layer_by_name("Props").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        for x, y, texture, in background.get_layer_by_name("Spawners").tiles():
            Spawner(
                location=(x * 32, y * 32),
                texture=texture,
                groups=(self.all_sprites, self.collidables),
                player=self.player,
                all_sprites=self.all_sprites,
                enemies=self.enemies,
                walls=self.walls,
                collidables=self.collidables,
                xp=self.xp,
            )
        self.player = Player((400, 300), self.walls, self.collidables, self.enemies, self.all_sprites, self.powerups, self.all_sprites)
        
    def check_timers(self):
        now = pygame.time.get_ticks()

        for powerup in self.powerups.copy():
            if powerup in self.powerup_timers.copy():
                if self.powerup_timers[powerup] - now <= 0:
                    del self.powerups[powerup]
                    del self.powerup_timers[powerup]
                    
    def run(self):
        while self.running:
            # quits elegantly, never use this for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            for orb in self.xp:
                if self.player.rect.colliderect(orb.rect):
                    self.num_xp = self.num_xp + 1
                    print(self.num_xp)
                    orb.kill()


            self.check_timers()

            self.screen.fill("black")

            dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

            self.all_sprites.update(dt)
 
            self.all_sprites.draw(self.screen, self.player.rect)

            pygame.display.flip() # updates screen


        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()
