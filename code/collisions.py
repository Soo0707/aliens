import pygame

def collision_x(target1, target2):
    for item1 in target1:
        for item2 in target2:
            if item1.rect.colliderect(item2.rect):
                if item1.direction.x > 0:
                    item1.rect.right = item2.rect.left
                elif item1.direction.x < 0:
                    item1.rect.left = item2.rect.right


def collision_y(target1, target2):
    for item1 in target1:
        for item2 in target2:
            if item1.rect.colliderect(item2.rect):
                if item1.direction.y > 0:
                    item1.rect.bottom = item2.rect.top
                elif item1.direction.y < 0:
                    item1.rect.top = item2.rect.bottom


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


