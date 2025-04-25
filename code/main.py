import pygame
from pytmx.util_pygame import load_pygame

from player import *
from enemy import *
from allsprites import *
#from spawner import *

class game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.running = True

        # sprite groups, useful for collision detection and camera later on
        self.all_sprites = AllSprites()
        self.collidables = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.setup()
    
    def setup(self):
        background = load_pygame(join("..", "assets", "map", "map.tmx"))

        # 32 cause tile size is 32px
        for x, y, texture in background.get_layer_by_name("Ground").tiles():
            MapTiles((x * 32, y * 32), texture, self.all_sprites)

        for x, y, texture in background.get_layer_by_name("Walls").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        for x, y, texture in background.get_layer_by_name("Props").tiles():
            Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        #for x, y, texture, in background.get_layer_by_name("Spawners").tiles():
            #Collidable((x * 32, y * 32), texture, (self.all_sprites, self.collidables))

        self.player = Player((400, 300), self.collidables, self.enemies, self.all_sprites, self.all_sprites)


    
        enemy = Enemy(
            player = self.player,
            groups = self.all_sprites,
            location = (500, 200),
            collide = self.collidables,
            attack = 10
        )

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
        
            
    #
    #def Rollerskates(Player, self):
        #if rollerskates in powerups:
            #self.health = self.health * 0.8
            #self.speed = self.speed * 1.2
            
    #def AOE_DAMAGE_BONUS(Player, self, enemy):
        #if dmg_bonus in powerups:
            #enemy in self.rect idk
        
    #def shield(PLayer, self):
        #current_time = pygame.time.get_ticks()
        #current_time = current_time/1000
        #if shield in powerups:
            #shield_health = self.health * 0.2
            #if current_time % 15 == 0:
                #shield_health = self.health * 0.2
    #            
            
        
    

if __name__ == "__main__":
    gaem = game()
    gaem.run()
