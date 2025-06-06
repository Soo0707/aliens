from enemy import *
from projectiles import Beer

class Drunkard(Enemy):
    def __init__(self, player, state, location, powerups, textures, beer_textures, enemy_projectile_group, xp_texture, xp_group, all_sprites_group, groups):
        super().__init__(player, state, location, powerups, xp_texture, xp_group, all_sprites_group, groups)
        self.speed = 500
        self.images = textures["normal"]
        self.images_flash = textures["flash"]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = location)
        self.health = 50
        self.beer_textures = beer_textures
        self.image_index = 0
        
        self.enemy_projectile_group = enemy_projectile_group
        self.can_attack_secondary = 10000

        self.animation_speed = 60

    def secondary(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        self_pos = pygame.math.Vector2(self.rect.center)

        direction = (player_pos - self_pos)

        if direction:
            direction = direction.normalize()

        Beer(self.beer_textures, self.state, self.rect.center, direction, (self.enemy_projectile_group, self.all_sprites_group))       
