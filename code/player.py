import pygame
from os.path import join
from os import listdir

from projectiles import *

class Player(pygame.sprite.Sprite):
    def __init__(self, location, collidables, all_sprites, powerups, projectiles, groups):
        super().__init__(groups)
        
        all_sprites.change_layer(self, 2)

        self.image = pygame.image.load(join("..", "assets", "player", "S", "0.png")).convert_alpha()

        self.rect = self.image.get_rect(center = location)

        self.aoe = None # for later when we have aoe effects, we'd probably want another rect

        self.direction = pygame.math.Vector2()

        self.bearing = 'S' # either N, S, E, W
        self.image_index = 0

        self.images = {
                "N": [],
                "S": [],
                "E": [],
                "W": []
                }

        self.import_images()

        self.all_sprites = all_sprites
        self.collidables = collidables
        self.projectiles = projectiles

        self.lmb_cooldown = 100
        self.can_lmb = True
        self.last_lmb = 0
        self.projectile_texture = pygame.image.load(join("..", "assets", "player", "projectile.png")).convert_alpha()

        self.rmb_cooldown = 1000
        self.can_rmb = True
        self.last_rmb = 0
        self.lazer_texture_horizontal = pygame.image.load(join("..", "assets", "player", "lazer.png")).convert_alpha()
        self.lazer_texture_vertical = pygame.transform.rotate(self.lazer_texture_horizontal, 90)
        
        self.powerups = powerups
        if "blood_sacrifice" in self.powerups:
            self.speed = 400
            self.health = 70
        else:
            self.speed = 300
            self.health = 100
    
    
    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        
        if "drunk" in self.powerups:
            self.direction.x = -self.direction.x
            self.direction.y = -self.direction.y

        if self.direction:
            self.direction = self.direction.normalize()

        mouse = pygame.mouse.get_pressed()

        if mouse[0] and self.can_lmb:
            mouse_pos = pygame.mouse.get_pos()
            directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

            if "drunk" not in self.powerups:
                Projectile(
                        self.projectile_texture,
                        self.rect.center,
                        pygame.math.Vector2(mouse_pos[0] - 640, mouse_pos[1] - 360).normalize(), # 1/2 of WINDOW_WIDTH and WINDOW_HEIGHT
                        (self.all_sprites, self.projectiles)
                        )
            else:
                for direction in directions:
                    Lazers(
                            self.lazer_texture_horizontal,
                            self.powerups["lazer_width"],
                            self.rect.center,
                            pygame.math.Vector2(direction),
                            (self.all_sprites, self.projectiles)
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
                            self.powerups["lazer_width"],
                            self.rect.center,
                            pygame.math.Vector2(direction),
                            (self.all_sprites, self.projectiles)
                            )
            else:
                Projectile(
                        self.projectile_texture,
                        self.rect.center,
                        pygame.math.Vector2(mouse_pos[0] - 640, mouse_pos[1] - 360).normalize(), # 1/2 of WINDOW_WIDTH and WINDOW_HEIGHT
                        (self.all_sprites, self.projectiles)
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
        

    def import_images(self):
        for key in self.images:
            for item in sorted(listdir(join("..", "assets", "player", key))):
                self.images[key].append(pygame.image.load(join("..", "assets", "player", key, item)).convert_alpha())

    def update(self, dt):
        if not self.can_lmb and pygame.time.get_ticks() - self.last_lmb >= self.lmb_cooldown:
            self.can_lmb = True

        if not self.can_rmb and pygame.time.get_ticks() - self.last_rmb >= self.rmb_cooldown:
            self.can_rmb = True

        self.input()
        self.update_bearing()
        self.animate(dt)
