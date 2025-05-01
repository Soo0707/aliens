import pygame
from os.path import join
from math import atan, sin, cos, pi

class Projectile(pygame.sprite.Sprite):
    def __init__(self, texture, location, direction, collidables, enemies, groups):
        super().__init__(groups)       
        self.speed = 1000
        self.direction = direction

        self.collidables = collidables
        self.enemies = enemies
        
        if not self.direction.x:
            self.image = pygame.transform.rotate(texture, -atan(self.direction.y) * 180 / 3.142)
        else:
            self.image = pygame.transform.rotate(texture, -atan(self.direction.y / self.direction.x) * 180 / 3.142)
        
        self.rect = self.image.get_frect(center = location)

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        
        for groups in self.collidables:
            for collidable in groups:
                if self.rect.colliderect(collidable):
                    self.kill()

        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                enemy.health -= 100
                self.kill()


class Lazers(pygame.sprite.Sprite):
    def __init__(self, texture, multiplier, location, direction, collidables, enemies, groups):
        super().__init__(groups)
        self.speed = 3000
        self.direction = direction

        self.collidables = collidables
        self.enemies = enemies
        
        self.texture = texture
        
        self.image = pygame.transform.scale_by(texture, multiplier)
        self.rect = self.image.get_frect(center = location)
        

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        for groups in self.collidables:
            for collidable in groups:
                if self.rect.colliderect(collidable):
                    self.kill()

        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                enemy.health -= 100
                self.kill()

class Circle(pygame.sprite.Sprite):
    def __init__(self, texture, multiplier,player, collidables, enemies, groups):
        super().__init__(groups)
        self.speed = 6

        self.angle = 5
        self.radius = 50

        self.player = player

        self.collidables = collidables
        self.enemies = enemies
        
        self.texture = texture
        
        self.image = pygame.transform.scale_by(texture, multiplier)
        self.rect = self.image.get_frect(center = self.player.rect.center)
        

    def update(self, dt):
        

        self.angle += self.speed * dt
        #self.angle %= 2 * pi

        #self.rect.x = self.player.rect.centerx + ((self.radius * sin(self.angle)))
        #self.rect.y = self.player.rect.centery + ((self.radius * cos(self.angle))) 

        offset = pygame.math.Vector2(0, -self.radius).rotate_rad(self.angle)
        self.rect.center = self.player.rect.center + offset
        
        
        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                enemy.health =- 100
