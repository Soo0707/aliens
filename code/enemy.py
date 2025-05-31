import pygame

from allsprites import *
from player import  *
from xp import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(groups)
        
        all_sprites_group.change_layer(self, 1)

        self.state = state
       
        self.direction = pygame.math.Vector2()
        self.location = location
        self.health = 100

        self.speed = 300 # Enemy
        self.attack = 5 #Enemy attack 
        self.attack_cooldown_primary = 5000 #attack cooldown
        self.attack_cooldown_secondary = 5000 #attack cooldown
        
        self.last_attack_primary = 0
        self.can_attack_primary = True

        self.last_attack_secondary = 0
        self.can_attack_secondary = True

        self.player = player

        self.all_sprites_group = all_sprites_group
        self.xp_group = xp_group
        
        self.xp_texture = xp_texture
        self.powerups = powerups

        self.animation_speed = 30
        self.flash = False

    def set_direction(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)

        self.direction = (player_pos - enemy_pos)

        if self.direction:
            self.direction = self.direction.normalize()
        
    def move_x(self, dt, state):
        if self.state == state:
            self.rect.x += self.direction.x * self.speed * dt

    def move_y(self, dt, state):
        if self.state == state:
            self.rect.y += self.direction.y * self.speed * dt

    def animate(self, dt):
        if self.direction:
            self.image_index += self.animation_speed * dt
            self.image = self.images[int(self.image_index) % len(self.images)]
        elif self.flash:
            self.image = self.image_flash
        else:
            self.image_index = 0
            self.image = self.images[0] # the 0th image is always the idle frame
    
    def secondary(self):
        pass

    def update(self, dt):
        now = pygame.time.get_ticks()
        
        if self.health <= 0:
            Orb(self.xp_texture, self.rect.center, (self.all_sprites_group, self.xp_group))
            self.kill()
            

            if "Blood Regeneration" in self.powerups:
                self.heal = (2*(1 + self.powerups["Blood Regeneration"]))
                if self.player.health < self.player.health_permanent:
                    self.player.health = self.player.health + self.heal
                    if "Shield" in self.powerups:          
                        if self.player.health > self.player.health_permanent_shield:
                            self.player.health = self.player.health_permanent_shield
                    elif self.player.health > self.player.health_permanent:
                        self.player.health = self.player.health_permanent

        if not self.can_attack_primary and now - self.last_attack_primary >= self.attack_cooldown_primary:
            self.can_attack_primary = True

        if not self.can_attack_secondary and now - self.last_attack_secondary >= self.attack_cooldown_secondary:
            self.can_attack_secondary = True

        self.set_direction()
        self.animate(dt)
        self.secondary()
