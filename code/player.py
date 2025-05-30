import pygame

from random import random, randint
from projectiles import *

class Player(pygame.sprite.Sprite):
    def __init__(self, location, textures, collidable_group, all_sprites_group, powerups, projectile_group, groups, sounds):
        super().__init__(groups)
        
        all_sprites_group.change_layer(self, 2)

        self.powerups = powerups
        self.sounds = sounds

        self.images = textures
        self.image =  self.images["S"][0]
        self.rect = self.image.get_rect(center = location)
        
        self.update_distance = pygame.Rect(location, (1920, 1080))


        self.direction = pygame.math.Vector2()

        self.bearing = 'S' # either N, S, E, W
        self.image_index = 0
        
        self.all_sprites_group = all_sprites_group
        self.collidable_group = collidable_group
        self.projectile_group = projectile_group

        self.lmb_cooldown = self.powerups["Projectiles"][1]
        self.can_lmb = True
        self.last_lmb = 0
        self.projectile_texture = self.images["projectile"][0]

        self.rmb_cooldown = self.powerups["Lazers"][1]
        self.can_rmb = True
        self.last_rmb = 0
        self.lazer_texture_horizontal = self.images["lazer"][0]
        self.lazer_texture_vertical = pygame.transform.rotate(self.lazer_texture_horizontal, 90)

        self.powerups = powerups
        self.speed = 300
        self.health = 100
        self.health_permanent = 100
        self.health_permanent_shield = 0

        self.circle_texture = self.images["circle"][0]
        self.orb =  Circle(
                self.circle_texture,
                self.powerups["Orb"][0],
                self,
                (self.all_sprites_group, self.projectile_group)
            )
   
    def input(self, state):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        
        if "Drunk" in self.powerups:
            self.direction.x = -self.direction.x
            self.direction.y = -self.direction.y

        if "Trap" in self.powerups:
            self.direction.x = 0
            self.direction.y = 0

            if self.powerups["Trap"] >= 5:
                del self.powerups["Trap"]
                

        if self.direction:
            self.direction = self.direction.normalize()

        mouse = pygame.mouse.get_pressed()

        if mouse[0] and self.can_lmb:
            mouse_pos = pygame.mouse.get_pos()
            mouse_direction = pygame.math.Vector2(mouse_pos[0] - 640, mouse_pos[1] - 360) # 1/2 of WINDOW_WIDTH and WINDOW_HEIGHT
            self.sounds["lmb"].play()
            
            if "Drunk" in self.powerups:
                noise = random() * 100
                mouse_direction.x += noise
                mouse_direction.y += noise

                if mouse_direction:
                    mouse_direction = mouse_direction.normalize()

                Projectile(
                        self.powerups["Projectiles"][0],
                        self.powerups["Projectiles"][2],
                        state,
                        self.projectile_texture,
                        self.rect.center,
                        mouse_direction,
                        (self.all_sprites_group, self.projectile_group)
                        )
            else:
                for i in range(self.powerups["Buckshot"]):
                    mouse_direction.x += i / self.powerups["Buckshot"] * 0.5
                    mouse_direction.y += i / self.powerups["Buckshot"] * .5

                    if mouse_direction:
                        mouse_direction = mouse_direction.normalize()

                    Projectile(
                            self.powerups["Projectiles"][0],
                            self.powerups["Projectiles"][2],
                            state,
                            self.projectile_texture,
                            self.rect.center,
                            mouse_direction,
                            (self.all_sprites_group, self.projectile_group)
                            )

            self.can_lmb = False
            self.last_lmb = pygame.time.get_ticks()

        if mouse[2] and self.can_rmb:
            directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
            self.sounds["rmb"].play()

            for direction in directions:
                if direction[1] != 0:
                    lazer_texture = self.lazer_texture_vertical
                else:
                    lazer_texture = self.lazer_texture_horizontal

                Lazers(
                        lazer_texture,
                        state,
                        self.powerups["Lazers"][0],
                        self.rect.center,
                        pygame.math.Vector2(direction),
                        (self.all_sprites_group, self.projectile_group)
                        )

            self.can_rmb = False
            self.last_rmb = pygame.time.get_ticks()



    def update_bearing(self):
        if self.direction.x > 0:
            self.bearing = "E"
        elif self.direction.x < 0:
            self.bearing = "W"
        elif self.direction.y > 0:
            self.bearing = "S"
        elif self.direction.y < 0:
            self.bearing = "N"

        
    def move_x(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
    
    def move_y(self, dt):
        self.rect.y += self.direction.y * self.speed * dt
    
    def animate(self, dt):
        if self.direction and "Greenbull" not in self.powerups:
            self.image_index += 10 * dt
            self.image = self.images[self.bearing][int(self.image_index) % len(self.images[self.bearing])]
        else:
            self.image_index = 0
            self.image = self.images[self.bearing][0] # the 0th image is always the idle frame
    
    def update(self, dt, state):
        if not self.can_lmb and pygame.time.get_ticks() - self.last_lmb >= self.lmb_cooldown:
            self.can_lmb = True

        if not self.can_rmb and pygame.time.get_ticks() - self.last_rmb >= self.rmb_cooldown:
            self.can_rmb = True

        if "Blood Sacrifice" in self.powerups:
            self.speed = 300 + (50* (1 + self.powerups["Blood Sacrifice"]))
            self.health_permanent = 80
            
        if "Shield" in self.powerups:
            now = pygame.time.get_ticks()
            if now % 300 == 0:
                self.shield = 20 * (1 + self.powerups["Shield"])
                self.health = self.health + self.shield
                if self.health_permanent_shield < self.health_permanent + self.shield:
                    self.health_permanent_shield = self.health_permanent + self.shield
                    if "Blood Sacrifice" in self.powerups:
                        self.health_permanent_shield -= 20
                if self.health > self.health_permanent_shield:
                    self.health = self.health_permanent_shield
                    

        x = self.powerups["Aura"][0]
        y = self.powerups["Aura"][1]
        self.aoe = pygame.FRect(0, 0, x, y)        
        self.aoe.center = self.rect.center
        self.update_distance.center = self.rect.center
            
        self.input(state)
        self.update_bearing()
        self.animate(dt)
