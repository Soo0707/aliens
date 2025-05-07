import pygame
from os.path import join
from enemy import *

class AllSprites(pygame.sprite.LayeredUpdates):
    def __init__(self, powerups):
        super().__init__()
        self.powerups = powerups
    
    def draw(self, surface, follows):
        if "aussie" in self.powerups:
            temp = pygame.surface.Surface((1280, 720))

            for sprite in self:
                temp.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(-follows.x, -follows.y) + pygame.math.Vector2(640, 360)) # 1/2 of window width and height

            temp_flipped = pygame.transform.flip(temp, 1, 1)
            surface.blit(temp_flipped)
        else:
            for sprite in self:
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

class Spawner(Collidable):
    def __init__(self, location, texture, player, enemies, all_sprites, xp, enemy_textures, groups, powerups):
        super().__init__(location, texture, groups)
        
        self.last_spawn = 0
        self.can_spawn = True
        self.fps_limited = False
        self.timeout_ticks = 2000

        self.player = player
        self.enemies = enemies
        self.all_sprites = all_sprites
        self.xp = xp
        
        self.enemy_textures = enemy_textures
        self.powerups = powerups

    def update(self, dt):
        if self.can_spawn:
            Enemy(
                player=self.player,
                groups=(self.all_sprites, self.enemies),
                location=self.rect.center,
                xp=self.xp,
                all_sprites=self.all_sprites,
                xp_texture = self.enemy_textures["xp"][0],
                textures = None,
                powerups = self.powerups
            )

            self.last_spawn = pygame.time.get_ticks()
            self.can_spawn = False

        if not self.can_spawn and pygame.time.get_ticks() - self.last_spawn >= self.timeout_ticks and not self.fps_limited:
           self.can_spawn = True
        
        if dt > 0.02: # ~ 45 fps
            self.fps_limited = True
        else:
            self.fps_limited = False
