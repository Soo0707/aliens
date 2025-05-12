import pygame
from os.path import join
from os import listdir

from projectiles import *

class Player(pygame.sprite.Sprite):
    def __init__(self, location, textures, collidable_group, all_sprites_group, powerups, projectile_group, groups):
        super().__init__(groups)
        
        all_sprites_group.change_layer(self, 2)

        self.powerups = powerups

        self.images = textures
        self.image =  self.images["S"][0]
        self.rect = self.image.get_rect(center = location)

        self.aoe = None # for later when we have aoe effects, we'd probably want another rect

        self.direction = pygame.math.Vector2()

        self.bearing = 'S' # either N, S, E, W
        self.image_index = 0
        
        self.all_sprites_group = all_sprites_group
        self.collidable_group = collidable_group
        self.projectile_group = projectile_group

        self.lmb_cooldown = self.powerups["projectiles"][1]
        self.can_lmb = True
        self.last_lmb = 0
        self.projectile_texture = self.images["projectile"][0]

        self.rmb_cooldown = self.powerups["lazers"][1]
        self.can_rmb = True
        self.last_rmb = 0
        self.lazer_texture_horizontal = self.images["lazer"][0]
        self.lazer_texture_vertical = pygame.transform.rotate(self.lazer_texture_horizontal, 90)

        self.powerups = powerups
        self.speed = 300
        self.health = 100
        self.health_permanent = 100

        self.circle_texture = self.images["circle"][0]
        self.orb = 0
        self.orb_spawn = True
    
    def input(self, state):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        
        if "drunk" in self.powerups:
            self.direction.x = -self.direction.x
            self.direction.y = -self.direction.y

        if self.direction:
            self.direction = self.direction.normalize()
            
        if "blood_sacrifice" in self.powerups:
            self.speed = 300 + (50* (1 + self.powerups["blood_sacrifice"]))
            self.health = 80
            self.health_permanent = 80

        mouse = pygame.mouse.get_pressed()

        mouse_pos = pygame.mouse.get_pos()
        mouse_direction = pygame.math.Vector2(mouse_pos[0] - 640, mouse_pos[1] - 360) # 1/2 of WINDOW_WIDTH and WINDOW_HEIGHT
        
        if mouse_direction:
            mouse_direction = mouse_direction.normalize()

        if mouse[0] and self.can_lmb:
            directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

            if "drunk" not in self.powerups:
                Projectile(
                        self.powerups["projectiles"][0],
                        state,
                        self.projectile_texture,
                        self.rect.center,
                        mouse_direction,
                        (self.all_sprites_group, self.projectile_group)
                        )
            else:
                for direction in directions:
                    Lazers(
                            self.lazer_texture_horizontal,
                            state,
                            self.powerups["lazers"][0],
                            self.rect.center,
                            pygame.math.Vector2(direction),
                            (self.all_sprites_group, self.projectile_group)
                            )
            
            self.can_lmb = False
            self.last_lmb = pygame.time.get_ticks()

        if mouse[2] and self.can_rmb:
            mouse_pos = pygame.mouse.get_pos()
            directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

            if "drunk" not in self.powerups:
                for direction in directions:
                    Lazers(
                            self.lazer_texture_horizontal,
                            state,
                            self.powerups["lazers"][0],
                            self.rect.center,
                            pygame.math.Vector2(direction),
                            (self.all_sprites_group, self.projectile_group)
                            )
            else:
                Projectile(
                        self.powerups["projectiles"][0],
                        state,
                        self.projectile_texture,
                        self.rect.center,
                        mouse_direction,
                        (self.all_sprites_group, self.projectile_group)
                        )

            self.can_rmb = False
            self.last_rmb = pygame.time.get_ticks()



        if self.orb == 0 and mouse[1]:
            self.orb += 1
            Circle(
                self.circle_texture,
                state,
                1, #size multiplier
                self,
                (self.projectile_group, self.all_sprites_group),
            )


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
        
        #self.aoe.x += self.direction.x * self.speed * dt
    def move_y(self, dt):
        self.rect.y += self.direction.y * self.speed * dt

        #self.aoe.y += self.direction.y * self.speed * dt
        
    
    def animate(self, dt):
        if self.direction and "greenbull" not in self.powerups:
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

        self.input(state)
        self.update_bearing()
        self.animate(dt)