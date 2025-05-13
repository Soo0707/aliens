import pygame
from os.path import join
from enemy import *
from australian import *
from drunkard import *
from poison import *

class AllSprites(pygame.sprite.LayeredUpdates):
    def __init__(self, powerups):
        super().__init__()
        self.powerups = powerups
    
    def draw(self, surface, follows, state):
        if "aussie" in self.powerups:
            temp = pygame.surface.Surface((1280, 720))

            for sprite in self:
                if hasattr(sprite, "state") and sprite.state != state:
                    continue
                temp.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(-follows.x, -follows.y) + pygame.math.Vector2(640, 360)) # 1/2 of window width and height

            temp_flipped = pygame.transform.flip(temp, 1, 1)
            surface.blit(temp_flipped)
        else:
            for sprite in self:
                if hasattr(sprite, "state") and sprite.state != state:
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
       

class MapTiles(pygame.sprite.Sprite):
    def __init__(self, location, texture, groups):
        super().__init__(groups)
        self.image = texture
        self.rect = self.image.get_frect(center = location)

class StatedGroup(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()

    def update(self, dt, state):
        for sprite in self:
            if sprite.state != state:
                continue
            sprite.update(dt)

class Spawner(Collidable):
    def __init__(self, location, texture, player, powerups, enemy_textures, enemy_projectile_group, enemy_group, all_sprites_group, xp_group, groups):
        super().__init__(location, texture, groups)
        
        self.last_spawn = 0
        self.can_spawn = True
        self.timeout_ticks = 200

        self.player = player
        self.all_sprites_group = all_sprites_group
        self.enemy_group = enemy_group
        self.xp_group = xp_group
        self.enemy_projectile_group = enemy_projectile_group

        self.enemy_textures = enemy_textures
        self.powerups = powerups

    def update(self, dt, state):
        if self.can_spawn:
            '''
            Enemy(
                player=self.player,
                groups=(self.all_sprites_group, self.enemy_group),
                state = state,
                location=self.rect.center,
                powerups=self.powerups,
                xp_group=self.xp_group,
                all_sprites_group = self.all_sprites_group,
                xp_texture = self.enemy_textures["xp"][0],
            )
            '''
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
            
            Poison(
                player=self.player,
                groups=(self.all_sprites_group, self.enemy_group),
                state = state,
                location=self.rect.center,
                textures = self.enemy_textures["poison"],
                xp_group=self.xp_group,
                all_sprites_group = self.all_sprites_group,
                xp_texture = self.enemy_textures["xp"][0],
                powerups=self.powerups)

            self.last_spawn = pygame.time.get_ticks()
            self.can_spawn = False

        if not self.can_spawn and pygame.time.get_ticks() - self.last_spawn >= self.timeout_ticks and dt < 0.02:
           self.can_spawn = True
