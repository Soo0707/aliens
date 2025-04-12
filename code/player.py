import pygame
from os import walk, join

class Player(pygame.sprite.Sprite):
    def init(self, location, groups):
        super().__init__()
        
        self.image = None
        self.rect = self.image.get_frect(center = location)

        self.aoe = None # for later when we have aoe effects, we'd probably want another rect

        self.direction_vector = pygame.math.Vector2()
        self.speed = 100

        self.bearing = 'S' # either N, S, E, W
        self.image_index = 0

        self.images = {"N": [],
                       "S": [],
                       "E": [],
                       "W": []
                       }

        for group in groups:
            group.add(self)

        self.import_images()
    
    def input(self):
        keys = pygame.key.get_pressed()

        self.direction_vector.x = int(keys[K_d]) - int(keys[K_a])
        self.direction_vector.y = int(keys[K_s]) - int(keys[K_w])

        if self.direction_vector:
            self.direction_vector = self.director_vector.normalize()

        mouse = pygame.mouse.get_pressed()

        if mouse[0]:
            pass

        if mouse[2]:
            pass

    def update_bearing(self):
        if self.direction_vector.x > 0:
            self.bearing = "E"
        elif self.direction_vector.x < 0:
            self.bearing = "W"
        elif self.direction_vector.y > 0:
            self.bearing = "D"
        elif self.direction_vector.y < 0:
            self.bearing = "N"

    def move(self, dt):
        self.rect.x += self.direction_vector.x * self.speed * dt
        self.rect.y += self.direction_vector.y * self.speed * dt

        self.aoe.x += self.direction_vector.x * self.speed * dt
        self.aoe.y += self.direction_vector.y * self.speed * dt
    
    def animate(self, dt):
        if self.direction_vector:
            pass

    def import_images(self):
        pass

    def update(self, dt):
        self.input()
        self.update_bearing()
        self.animate(dt)
        self.move(dt)
