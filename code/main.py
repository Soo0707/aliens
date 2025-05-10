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


        self.powerup_list = ["greenbull", "aussie", "milk", "drunk", "lazers", "projectiles", "blood_sacrifice", "blood_regeneration"] # all possible powerup keys here
        self.powerups = {
                "projectiles" : [1000, 100], # index: speed, cooldown
                "lazers" : [5, 1000] # index: width, cooldown
                } 
        self.powerup_timers = {} # key = powerup name, value = expiry (tick now + duration) in ticks
        
        # sprite groups, useful for collision detection and camera later on
        self.all_sprites_group = AllSprites(self.powerups)
        self.enemy_group = pygame.sprite.LayeredUpdates()
        self.xp_group = pygame.sprite.LayeredUpdates()
        self.collidable_group = pygame.sprite.LayeredUpdates()
        self.walls_group = pygame.sprite.LayeredUpdates()
        self.projectile_group = pygame.sprite.LayeredUpdates()
        self.enemy_projectile_group = pygame.sprite.LayeredUpdates()
        self.spawners_group = pygame.sprite.LayeredUpdates()

        self.player = Player((1024, 4032), self.collidable_group, self.all_sprites_group, self.powerups, self.projectile_group, self.all_sprites_group)

        self.num_xp = 0

        self.textures = {
                "bomber": [],
                "drunkard": [],
                "hooker": [],
                "poison": [],
                "trapper": [],
                "australian":[],
                "beer": [],
                "xp": []
                }
        
        self.turn = 1
        

        self.powerup_menu = Powerup_Menu(
                                         powerup_list = self.powerup_list,
                                         powerups = self.powerups
                                        )
        self.pause_menu = Pause()
        self.is_paused = False #<--- condition for pausing
        self.powerup_menu_activation = False #<--- condition for pausing
        
        self.load_map()
        self.load_textures()

    def load_map(self):
        background = load_pygame(join("..", "assets", "map", "map.tmx"))
        # 32 cause tile size is 32px
        for x, y, texture in background.get_layer_by_name("Ground").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites_group)

        for x, y, texture in background.get_layer_by_name("Walls").tiles():
            Walls((x * 32, y * 32), texture, (self.all_sprites_group, self.walls_group))

        for x, y, texture in background.get_layer_by_name("Props").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites_group, self.collidable_group))

        for x, y, texture, in background.get_layer_by_name("Spawners").tiles():
            Spawner(
                location=(x * 32, y * 32),
                texture=texture,
                groups=(self.all_sprites_group, self.collidable_group, self.spawners_group),
                player=self.player,
                powerups= self.powerups,
                enemy_projectile_group = self.enemy_projectile_group,
                all_sprites_group=self.all_sprites_group,
                xp_group=self.xp_group,
                enemy_group = self.enemy_group,
                enemy_textures = self.textures,               
            )

    def load_textures(self):
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
                    if self.is_paused:
                        self.is_paused = False
                    else:
                        self.is_paused = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.is_paused = False
            
            
            if self.is_paused:
                self.pause_menu.do_pause()  
            else:
                self.screen.fill("black")
                dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

                self.player.move_x(dt)               
                if "greenbull" not in self.powerups:
                    collision_x(self.player, self.collidable_group, False)
                collision_x(self.player, self.walls_group, False)

                self.player.move_y(dt)
                if "greenbull" not in self.powerups:
                    collision_y(self.player, self.collidable_group, False)
                collision_y(self.player, self.walls_group, False)

 #               print(self.enemy_group, self.clock.get_fps())

                self.player.update(dt)
                
                if self.turn == 1:
                    self.check_timers()
                    for orb in self.xp_group:
                        if self.player.rect.colliderect(orb.rect):
                            self.num_xp = self.num_xp + 1
                            orb.kill()
                
                    collision_projectile(self.projectile_group, self.enemy_group, self.walls_group)
                    le_attack(self.player, self.enemy_group, self.powerups, self.powerup_timers)

                    self.turn = 2
                elif self.turn == 2:
                    check_enemy_projectiles(self.player, self.powerups, self.powerup_timers, self.enemy_projectile_group, self.walls_group)

                    for enemy in self.enemy_group:
                        enemy.move_x(dt)

                    collision_x(self.enemy_group, self.collidable_group, True) 
                    collision_x(self.enemy_group, self.walls_group, True) 
                    
                    for enemy in self.enemy_group:
                        enemy.move_y(dt)

                    collision_y(self.enemy_group, self.collidable_group, True)
                    collision_y(self.enemy_group, self.walls_group, True)

                    self.turn = 3
                elif self.turn == 3:
                    if self.player.rect.x < 160 and self.player.rect.y > 3968:
                        self.running = False
                    elif self.player.rect.x > 1888 and self.player.rect.y > 3968:
                        self.player.rect.x = 400
                        self.player.rect.y = 300

                    self.spawners_group.update(dt)
                    self.enemy_group.update(dt)
                    
                    self.turn = 1


                self.projectile_group.update(dt)
                self.enemy_projectile_group.update(dt)

                self.all_sprites_group.draw(self.screen, self.player.rect)
                
                if self.powerup_menu_activation:
                    self.powerup_menu.update()  
                    self.powerup_menu.draw()                 

            pygame.display.flip() # updates screen

        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()
