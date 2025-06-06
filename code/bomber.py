from enemy import *

class Bomber(Enemy):
    def __init__(self, player,state,location,powerups, textures,bomber_explosion_texture, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups)

        self.player = player
        self.images = textures["normal"]
        self.images_flash = textures["flash"]
        self.image = self.images[0]
        self.image_index = 0
        self.speed = 700
        self.rect = self.image.get_rect(center = location)

        self.plode = False
        self.plode_index = 0
        self.explode_images= bomber_explosion_texture
        self.explode_image = self.explode_images[0]

        self.attack = 15

    

    def explode(self , dt):
        self.plode_index += 50 * dt

        self.image = self.explode_images[int(self.plode_index) % len(self.explode_images)]
        if self.plode_index >= len(self.explode_images):
            self.kill()
        
    
    def update(self, dt):
        now = pygame.time.get_ticks()
        
        if self.health <= 0:
            Orb(self.xp_texture, self.rect.center, (self.all_sprites_group, self.xp_group))
            self.kill()

        if not self.can_attack_primary and now - self.last_attack_primary >= self.attack_cooldown_primary:
            self.can_attack_primary = True
       
        self.set_direction()
        if not self.plode:
            self.animate(dt)
        else:
            self.explode(dt)
