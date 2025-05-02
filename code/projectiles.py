import pygame
from math import atan

class Projectile(pygame.sprite.Sprite):
    def __init__(self, texture, location, direction, groups):
        super().__init__(groups)       
        self.speed = 1000
        self.direction = direction

        if not self.direction.x:
            self.image = pygame.transform.rotate(texture, -atan(self.direction.y) * 180 / 3.142)
        else:
            self.image = pygame.transform.rotate(texture, -atan(self.direction.y / self.direction.x) * 180 / 3.142)
        
        self.rect = self.image.get_frect(center = location)

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt       


class Lazers(pygame.sprite.Sprite):
    def __init__(self, texture, multiplier, location, direction, groups):
        super().__init__(groups)
        self.speed = 3000
        self.direction = direction

        self.texture = texture
        
        self.image = pygame.transform.scale_by(texture, multiplier)
        self.rect = self.image.get_frect(center = location)
        

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

class Circle(pygame.sprite.Sprite):
    def __init__(self, texture, multiplier, player, groups):
        super().__init__(groups)
        self.speed = 6

        self.angle = 5
        self.radius = 50

        self.player = player
        
        self.texture = texture
        
        self.image = pygame.transform.scale_by(texture, multiplier)
        self.rect = self.image.get_frect(center = self.player.rect.center)
        

    def update(self, dt):
        self.angle += self.speed * dt

        offset = pygame.math.Vector2(0, -self.radius).rotate_rad(self.angle)
        self.rect.center = self.player.rect.center + offset
        
