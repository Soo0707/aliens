import pygame
from os.path import join

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def draw(self, surface, follows):
        for sprite in self:
            surface.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(-follows.x, -follows.y) + pygame.math.Vector2(1280 / 2, 720 / 2))
