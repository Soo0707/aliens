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
        pygame.font.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.state = 0
        self.turn = -1
        self.state_timeout = 0
        
        self.powerup_list = ["Greenbull", "Milk", "Lazers", "Projectiles", "Blood Sacrifice", "Blood Regeneration", "Shield", "Buckshot", "Aura", "Magnetism" , "Orb", "Block Breaker"] # all possible powerup keys here
        self.powerups = {
                "Projectiles" : [1000, 250, 25], # index: speed, cooldown, damage
                "Lazers" : [1, 750], # index: multiplier for width and damage, cooldown
                "Buckshot": 1,
                "Aura": [0,0,0],
                "Orb" : [0.2,1,5,False], #Size, Speed , Damage , do_update
                "done": 0
                }
        self.powerup_timers = {} # key = powerup name, value = expiry (tick now + duration) in ticks
        self.powerup_definitions = {
                "Greenbull" : "Time limited invincibility",
                "Milk" : "Removes and prevents debuffs", 
                "Lazers" : "Increase DMG & Reduced Cooldown of RMB",
                "Projectiles" : "Increase SPD, DMG & Reduced Cooldown of LMB",
                "Blood Sacrifice" : "Sacrificing Health for Speed",
                "Blood Regeneration" : "Regains Health after killing",
                "Shield" : "Regains health after some time",
                "Aura" : "Damages surrounding enemies",
                "Buckshot": "+2 projectile for LMB",
                "Magnetism": "Directly collect XP",
                "Block Breaker": "Why Not? Just be fast",
                "Orb" : "Increase DMG, SIZE & SPD of Orb"
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

        self.font = pygame.font.Font(None, 35)
        self.num_xp = 0
        self.level_up = 2

        self.textures = {
                "bomber": {"normal": [], "flash" : []},
                "bomber_explosion" : [],
                "drunkard": {"normal": [], "flash" : []},
                "big_man": {"normal": [], "flash" : []},
                "poison": {"normal": [], "flash" : []},
                "trapper": {"normal": [], "flash" : []},
                "australian": {"normal": [], "flash" : []},
                "pleb": {"normal": [], "flash" : []},
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
        
        pygame.display.set_icon(self.textures["player"]["S"][0])
        pygame.display.set_caption("aliens")
        
        #initialise mixer
        pygame.mixer.init()
        self.sounds = {
                "level_up" : None,
                "lmb": None,
                "rmb": None,
                "xp": None,
                "damage": None,
                "poison": None,
                "explosion": None,
                "menu_select": None,
                "menu_hover": None,
                "pause": None,
                "unpause": None
                }
        
        self.load_sounds()
        
        self.player_spawn = (0, 0)
        with open(join("..", "assets", "map", "spawn.txt"), "r") as file:
            x = int(file.readline().strip())
            y = int(file.readline().strip())
            self.player_spawn = (x, y)


        self.player = Player(self.player_spawn, self.textures["player"], self.collidable_group, self.all_sprites_group, self.powerups, self.projectile_group, self.all_sprites_group, self.sounds)

        self.powerup_menu = Powerup_Menu(
                                         powerup_list = self.powerup_list,
                                         powerups = self.powerups,
                                         powerup_timers = self.powerup_timers,
                                         powerup_definitions = self.powerup_definitions,
                                         sounds = self.sounds
                                        )
        self.pause_menu = Pause(state = self.state)
        self.is_paused = False

        self.map_loopover_x = 0
        self.map_loopover_y = 0
        self.load_map()

    def load_sounds(self):
        for key in self.sounds:
            self.sounds[key] = pygame.mixer.Sound(join("..","assets", "sounds", f"{key}.wav"))

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
        enemies = {"australian", "big_man", "bomber", "drunkard", "poison", "trapper", "pleb"}
        for key in self.textures:
            if key == "player":
                continue

            if key in enemies:
                for item in sorted(listdir(join("..", "assets", "enemy", key, "normal"))):
                    self.textures[key]["normal"].append(pygame.image.load(join("..", "assets", "enemy", key, "normal", item)).convert_alpha())

                for item in sorted(listdir(join("..", "assets", "enemy", key, "flash"))):
                    self.textures[key]["flash"].append(pygame.image.load(join("..", "assets", "enemy", key, "flash", item)).convert_alpha())
            else:
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
            self.sounds["poison"].play()
            self.player.health -= 5
            self.powerups["Poison"] = now
        
        if now - self.powerups["Aura"][2] > 1000:
            AOE_collision(self.player, self.enemy_group, self.powerups, self.powerup_timers, self.state)
            self.powerups["Aura"][2] = now
    
        if now - self.state_timeout <= 0:
            self.state_timeout = 0
        
        for spawner in self.spawners_group:
            if not spawner.can_spawn and now - spawner.last_spawn >= spawner.timeout_ticks and spawner.rect.colliderect(self.player.update_distance) and self.state_timeout == 0 and self.dt < 0.02:
                spawner.can_spawn = True

    def xp_bar(self):
        self.width = (self.num_xp / self.level_up) * 1260

        self.empty_rect = (10 , 690 , 1260 , 10)
        pygame.Surface.fill(self.screen , (0,0,0), self.empty_rect )
        self.progress_rect = (10 , 690 , self.width , 10)

        pygame.Surface.fill(self.screen , (0, 218, 254), self.progress_rect)

    def health_bar(self):
        self.width = 200  - (self.player.health / self.player.health_permanent) * 200

        self.bg_rect = (1000 , 15 , 250 , 30)
        pygame.Surface.fill(self.screen , (128,128,128), self.bg_rect)

        self.progress_rect = (1005 , 20 , 200 , 20)
        pygame.Surface.fill(self.screen , (0,255,0), self.progress_rect )

        self.empty_rect = (1005 , 20 , self.width , 20)
        pygame.Surface.fill(self.screen , (0,0,0), self.empty_rect )

    def powerup_bar(self):
        now = pygame.time.get_ticks()
        flicker = 5000
        draw_drunk = True
        draw_bull = True
        draw_mag = True
        draw_milk = True
        draw_poison = True

        if "Drunk" in self.powerups:
            duration = self.powerup_timers["Drunk"]

            if duration - now < flicker:
                draw_drunk = (now//250) % 2 == 0

            if draw_drunk:
                self.drunk_rect = (1230 , 50 , 20 , 20)
                pygame.Surface.fill(self.screen , (255 , 255 , 0) , self.drunk_rect)

        if "Poison" in self.powerups:
            duration = self.powerup_timers["Poison"]

            if duration - now < flicker:
                draw_poison = (now//250) % 2 == 0
            
            if draw_poison:
                self.poison_rect = (1205 , 50 ,20, 20)
                pygame.Surface.fill(self.screen, (76, 0, 230) , self.poison_rect)

        if "Greenbull" in self.powerups:
            duration = self.powerup_timers["Greenbull"]

            if duration - now < flicker:
                draw_bull = (now//250) % 2 == 0

            if draw_bull:    
                self.greenbull_rect = (1180 , 50 , 20 , 20)
                pygame.Surface.fill(self.screen , (0,255,0) , self.greenbull_rect)

        if "Milk" in self.powerups:
            duration = self.powerup_timers["Milk"]

            if duration - now < flicker:
                draw_milk = (now//250) % 2 == 0
            
            if draw_milk:
                self.milk_rect = (1155 , 50 , 20 , 20)
                pygame.Surface.fill(self.screen , (255,255,255) , self.milk_rect)

        
        if "Magnetism" in self.powerups:
            duration = self.powerup_timers["Magnetism"]

            if duration - now < flicker:
                draw_mag = (now//250) % 2 == 0

            self.magnet_half = (1140, 50 , 10 ,20)
            self.magnet_other_half = (1130,50,10,20)

            if draw_mag:
                pygame.Surface.fill(self.screen, (0,0,255) , self.magnet_other_half)
                pygame.Surface.fill(self.screen , (255,0,0), self.magnet_half)

    def reset(self):
        for pixel in self.died_text_group:
            self.all_sprites_group.add(pixel)
            self.visible_menu_pixels_group.add(pixel)

        for pixel in self.menu_text_group:
            self.all_sprites_group.add(pixel)
            self.visible_menu_pixels_group.add(pixel)
        self.turn = -1 # back to start menu state
        
        for skibidi in self.powerups.copy():
            if skibidi == "Projectiles":
                self.powerups["Projectiles"] = [1000, 250, 25]
            elif skibidi == "Lazers":
                self.powerups["Lazers"] = [1, 750]
            elif skibidi == "Buckshot":
                self.powerups["Buckshot"] = 1
            elif skibidi == "Aura":
                self.powerups["Aura"] = [0,0,0]
            elif skibidi == "Orb":
                self.powerups["Orb"] = [0.2,1,5,True]
                self.player.orb.upgrade(self.powerups)
            elif skibidi == "done":
                self.powerups["done"] = 0
            else:
                del self.powerups[skibidi]


        for keys in self.powerup_timers.copy():
            del self.powerup_timers[keys]

        for enemy in self.enemy_group:
            enemy.kill()

        for enemy_projectiles in self.enemy_projectile_group:
            enemy_projectiles.kill()

        for projectile in self.projectile_group:
            if type(projectile) == Circle:
                continue
            projectile.kill()

        for xp in self.xp_group:
            xp.kill()

        for spawner in self.spawners_group:
            spawner.timeout_ticks = 4000

        self.state = 0
        self.state_timeout = 0

        self.num_xp = 0
        self.level_up = 2

        self.player.rect.center = self.player_spawn

        self.player.health = 100
        self.player.health_permanent = 100
        self.player.health_permanent_shield = 0

        self.player.speed = 300

    def run(self):
        while self.running:
            # quits elegantly, never use this for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.is_paused:
                        self.is_paused = False
                        self.sounds["unpause"].play()
                    else:
                        self.is_paused = True
                        self.sounds["pause"].play()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q and self.state > 0 and self.state_timeout == 0 and not self.is_paused:
                    self.state -= 1
                    self.state_timeout = pygame.time.get_ticks() + 5000

                if event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.state < 5 and self.state_timeout == 0 and not self.is_paused:
                    self.state += 1
                    self.state_timeout = pygame.time.get_ticks() + 5000

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if "Trap" in self.powerups:
                        self.powerups["Trap"] +=1

            if self.is_paused:
                self.pause_menu = Pause(state = self.state)
                self.pause_menu.do_pause()
            else:
                self.screen.fill("#18215d00")
                
                self.dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics
                if self.turn >= -1:

                    self.player.move_x(self.dt)
                    if "Greenbull" not in self.powerups:
                        collision_x(self.player, self.collidable_group, self.player.update_distance, False, self.state)

                    collision_x(self.player, self.walls_group, self.player.update_distance, False, self.state)

                    self.player.move_y(self.dt)
                    if "Greenbull" not in self.powerups:
                        collision_y(self.player, self.collidable_group, self.player.update_distance, False, self.state)
                    collision_y(self.player, self.walls_group, self.player.update_distance, False, self.state)

                    self.player.update(self.dt, self.state)
                    self.projectile_group.update(self.dt, self.state)
                    self.enemy_projectile_group.update(self.dt, self.state)

                now = pygame.time.get_ticks()
                if self.turn == 1:
                    for xp in self.xp_group:
                        if now - xp.birth > 5000:
                            xp.kill()
                    
                    collect_xp(self)

                    for projectile in self.projectile_group:
                        if type(projectile) == Circle:
                            continue

                        if not projectile.rect.colliderect(self.player.update_distance):
                            projectile.kill()

                    collision_projectile(self.projectile_group, self.enemy_group, self.walls_group, self.powerups, self.state)

                    if "Greenbull" not in self.powerups:
                        le_attack(self.player, self.enemy_group, self.powerups, self.powerup_timers, self.state, self.dt, self.sounds)

                    self.check_timers()

                    self.turn = 2
                elif self.turn == 2:
                    for enemy in self.enemy_group:
                        if not enemy.rect.colliderect(self.player.update_distance):
                            enemy.kill()

                    for enemy in self.enemy_group:
                        enemy.move_x(self.dt, self.state)

                    collision_x(self.enemy_group, self.collidable_group, self.player.update_distance, True, self.state)
                    collision_x(self.enemy_group, self.walls_group, self.player.update_distance, True, self.state)

                    for enemy in self.enemy_group:
                        enemy.move_y(self.dt, self.state)

                    collision_y(self.enemy_group, self.collidable_group, self.player.update_distance, True, self.state)
                    collision_y(self.enemy_group, self.walls_group, self.player.update_distance, True, self.state)

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
                        self.sounds["level_up"].play()
                        self.level_up += 2
                        self.num_xp = 0

                        for spawner in self.spawners_group:
                            if spawner.timeout_ticks > 0:
                                spawner.timeout_ticks -= self.level_up * 5

                            if spawner.timeout_ticks < 0:
                                spawner.timeout_ticks = 0
                        
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

                    if self.powerups["Orb"][3] == True:
                        self.player.orb.upgrade(self.powerups)

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
              

                if "Trap" in self.powerups:
                    space_rect = (487.5 , 640 , 305 , 30)
                    pygame.draw.rect(self.screen, (235,235,235), space_rect , border_radius=10)

                    text = self.font.render("Spam SPACE to Escape", True, (0, 0, 0)) 
                    rect = pygame.Rect((487.5 , 640 , 305 , 30))
                    text_rect = text.get_rect(center = rect.center)
                    self.screen.blit(text, text_rect)

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

