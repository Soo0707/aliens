import pygame
from math import atan

class Projectile(pygame.sprite.Sprite):
    def __init__(self, speed, damage, state, texture, location, direction, groups):
        super().__init__(groups)       
        self.speed = speed
        self.direction = direction
        self.damage = damage

        self.state = state

        if not self.direction.x:
            self.image = pygame.transform.rotate(texture, -atan(self.direction.y) * 180 / 3.142)
        else:
            self.image = pygame.transform.rotate(texture, -atan(self.direction.y / self.direction.x) * 180 / 3.142)
        
        self.rect = self.image.get_frect(center = location)

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt       


class Lazers(pygame.sprite.Sprite):
    def __init__(self, texture, state, multiplier, location, direction, groups):
        super().__init__(groups)
        self.speed = 3000
        self.direction = direction
        self.state = state
        self.damage = 25 * multiplier

        self.texture = texture
        
        self.image = pygame.transform.scale_by(texture, multiplier)
        self.rect = self.image.get_frect(center = location)
        
    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

class Circle(pygame.sprite.Sprite):
    def __init__(self, texture, multiplier, player, groups):
        super().__init__(groups)

        for group in groups:
            group.change_layer(self,2)

        self.speed = 1
        self.multiplier = multiplier
        self.texture = texture

        self.angle = 5
        self.radius = 50

        self.player = player
        
        self.texture = texture
        self.damage = 5
        
        self.image = pygame.transform.scale_by(self.texture, self.multiplier)
        self.rect = self.image.get_frect(center = self.player.rect.center)

    def update(self, dt):
        self.angle += self.speed * dt
        offset = pygame.math.Vector2(0, -self.radius).rotate_rad(self.angle)
        self.rect.center = self.player.rect.center + offset

    def upgrade(self,powerups):
        self.multiplier = powerups["Orb"][0] 
        self.speed = powerups["Orb"][1]
        self.damage =powerups["Orb"][2]

        if self.multiplier >= 2:
            self.multiplier = 2

        self.image = pygame.transform.scale_by(self.texture, self.multiplier)
        self.rect = self.image.get_frect(center = self.player.rect.center)

        powerups["Orb"][3] = False

class Beer(pygame.sprite.Sprite):
    def __init__(self, textures, state, location, direction, groups):
        super().__init__(groups)
        self.image_index = 0
        self.textures = textures

        self.state = state
        
        self.image = self.textures[0]
        self.direction = direction
        self.speed = 500

        self.rect = self.image.get_rect(center = location)

    def animate(self, dt):
        self.image_index += 50 * dt
        self.image = self.textures[int(self.image_index) % len(self.textures)]
    
    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        self.animate(dt)

