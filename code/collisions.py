import pygame

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
