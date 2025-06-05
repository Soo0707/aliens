import pygame

from random import randint

from australian import *
from drunkard import *
from poison import *
from bomber import *
from trapper import *
from bigman import *

class AllSprites(pygame.sprite.LayeredUpdates):
    def __init__(self, powerups):
        super().__init__()
        self.powerups = powerups
    
    def draw(self, surface, follows, state):
        if "Aussie" in self.powerups:
            temp = pygame.surface.Surface((1280, 720))
            temp.fill("#18215d00")

            for sprite in self:
                if hasattr(sprite, "state") and sprite.state != state:
                    continue
                
                if sprite.rect.x < follows.x - 672 or sprite.rect.x > follows.x + 640:
                    continue

                if sprite.rect.y < follows.y - 392 or sprite.rect.y > follows.y + 360:
                    continue

                temp.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(-follows.x, -follows.y) + pygame.math.Vector2(640, 360)) # 1/2 of window width and height

            temp_flipped = pygame.transform.flip(temp, 1, 1)
            surface.blit(temp_flipped)
        else:
            for sprite in self:
                if hasattr(sprite, "state") and sprite.state != state:
                    continue

                if sprite.rect.x < follows.x - 672 or sprite.rect.x > follows.x + 640:
                    continue

                if sprite.rect.y < follows.y - 392 or sprite.rect.y > follows.y + 360:
                    continue

                surface.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(-follows.x, -follows.y) + pygame.math.Vector2(640, 360))        


class Collidable(pygame.sprite.Sprite):
    def __init__(self,location, texture, groups):
        super().__init__(groups)
        
        self.image = texture
        self.rect = self.image.get_rect(center = location)

class Walls(Collidable):
    def __init__(self, location, texture, groups):
        super().__init__(location, texture, groups)
       

class DecorTiles(pygame.sprite.Sprite):
    def __init__(self, location, texture, group):
        super().__init__(group)
        group.change_layer(self, 3)
        self.image = texture
        self.rect = self.image.get_rect(center = location)

class MapTiles(pygame.sprite.Sprite):
    def __init__(self, location, texture, groups):
        super().__init__(groups)
        self.image = texture
        self.rect = self.image.get_rect(center = location)

class StatedGroup(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()

    def update(self, dt, state):
        for sprite in self:
            if hasattr(sprite, "state") and sprite.state != state:
                continue
            sprite.update(dt)

class Spawner(Collidable):
    def __init__(self, location, texture, player, powerups, enemy_textures, enemy_projectile_group, enemy_group, all_sprites_group, xp_group, groups):
        super().__init__(location, texture, groups)
        
        self.last_spawn = 0
        self.can_spawn = True
        self.timeout_ticks = 4000

        self.rect = self.image.get_rect(center = location)
        self.player = player
        self.all_sprites_group = all_sprites_group
        self.enemy_group = enemy_group
        self.xp_group = xp_group
        self.enemy_projectile_group = enemy_projectile_group

        self.enemy_textures = enemy_textures
        self.powerups = powerups

        self.random_index = 0
        self.rands = [randint(0, 50) for x in range(20)]

    def update(self, dt, state):
        if self.can_spawn:
            n = self.rands[self.random_index]
            
            if n < 10 and self.timeout_ticks <= 2000:
                BigMan(
                    player=self.player,
                    groups=(self.all_sprites_group, self.enemy_group),
                    state = state,
                    location=self.rect.center,
                    textures = self.enemy_textures["big_man"],
                    xp_group=self.xp_group,
                    all_sprites_group = self.all_sprites_group,
                    xp_texture = self.enemy_textures["xp"][0],
                    powerups=self.powerups
                    )

            if n >= 10 and n < 20:
                Australian(
                    player=self.player,
                    groups=(self.all_sprites_group, self.enemy_group),
                    state = state,
                    location=self.rect.center,
                    textures = self.enemy_textures["australian"],
                    xp_group=self.xp_group,
                    all_sprites_group = self.all_sprites_group,
                    xp_texture = self.enemy_textures["xp"][0],
                    powerups=self.powerups
                    )
            
            if n >= 20 and n < 25:
                Bomber(
                    player=self.player,
                    groups=(self.all_sprites_group, self.enemy_group),
                    state = state,
                    textures = self.enemy_textures["bomber"],
                    location=self.rect.center,
                    powerups=self.powerups,
                    xp_texture=self.enemy_textures["xp"][0],
                    xp_group=self.xp_group,
                    bomber_explosion_texture = self.enemy_textures["bomber_explosion"],
                    all_sprites_group = self.all_sprites_group,
                    )
            
            if n >= 25 and n < 30:
                Trapper(
                    player=self.player,
                    groups=(self.all_sprites_group, self.enemy_group),
                    state = state,
                    location=self.rect.center,
                    textures = self.enemy_textures["trapper"],
                    xp_group=self.xp_group,
                    all_sprites_group = self.all_sprites_group,
                    xp_texture = self.enemy_textures["xp"][0],
                    powerups=self.powerups
                    )

            if n >= 30 and n < 40:
                Poison(
                    player=self.player,
                    groups=(self.all_sprites_group, self.enemy_group),
                    state = state,
                    location=self.rect.center,
                    textures = self.enemy_textures["poison"],
                    xp_group=self.xp_group,
                    all_sprites_group = self.all_sprites_group,
                    xp_texture = self.enemy_textures["xp"][0],
                    powerups=self.powerups
                    )
            
            if n >= 40 and n < 50:
                Drunkard(
                    player=self.player,
                    groups=(self.all_sprites_group, self.enemy_group),
                    state = state,
                    location=self.rect.center,
                    textures = self.enemy_textures["drunkard"],
                    beer_textures = self.enemy_textures["beer"],
                    enemy_projectile_group = self.enemy_projectile_group,
                    xp_group=self.xp_group,
                    all_sprites_group = self.all_sprites_group,
                    xp_texture = self.enemy_textures["xp"][0],
                    powerups=self.powerups
                    )
                
            self.random_index = (self.random_index + 1) % 20
            self.last_spawn = pygame.time.get_ticks()
            self.can_spawn = False

