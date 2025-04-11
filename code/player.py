import pygame
from os import walk, join

class Player(pygame.sprite.Sprite):
    def init(self, location, groups):
        super().__init__()
        
        self.image = pygame.draw.rect("red")
        self.rect = self.image.get_frect(center = location)

        self.aoe = None # for later when we have aoe effects, we'd probably want another rect

        self.direction_vector = pygame.math.Vector2()
        self.speed = 100

        self.images = []

        for group in groups:
            group.add(self)

    
    def input(self):
        pass
    
    def move(self, dt):
        pass
    
    def import_sprites(self):
        pass

    def update(self, dt):
        self.input()
        self.move(dt)
