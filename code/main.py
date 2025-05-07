import pygame
from pytmx.util_pygame import load_pygame

from projectiles import *
from player import *
from xp import *
from allsprites import *
from collisions import *
from powerup_menu import *
from pause import *

from os.path import join
from os import listdir

class game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True

        self.powerup_list = ["greenbull", "aussie", "milk", "drunk", "lazer_width", "blood_sacrifice", "blood_regeneration"] # all possible powerup keys here
        self.powerups = {
                "lazer_width" : 5,
                "greenbull": 0,
                } # key = powerup name, value = any stuff you need to make it work
        self.powerup_timers = {} # key = powerup name, value = expiry (tick now + duration) in ticks
        
        # sprite groups, useful for collision detection and camera later on
        self.all_sprites = AllSprites(self.powerups)
        self.enemies = pygame.sprite.LayeredUpdates()
        self.xp = pygame.sprite.LayeredUpdates()
        self.collidables = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.projectiles = pygame.sprite.LayeredUpdates()
        
        self.num_xp = 0

        self.textures = {
                "bomber": [],
                "drunkard": [],
                "hooker": [],
                "poison": [],
                "trapper": [],
                "xp": []
                }
        
        self.turn = 1
        
        self.powerup_menu = Powerup_Menu(powerup_list = self.powerup_list,
                                         powerups = self.powerups
                                         )
        self.pause = Pause()
        self.is_paused = False #<--- condition for pausing
        self.powerup_menu_activation = True #<--- condition for pausing

        self.setup()

    
    def setup(self):
        background = load_pygame(join("..", "assets", "map", "map.tmx"))

        self.player = Player((400, 300), self.collidables, self.all_sprites, self.powerups, self.projectiles, self.all_sprites)

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
                xp=self.xp,
                enemies = self.enemies,
                enemy_textures = self.textures,
                powerups= self.powerups
            )
        
        for key in self.textures:
            for item in sorted(listdir(join("..", "assets", "enemy", key))):
                self.textures[key].append(pygame.image.load(join("..", "assets", "enemy", key, item)).convert_alpha())
           


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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_paused = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.is_paused = False

            
            if self.is_paused:
                self.pause.do_pause()            
                
            else:
                self.check_timers
                self.screen.fill("black")                    
            

                dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics
            
                self.player.move_x(dt)
            
                if "greenbull" not in self.powerups:
                    collision_x(self.player, self.collidables, False)
                collision_x(self.player, self.walls, False)

                self.player.move_y(dt)
                if "greenbull" not in self.powerups:
                    collision_y(self.player, self.collidables, False)
                collision_y(self.player, self.walls, False)

                if self.turn == 1:               
                    for orb in self.xp:
                        if self.player.rect.colliderect(orb.rect):
                            self.num_xp = self.num_xp + 1
                            orb.kill()
            
                    collision_projectile(self.projectiles, self.enemies, (self.collidables, self.walls))
                    self.turn = 2
                elif self.turn == 2:
                    for enemy in self.enemies:
                        enemy.move_x(dt)

                    collision_x(self.enemies, self.collidables, True) 
                    collision_x(self.enemies, self.walls, True) 
                
                    for enemy in self.enemies:
                        enemy.move_y(dt)

                    collision_y(self.enemies, self.collidables, True)
                    collision_y(self.enemies, self.walls, True)
                    self.turn = 1

                self.all_sprites.update(dt)


                self.all_sprites.draw(self.screen, self.player.rect)
                
                if self.powerup_menu_activation:
                    self.powerup_menu.update()  
                    self.powerup_menu.draw() 
                    
            pygame.display.flip() # updates screen


        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()
