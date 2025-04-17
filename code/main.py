import pygame
from pytmx.util_pygame import load_pygame

from player import *
from collidable import *
from allsprites import *

class game():
    def __init__(self):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True

        # sprite groups, useful for collision detection and camera later on
        self.all_sprites = AllSprites()
        self.map_tiles = pygame.sprite.Group()
        self.collidables = pygame.sprite.Group()

        self.setup()

        self.health = 100
        self.powerups = {}

    
    def setup(self):
        self.player = Player((400, 300), self.collidables, self.all_sprites)
        
        temp = pygame.image.load(join("..", "assets", "collidable.png")).convert_alpha()
        self.a = Collidable((800, 400), temp, (self.collidables, self.all_sprites))
        self.b = Collidable((100, 60), temp, (self.collidables, self.all_sprites))

    def run(self):
        while self.running:
            # quits elegantly, never use this for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics
            
            self.all_sprites.update(dt)

            self.all_sprites.draw(self.screen, self.player.rect)

            pygame.display.flip() # updates screen


        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()
