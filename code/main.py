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
        self.turn = -1
        
        self.powerup_list = ["Greenbull", "Milk", "Lazers", "Projectiles", "Blood Sacrifice", "Blood Regeneration", "Shield", "Buckshot", "Aura", "Magnetism", "Block Breaker"]# all possible powerup keys here
        self.powerups = {
                "Projectiles" : [1000, 150, 25], # index: speed, cooldown, damage
                "Lazers" : [1, 750], # index: multiplier for width and damage, cooldown
                "Buckshot": 1,
                "Aura": [0,0,0],
                "done": 0
                }
        self.powerup_timers = {} # key = powerup name, value = expiry (tick now + duration) in ticks
        self.powerup_definitions = {
                "Greenbull" : "Time limited invincibility",
                "Milk" : "Removes and prevents debuffs", 
                "Lazers" : "+DMG, -Timeout",
                "Projectiles" : "+SPD, +DMG, -Timeout",
                "Blood Sacrifice" : "Sacrificing Health for Speed",
                "Blood Regeneration" : "Regains Health after killing",
                "Shield" : "Regains health after some time",
                "Aura" : "Damages surrounding enemies",
                "Buckshot": "+1 projectile for LMB",
                "Magnetism": "Directly collect XP",
                "Block Breaker": "Why Not? Just be fast",
                }
        
        # sprite groups, useful for collision detection and camera later on
        self.all_sprites_group = AllSprites(self.powerups)
        
        self.enemy_group = StatedGroup()
        self.projectile_group = StatedGroup()
        self.enemy_projectile_group = StatedGroup()

        self.xp_group = pygame.sprite.LayeredUpdates()
        self.collidable_group = pygame.sprite.LayeredUpdates()
        self.walls_group = pygame.sprite.LayeredUpdates()
        self.spawners_group = pygame.sprite.LayeredUpdates()

        self.menu_text_group = pygame.sprite.Group()
        self.title_text_group = pygame.sprite.Group()
        self.died_text_group = pygame.sprite.Group()
        self.start_trigger_group = pygame.sprite.Group()
        self.quit_trigger_group = pygame.sprite.Group()
        self.visible_menu_pixels_group = pygame.sprite.Group()

        self.num_xp = 0
        self.level_up = 4

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

        self.player = Player((1344, 3104), self.textures["player"], self.collidable_group, self.all_sprites_group, self.powerups, self.projectile_group, self.all_sprites_group)

        self.powerup_menu = Powerup_Menu(
                                         powerup_list = self.powerup_list,
                                         powerups = self.powerups,
                                         powerup_timers = self.powerup_timers,
                                         powerup_definitions = self.powerup_definitions
                                        )
        self.pause_menu = Pause()
        self.is_paused = False

        self.map_loopover_x = 0
        self.map_loopover_y = 0
        self.load_map()

    def load_map(self):
        map_file = load_pygame(join("..", "assets", "map", "map.tmx"))

        # 32 cause tile size is 32px
        for x, y, texture in map_file.get_layer_by_name("Ground").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites_group)
            self.map_loopover_x = x
            self.map_loopover_y = y

        self.map_loopover_x *= 32
        self.map_loopover_y *= 32

        for x, y, texture in map_file.get_layer_by_name("MenuText").tiles():
            MapTiles((x * 32, y * 32), texture, self.menu_text_group)

        for x, y, texture in map_file.get_layer_by_name("DiedText").tiles():
            MapTiles((x * 32, y * 32), texture, self.died_text_group)
        
        for x, y, texture in map_file.get_layer_by_name("TitleText").tiles():
            MapTiles((x * 32, y * 32), texture, self.title_text_group)

        for x, y, texture in map_file.get_layer_by_name("StartTrigger").tiles():
            MapTiles((x * 32, y * 32), texture, self.start_trigger_group)
        
        for x, y, texture in map_file.get_layer_by_name("QuitTrigger").tiles():
            MapTiles((x * 32, y * 32), texture, self.quit_trigger_group)

        for x, y, texture in map_file.get_layer_by_name("Walls").tiles():
            Walls((x * 32, y * 32), texture, (self.all_sprites_group, self.walls_group))

        for x, y, texture in map_file.get_layer_by_name("Props").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites_group, self.collidable_group))

        for x, y, texture in map_file.get_layer_by_name("Decorations").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites_group)

        for x, y, texture, in map_file.get_layer_by_name("Spawners").tiles():
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
                enemy_textures = self.textures
            )

        for pixel in self.menu_text_group:
            self.all_sprites_group.add(pixel)
            self.visible_menu_pixels_group.add(pixel)

        for pixel in self.title_text_group:
            self.all_sprites_group.add(pixel)
            self.visible_menu_pixels_group.add(pixel)

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

        if "Poison" in self.powerups and now - self.powerups["Poison"] > 1000:
            self.player.health -= 5
            self.powerups["Poison"] = now
        
        if now - self.powerups["Aura"][2] > 1000:
            AOE_collision(self.player, self.enemy_group, self.powerups, self.powerup_timers, self.state)
            self.powerups["Aura"][2] = now
        
        for spawner in self.spawners_group:
            if not spawner.can_spawn and now - spawner.last_spawn >= spawner.timeout_ticks and self.dt < 0.02 and spawner.rect.colliderect(self.player.update_distance):
                spawner.can_spawn = True

    def xp_bar(self):
        self.width = 200 - (self.num_xp / self.level_up) * 200

        self.bg_rect = (1000 , 10 , 250 , 30)
        pygame.draw.rect(self.screen , (128,128,128), self.bg_rect)

        self.progress_rect = (1005 , 15 , 200 , 20)
        pygame.draw.rect(self.screen , (0, 218, 254), self.progress_rect )

        self.empty_rect = (1005 , 15 , self.width , 20)
        pygame.draw.rect(self.screen , (0,0,0), self.empty_rect )

    def health_bar(self):
        self.width = 200  - (self.player.health / self.player.health_permanent) * 200

        self.bg_rect = (1000 , 45 , 250 , 30)
        pygame.draw.rect(self.screen , (128,128,128), self.bg_rect)

        self.progress_rect = (1005 , 50 , 200 , 20)
        pygame.draw.rect(self.screen , (0,255,0), self.progress_rect )

        self.empty_rect = (1005 , 50 , self.width , 20)
        pygame.draw.rect(self.screen , (0,0,0), self.empty_rect )

    def powerup_bar(self):
        if "Drunk" in self.powerups:
            self.drunk_rect = (1230 , 80 , 20 , 20)
            pygame.draw.rect(self.screen , (255 , 255 , 0) , self.drunk_rect)

        if "Poison" in self.powerups:
            self.poison_rect = (1205 , 80 ,20, 20)
            pygame.draw.rect(self.screen, (76, 0, 230) , self.poison_rect)

        if "Greenbull" in self.powerups:
            self.greenbull_rect = (1180 , 80 , 20 , 20)
            pygame.draw.rect(self.screen , (0,255,0) , self.greenbull_rect)

        if "Milk" in self.powerups:
            self.milk_rect = (1155 , 80 , 20 , 20)
            pygame.draw.rect(self.screen , (255,255,255) , self.milk_rect)

    def reset(self):
        for pixel in self.died_text_group:
            self.all_sprites_group.add(pixel)
            self.visible_menu_pixels_group.add(pixel)

        for pixel in self.menu_text_group:
            self.all_sprites_group.add(pixel)
            self.visible_menu_pixels_group.add(pixel)
        self.turn = -1 # back to start menu state
        
        if "Aussie" in self.powerups:
            del self.powerups["Aussie"]

        if "Drunk" in self.powerups:
            del self.powerups["Drunk"]

        if "Poison" in self.powerups:
            del self.powerups["Poison"]

        if "Trap" in self.powerups:
            del self.powerups["Trap"]

        if "Greenbull" in self.powerups:
            del self.powerups["Greenbull"]
        '''
        reset powerups dict and timers dict here
        '''
        for enemies in self.enemy_group:
            enemies.kill()

        for enemy_projectiles in self.enemy_projectile_group:
            enemy_projectiles.kill()

        for projectile in self.projectile_group:
            projectile.kill()

        for xp in self.xp_group:
            xp.kill()

        self.state = 0

        self.num_xp = 0
        self.level_up = 4

        self.player.rect.center = (1344, 3104)

        self.player.health = 100
        self.player.health_permanent = 100

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
                    self.state -= 1

                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.state += 1

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if "Trap" in self.powerups:
                        self.powerups["Trap"] +=1

            if self.is_paused:
                self.pause_menu.do_pause()
            else:
                self.screen.fill("#18215d00")
                self.dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics
                
                if self.turn >= -1:
                    self.player.move_x(self.dt)
                    if "Greenbull" not in self.powerups:
                        collision_x(self.player, self.collidable_group, False, self.state)

                    collision_x(self.player, self.walls_group, False, self.state)

                    self.player.move_y(self.dt)
                    if "Greenbull" not in self.powerups:
                        collision_y(self.player, self.collidable_group, False, self.state)
                    collision_y(self.player, self.walls_group, False, self.state)

                    self.player.update(self.dt, self.state)
                    self.projectile_group.update(self.dt, self.state)
                    self.enemy_projectile_group.update(self.dt, self.state)

                now = pygame.time.get_ticks()
                if self.turn == 1:
                    for xp in self.xp_group:
                        if not xp.rect.colliderect(self.player.update_distance):
                            xp.kill()
                    
                    if "Magnetism" not in self.powerups:
                        collect_xp(self)
                    else:
                        for xp in self.xp_group:
                            self.num_xp += 1
                            xp.kill()

                    for projectile in self.projectile_group:
                        if type(projectile) == Circle:
                            continue

                        if not projectile.rect.colliderect(self.player.update_distance):
                            projectile.kill()

                    collision_projectile(self.projectile_group, self.enemy_group, self.walls_group, self.powerups, self.state)

                    if "Greenbull" not in self.powerups:
                        le_attack(self.player, self.enemy_group, self.powerups, self.powerup_timers, self.state, self.dt)

                    self.check_timers()

                    self.turn = 2
                elif self.turn == 2:
                    for enemy in self.enemy_group:
                        if not enemy.rect.colliderect(self.player.update_distance):
                            enemy.kill()

                    for enemy in self.enemy_group:
                        enemy.move_x(self.dt, self.state)

                    collision_x(self.enemy_group, self.collidable_group, True, self.state)
                    collision_x(self.enemy_group, self.walls_group, True, self.state)

                    for enemy in self.enemy_group:
                        enemy.move_y(self.dt, self.state)

                    collision_y(self.enemy_group, self.collidable_group, True, self.state)
                    collision_y(self.enemy_group, self.walls_group, True, self.state)

                    self.turn = 3
                elif self.turn == 3:
                    for projectile in self.enemy_projectile_group:
                        if not projectile.rect.colliderect(self.player.update_distance):
                            projectile.kill()

                    check_enemy_projectiles(self.player, self.powerups, self.powerup_timers, self.enemy_projectile_group, self.walls_group, self.state)

                    if self.player.health <= 0:
                        self.reset()
                        continue

                    self.enemy_group.update(self.dt, self.state)
                    self.spawners_group.update(self.dt, self.state)

                    if self.num_xp >= self.level_up:
                        self.level_up += 4
                        self.num_xp = 0

                        for spawner in self.spawners_group:
                            if spawner.timeout_ticks > 50:
                                spawner.timeout_ticks -= self.level_up * 5

                            if spawner.timeout_ticks < 50:
                                spawner.timeout_ticks = 50

                        self.turn = -2
                        continue

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
                elif self.turn == -1:
                    # start menu state
                    for sprite in self.quit_trigger_group:
                        if self.player.rect.colliderect(sprite.rect):
                            self.running = False

                    for sprite in self.start_trigger_group:
                        if self.player.rect.colliderect(sprite.rect):
                            self.turn = 1

                            for pixel in self.visible_menu_pixels_group:
                                self.all_sprites_group.remove(pixel)

                            self.visible_menu_pixels_group.empty()

                self.all_sprites_group.draw(self.screen, self.player.rect, self.state)
                self.xp_bar()
                self.health_bar()
                self.powerup_bar()

                if self.turn == -2: # -2 is the powerup menu state
                    self.powerup_menu.update()
                    self.powerup_menu.general()
                    if self.powerups["done"]:
                        self.turn = 1
                        self.powerups["done"] = 0


            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()

