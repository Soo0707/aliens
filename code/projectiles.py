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
<<<<<<< HEAD
        self.rect.y += self.direction.y * self.speed * dt

        for collidable in self.collidables:
            if self.rect.colliderect(collidable):
                self.kill()

        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                enemy.health -= 100
                self.kill()
=======
        self.rect.y += self.direction.y * self.speed * dt       
>>>>>>> 39db91dbf442dc27425ea1e60973f07a3cd3f01f


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
<<<<<<< HEAD

        for collidable in self.collidables:
            if self.rect.colliderect(collidable):
                self.kill()

        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                enemy.health -= 100
                self.kill()
=======
>>>>>>> 39db91dbf442dc27425ea1e60973f07a3cd3f01f
