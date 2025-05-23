import pygame

from bomber import *
from australian import *
from poison import *
from projectiles import *
from trapper import *

def collision_x(target1, target2, iterable, state):
    if iterable:
        for item1 in target1: 
            if item1.state != state: # used for enemies, the player transcends states, so the else case doesn't have it
                continue

            for item2 in target2:
                if item1.rect.colliderect(item2.rect):
                    if item1.direction.x > 0:
                        item1.rect.right = item2.rect.left
                    elif item1.direction.x < 0:
                        item1.rect.left = item2.rect.right
    else:
        for item in target2:
            if target1.rect.colliderect(item.rect):
                if target1.direction.x > 0:
                    target1.rect.right = item.rect.left
                elif target1.direction.x < 0:
                    target1.rect.left = item.rect.right

def collision_y(target1, target2, iterable, state):
    if iterable:
        for item1 in target1:
            if item1.state != state:
                continue
            
            for item2 in target2:
                if item1.rect.colliderect(item2.rect):
                    if item1.direction.y > 0:
                        item1.rect.bottom = item2.rect.top
                    elif item1.direction.y < 0:
                        item1.rect.top = item2.rect.bottom
    else:
        for item in target2:
            if target1.rect.colliderect(item.rect):
                if target1.direction.y > 0:
                    target1.rect.bottom = item.rect.top
                elif target1.direction.y < 0:
                    target1.rect.top = item.rect.bottom


def collision_projectile(projectiles, enemies, walls, state):
    for projectile in projectiles:
        if type(projectile) == Circle:
            continue

        if hasattr(projectile, "state") and projectile.state != state:
            continue

        for wall in walls:
            if projectile.rect.colliderect(wall):
                projectile.kill()

        for enemy in enemies:
            if projectile.rect.colliderect(enemy):
                enemy.health -= 100
                if type(projectile) == Projectile:
                    projectile.kill()

def check_enemy_projectiles(player, powerups, powerup_timers, enemy_projectile_group, walls, state):
    now = pygame.time.get_ticks()

    for projectile in enemy_projectile_group:
        if projectile.state != state:
            continue

        if projectile.rect.colliderect(player.rect):
            if type(projectile) == Beer and "Milk" not in powerups:
                powerups["Drunk"] = 0
                powerup_timers["Drunk"] = now + 1000
            projectile.kill()

        for wall in walls:
            if projectile.rect.colliderect(wall.rect):
                projectile.kill()

def le_attack(player, enemy_group, powerups, powerup_timers, state,dt):
    now = pygame.time.get_ticks()
    for enemy in enemy_group:
        if enemy.state != state:
            continue

        if enemy.can_attack_primary and enemy.rect.colliderect(player.rect):
            player.health -= enemy.attack
            enemy.can_attack_primary = False
            enemy.last_attack_primary = now
             
            if type(enemy) == Australian and "Milk" not in powerups:
                powerups["Aussie"] = 0
                powerup_timers["Aussie"] = now + 500
            
            elif type(enemy) == Poison and "Milk" not in powerups:
                powerups["Poison"] = pygame.time.get_ticks()
                powerup_timers["Poison"] = now + 5000

            elif type(enemy) == Bomber:
                enemy.plode = True
                enemy.explode(dt)
            
            elif type(enemy) == Trapper and "Milk" not in powerups:
                powerups["Trap"] = 0

def collect_xp(self):
    for orb in self.xp_group:
                        if self.player.rect.colliderect(orb.rect):
                            self.num_xp = self.num_xp + 1
                            orb.kill()
                

def AOE_collision(player, enemy_group, powerups, powerup_timers, state):
    for enemy in enemy_group:
        if enemy.state != state:
            continue

        if enemy.rect.colliderect(player.aoe):
            enemy.health -= 2
                
