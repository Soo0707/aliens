import pygame
from os.path import join

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def draw(self, surface, follows):
        for sprite in self:
            surface.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(-follows.x, -follows.y) + pygame.math.Vector2(640, 360)) # 1/2 of window width and height


class Collidable(pygame.sprite.Sprite):
    def __init__(self,location, texture, groups):
        super().__init__(groups)
        
        self.image = texture
        self.rect = self.image.get_rect(center = location)


class Walls(Collidable):
    def __init__(self, location, texture, groups):
        super().__init__(location, texture, groups)
        
        self.image = texture
        self.rect = self.image.get_rect(center = location)
       

class MapTiles(pygame.sprite.Sprite):
    def __init__(self, location, texture, groups):
        super().__init__(groups)
        self.image = texture
        self.rect = self.image.get_frect(center = location)


class Spawner(Collidable):
    def __init__(self, location, texture, groups):
        super().__init__(location, texture, groups)
        
        self.image = texture
        self.rect = self.image.get_rect(center = location)

        self.last_spawn = 0
        self.can_spawn = True
        self.timeout_ticks = 300

    def update(self, dt):
        if self.can_spawn:
            print(f"Spawned at: {self.rect}")

            self.last_spawn = pygame.time.get_ticks()
            self.can_spawn = False
        elif not self.can_spawn and pygame.time.get_ticks() - self.timeout_ticks <= 0:
            self.can_spawn = True
        
