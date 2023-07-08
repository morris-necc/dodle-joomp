import pygame
import os
import sys
from shapely.geometry import Polygon

ALPHA = (0, 255, 0)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
    
    def die(self):
        self.kill()
        return 1

def enemy(xloc, yloc, enem_list, type):
    if type == 1:
        enem_dirR = os.path.join(sys.path[0], "assets", "sprites", "cannon",  "2R.png")
        enem_dirL = os.path.join(sys.path[0], "assets", "sprites", "cannon", "2L.png")
    if xloc == 0:
        enem = Enemy(xloc, yloc, enem_dirL)
    elif xloc == 480-30:
        enem = Enemy(xloc, yloc, enem_dirR)
    enem_list.add(enem)
    return enem_list

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sys.path[0], "assets", "sprites", "cannon", "1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tx = self.image.get_width()
        self.ty = self.image.get_height()
        self.speed = 5
        self.direction = 1 if x == 0 else -1
        self.position = (self.rect.x + self.tx/2, self.rect.y + self.ty/2)
        self.polygon = Polygon([
            (self.rect.x, self.rect.y),
            (self.rect.x + self.tx, self.rect.y),
            (self.rect.x + self.tx, self.rect.y + self.ty),
            (self.rect.x, self.rect.y + self.ty)
        ])

    def update(self):
        self.position = (self.rect.x + self.tx/2, self.rect.y + self.ty/2)
        self.rect.x += self.speed * self.direction

        self.polygon = Polygon([
            (self.rect.x, self.rect.y),
            (self.rect.x + self.tx, self.rect.y),
            (self.rect.x + self.tx, self.rect.y + self.ty),
            (self.rect.x, self.rect.y + self.ty)
        ])
        if self.rect.x > 480 or self.rect.x < 0:
            self.kill()
            del self
    
    def die(self):
        self.kill()
        return 2