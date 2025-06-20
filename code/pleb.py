from enemy import *

class Pleb(Enemy):
    def __init__(self, player, state, location, powerups, textures, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups)
        self.speed = 450
        self.health = 50
        self.images = textures["normal"]
        self.images_flash = textures["flash"]
        
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = location)
        self.image_index = 0
        self.animation_speed = 30