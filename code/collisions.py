import pygame

from bomber import *
from australian import *
from projectiles import *

def collision_x(target1, target2, iterable):
    if iterable:
        for item1 in target1:
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

def collision_y(target1, target2, iterable):
    if iterable:
        for item1 in target1:
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


def collision_projectile(projectiles, enemies, props):
    for projectile in projectiles:
        for groups in props:
            for collidable in groups:
                if projectile.rect.colliderect(collidable):
                    projectile.kill()

        for enemy in enemies:
            if projectile.rect.colliderect(enemy):
                enemy.health -= 100
                projectile.kill()

def toggle_spawners(player, spawner_group):
    for spawner in spawner_group:
        if spawner.rect.colliderect(player.rect):
            spawner.can_spawn = True
        else:
            spawner.can_spawn = False

def check_enemy_projectiles(player, powerups, powerup_timers, enemy_projectile_group, walls):
    now = pygame.time.get_ticks()
    for projectile in enemy_projectile_group:
        if projectile.rect.colliderect(player.rect):
            if type(projectile) == Beer:
                powerups["drunk"] = 0
                powerup_timers["drunk"] = now + 1000
            projectile.kill()

        for wall in walls:
            if projectile.rect.colliderect(wall.rect):
                projectile.kill()

def le_attack(player, enemy_group, powerups, powerup_timers , dt):
    now = pygame.time.get_ticks()
    for enemy in enemy_group:
        if enemy.can_attack_primary and enemy.rect.colliderect(player.rect):
            player.health -= enemy.attack
            enemy.can_attack_primary = False
            enemy.last_attack_primary = now

            if type(enemy) == Australian:
                powerups["aussie"] = 0
                powerup_timers["aussie"] = now + 500
            
            if type(enemy) == Bomber:
                enemy.plode = True
                enemy.explode(dt)
                print('GAY')
                