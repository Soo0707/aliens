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
        self.state = 0
        self.tick_offsets = [0 for i in range(10)]

        self.powerup_list = ["greenbull", "aussie", "milk", "drunk", "lazers", "projectiles", "blood_sacrifice", "blood_regeneration", "Shield", "poison", "buckshot"] # all possible powerup keys here
        self.powerups = {
                "projectiles" : [1000, 100], # index: speed, cooldown
                "lazers" : [5, 1000], # index: width, cooldown
                "buckshot": 1,
                }
        self.powerup_timers = {} # key = powerup name, value = exp_groupiry (tick now + duration) in ticks
        
        # sprite groups, useful for collision detection and camera later on
        self.all_sprites_group = AllSprites(self.powerups)
        
        self.enemy_group = StatedGroup()
        self.projectile_group = StatedGroup()
        self.enemy_projectile_group = StatedGroup()

        self.xp_group = pygame.sprite.LayeredUpdates()
        self.collidable_group = pygame.sprite.LayeredUpdates()
        self.walls_group = pygame.sprite.LayeredUpdates()
        self.spawners_group = pygame.sprite.LayeredUpdates()

        self.num_xp = 0
        self.level = 0
        self.level_up = 10
        

        self.textures = {
                "bomber": [],
                "bomber_explosion" : [],
                "drunkard": [],
                "hooker": [],
                "poison": [],
                "trapper": [],
                "australian":[],
                "beer": [],
                "xp": [],
                "player" : {
                    "N": [],
                    "S": [],
                    "E": [],
                    "W": [],
                    "lazer": [],
                    "projectile": [],
                    "circle": []
                    }
                }
        
        self.load_textures()
        
        self.player = Player((1024, 4032), self.textures["player"], self.collidable_group, self.all_sprites_group, self.powerups, self.projectile_group, self.all_sprites_group)
        self.turn = 1

        self.powerup_menu = Powerup_Menu(
                                         powerup_list = self.powerup_list,
                                         powerups = self.powerups,
                                         powerup_timers = self.powerup_timers
                                        )
        self.pause_menu = Pause()
        self.is_paused = False #<--- condition for pausing
        self.powerup_menu_activation = True

        self.map_loopover_x = 0
        self.map_loopover_y = 0
        self.load_map()

    def load_map(self):
        background = load_pygame(join("..", "assets", "map", "map.tmx"))

        # 32 cause tile size is 32px
        for x, y, texture in background.get_layer_by_name("Ground").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites_group)
            self.map_loopover_x = x
            self.map_loopover_y = y

        self.map_loopover_x *= 32
        self.map_loopover_y *= 32
        
        for x, y, texture in background.get_layer_by_name("Walls").tiles():
            Walls((x * 32, y * 32), texture, (self.all_sprites_group, self.walls_group))

        for x, y, texture in background.get_layer_by_name("Props").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites_group, self.collidable_group))

        for x, y, texture in background.get_layer_by_name("Decorations").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites_group)

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
            if key == "player":
                continue

            for item in sorted(listdir(join("..", "assets", "enemy", key))):
                self.textures[key].append(pygame.image.load(join("..", "assets", "enemy", key, item)).convert_alpha())
           
        for key in self.textures["player"]:
            for item in sorted(listdir(join("..", "assets", "player", key))):
                self.textures["player"][key].append(pygame.image.load(join("..", "assets", "player", key, item)).convert_alpha())

    def check_timers(self):
        now = pygame.time.get_ticks()

        for powerup in self.powerups.copy():
            if powerup in self.powerup_timers.copy():
                if self.powerup_timers[powerup] - now <= 0:
                    del self.powerups[powerup]
                    del self.powerup_timers[powerup]
                    

    def xp_bar(self):
        self.width = 200 - (self.num_xp / self.level_up) * 200

        self.bg_rect = (1000 , 10 , 250 , 30)
        pygame.draw.rect(self.screen , (128,128,128), self.bg_rect)
        
        self.progress_rect = (1005 , 15 , 200 , 20)
        pygame.draw.rect(self.screen , (0,0,255), self.progress_rect )

        self.empty_rect = (1005 , 15 , self.width , 20)
        pygame.draw.rect(self.screen , (0,0,0), self.empty_rect )

    def heatlh_bar(self):
        self.width = 200  - (self.player.health / self.player.health_permanent) * 200

        self.bg_rect = (1000 , 45 , 250 , 30)
        pygame.draw.rect(self.screen , (128,128,128), self.bg_rect)

        self.progress_rect = (1005 , 50 , 200 , 20)
        pygame.draw.rect(self.screen , (0,255,0), self.progress_rect )

        self.empty_rect = (1005 , 50 , self.width , 20)
        pygame.draw.rect(self.screen , (0,0,0), self.empty_rect )

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            
            self.screen.fill("#18215d00")
            dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

            self.player.move_x(dt)               
            collision_x(self.player, self.collidable_group, False, self.state)
            collision_x(self.player, self.walls_group, False, self.state)

            self.player.move_y(dt)
            collision_y(self.player, self.collidable_group, False, self.state)
            collision_y(self.player, self.walls_group, False, self.state)

            self.player.update(dt, self.state)
            
            if self.player.rect.x < 160 and self.player.rect.y > 3968:
                self.running = False
            elif self.player.rect.x > 1888 and self.player.rect.y > 3968:
                self.player.rect.x = 400
                self.player.rect.y = 300
                self.player.update_distance.x = 400
                self.player.update_distance.y = 300
                return

            self.projectile_group.update(dt, self.state)
            self.enemy_projectile_group.update(dt, self.state)

            self.all_sprites_group.draw(self.screen, self.player.rect, self.state)

            pygame.display.flip()

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

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q and self.state > 0:
                    self.tick_offsets[self.state] = pygame.time.get_ticks()
                    self.state -= 1
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.state + 1 < len(self.tick_offsets):
                    self.tick_offsets[self.state] = pygame.time.get_ticks()
                    self.state += 1
                
            print(self.map_loopover_x, self.map_loopover_y)
            if self.player.health <= 0:
                self.player.health = 100
            
            if self.is_paused:
                self.pause_menu.do_pause()  
            else:
                self.screen.fill("#18215d00")
                dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

                self.player.move_x(dt)               
                if "greenbull" not in self.powerups:
                    collision_x(self.player, self.collidable_group, False, self.state)
                collision_x(self.player, self.walls_group, False, self.state)

                self.player.move_y(dt)
                if "greenbull" not in self.powerups:
                    collision_y(self.player, self.collidable_group, False, self.state)
                collision_y(self.player, self.walls_group, False, self.state)

                self.player.update(dt, self.state)
                
                now = pygame.time.get_ticks()
                if self.turn == 1:
                    for xp in self.xp_group:
                        if now - xp.birth >= 10000:
                            xp.kill()

                    collect_xp(self)

                    for projectile in self.projectile_group:
                        if type(projectile) == Circle:
                            continue

                        if now - projectile.birth - self.tick_offsets[self.state] >= 1000:
                            projectile.kill()

                    collision_projectile(self.projectile_group, self.enemy_group, self.walls_group, self.state)
                    le_attack(self.player, self.enemy_group, self.powerups, self.powerup_timers, self.state, dt)
                    AOE_collision(self.player, self.enemy_group, self.powerups, self.powerup_timers, self.state)
                    self.check_timers()

                    self.turn = 2
                elif self.turn == 2:
                    for enemy in self.enemy_group:            
                        if now - enemy.birth - self.tick_offsets[self.state] >= 10000 or not enemy.rect.colliderect(self.player.update_distance):
                            enemy.kill()

                    for enemy in self.enemy_group:
                        enemy.move_x(dt, self.state)

                    collision_x(self.enemy_group, self.collidable_group, True, self.state) 
                    collision_x(self.enemy_group, self.walls_group, True, self.state) 
                    
                    for enemy in self.enemy_group:
                        enemy.move_y(dt, self.state)

                    collision_y(self.enemy_group, self.collidable_group, True, self.state)
                    collision_y(self.enemy_group, self.walls_group, True, self.state)

                    self.turn = 3
                elif self.turn == 3:
                    for projectile in self.enemy_projectile_group:
                        if now - projectile.birth - self.tick_offsets[self.state] >= 1000:
                            projectile.kill()

                    check_enemy_projectiles(self.player, self.powerups, self.powerup_timers, self.enemy_projectile_group, self.walls_group, self.state)

                    self.enemy_group.update(dt, self.state)
                    self.spawners_group.update(dt, self.state)

                    if self.num_xp >= self.level_up:
                        self.level_up += 10
                        self.num_xp = 0
                        self.powerup_menu.state = 'general'
                        
                        self.powerup_menu_activation = True

                    if self.player.rect.x < 0:
                        self.player.rect.x = self.map_loopover_x
                        self.player.update_distance.x = self.map_loopover_x
                        self.player.aoe.x = self.map_loopover_x

                    elif self.player.rect.x > self.map_loopover_x:
                        self.player.rect.x = 0
                        self.player.update_distance.x = 0
                        self.player.aoe.x = 0

                    if self.player.rect.y < 0:
                        self.player.rect.y = self.map_loopover_y
                        self.player.update_distance.y = self.map_loopover_y
                        self.player.aoe.y = self.map_loopover_y

                    elif self.player.rect.y > self.map_loopover_y:
                        self.player.rect.y = 0
                        self.player.update_distance.y = 0
                        self.player.aoe.y = 0

                    self.turn = 1


                self.projectile_group.update(dt, self.state)
                self.enemy_projectile_group.update(dt, self.state)

                self.all_sprites_group.draw(self.screen, self.player.rect, self.state)
                
                self.xp_bar()
                self.heatlh_bar()

                if self.powerup_menu_activation:
                    self.powerup_menu.update()  
                    self.powerup_menu.draw()                 

            pygame.display.flip() 

        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.start()
    gaem.run()

