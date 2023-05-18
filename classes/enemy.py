import pygame
import os
import sys
import random
ALPHA = (0, 255, 0)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

def enemy(eloc, enem_list, type):
    if type == 1:
        enem_dirR = os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Shooter Traps", "Sprites", "Cannon", "Cannon Destroyed", "2R.png")
        enem_dirL = os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Shooter Traps", "Sprites", "Cannon", "Cannon Destroyed", "2L.png")
    for enemy in eloc:
        if enemy[0] == 0:
            enem = Enemy((enemy[0]),enemy[1], enem_dirL)
        elif enemy[0] == 480-30:
            enem = Enemy((enemy[0]),enemy[1], enem_dirR)
        enem_list.add(enem)
    return enem_list

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Shooter Traps", "Sprites", "Cannon", "Cannon Ball Idle", "1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = 1 if x == 0 else -1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x > 480 or self.rect.x < 0:
            self.kill()