import pygame

def collision_x(target1, target2):
    for item1 in target1:
        for item2 in target2:
            if item1 == item2:
                continue

            if item1.rect.colliderect(item2.rect):
                if item1.old_rect.x <= item2.old_rect.x and item1.rect.x >= item2.rect.x:
                    item1.rect.right = item1.old_rect.right
                elif item1.old_rect.x >= item2.old_rect.x and item1.rect.x <= item2.rect.x:
                    item1.rect.left = item1.old_rect.left
                item1.direction.x *= -1


def collision_y(target1, target2):
    for item1 in target1:
        for item2 in target2:
            if item1 == item2:
                continue

            if item1.rect.colliderect(item2.rect):
                if item1.old_rect.y <= item2.old_rect.y and item1.rect.y >= item2.rect.y:
                    item1.rect.bottom = item1.old_rect.bottom
                elif item1.old_rect.y >= item2.old_rect.y and item1.rect.y <= item2.rect.y:
                    item1.rect.top = item1.old_rect.top
                item1.direction.y *= -1

def collision_x_nonmoving(target1, target2):
    for item1 in target1:
        for item2 in target2:
            if item1.rect.colliderect(item2.rect):
                if item1.direction.x > 0:
                    item1.rect.right = item2.rect.left
                elif item1.direction.x < 0:
                    item1.rect.left = item2.rect.right


def collision_y_nonmoving(target1, target2):
    for item1 in target1:
        for item2 in target2:
            if item1.rect.colliderect(item2.rect):
                if item1.direction.y > 0:
                    item1.rect.bottom = item2.rect.top
                elif item1.direction.y < 0:
                    item1.rect.top = item2.rect.bottom


def collision_projectile(projectiles, enemies, props):
    for projectile in projectiles:
        for enemy in enemies:
            if projectile.rect.colliderect(enemy):
                enemy.health -= 100
                projectile.kill()

        for groups in props:
            for collidable in groups:
                if projectile.rect.colliderect(collidable):
                    projectile.kill()

