import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, location, collidable, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(join("..", "assets", "player", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = location)

        self.aoe = None # for later when we have aoe effects, we'd probably want another rect

        self.direction_vector = pygame.math.Vector2()
        self.speed = 300

        self.bearing = 'S' # either N, S, E, W
        self.image_index = 0

        self.images = {"N": [],
                       "S": [],
                       "E": [],
                       "W": []
                       }

        self.import_images()

        self.collidables = collidable
    
    def input(self):
        keys = pygame.key.get_pressed()

        self.direction_vector.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction_vector.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if self.direction_vector:
            self.direction_vector = self.direction_vector.normalize()

        mouse = pygame.mouse.get_pressed()

        if mouse[0]:
            print("click left")

        if mouse[2]:
            print("click right")

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

        for collidable in self.collidables:
            if self.rect.colliderect(collidable):
                if self.direction_vector.x > 0:
                    self.rect.right = collidable.rect.left
                elif self.direction_vector.x < 0:
                    self.rect.left = collidable.rect.right
        
        self.rect.y += self.direction_vector.y * self.speed * dt
        

        for collidable in self.collidables:
            if self.rect.colliderect(collidable):
                if self.direction_vector.y > 0:
                    self.rect.bottom = collidable.rect.top
                elif self.direction_vector.y < 0:
                    self.rect.top = collidable.rect.bottom


        '''    
        self.aoe.x += self.direction_vector.x * self.speed * dt
        self.aoe.y += self.direction_vector.y * self.speed * dt
        '''

    
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
