import pygame
import os
import sys
from shapely.geometry import Polygon

ALPHA = (0, 255, 0)
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = pygame.Rect((xloc, yloc), (32, 32))
        self.rect.y = yloc
        self.rect.x = xloc
        self.tx = self.ty = 32
        self.position = (self.rect.x + self.tx/2, self.rect.y + self.ty/2)
        self.polygon = Polygon([
            (self.rect.x, self.rect.y),
            (self.rect.x + self.tx, self.rect.y),
            (self.rect.x + self.tx, self.rect.y + self.ty),
            (self.rect.x, self.rect.y + self.ty)])
        
    def update(self):
        self.position = (self.rect.x + self.tx/2, self.rect.y + self.ty/2)
        self.polygon = Polygon([
            (self.rect.x, self.rect.y),
            (self.rect.x + self.tx, self.rect.y),
            (self.rect.x + self.tx, self.rect.y + self.ty),
            (self.rect.x, self.rect.y + self.ty)
        ])

    def die(self):
        self.kill()
        del self
        return 0

def platform(x, y, plat_list, type, length):
    if type == 1:
        plat_dir = os.path.join(sys.path[0], "assets", "sprites", "platform", "Terrain (32x32).png")
    for i in range(length):
        plat = Platform(x+i*32, y, plat_dir)
        plat_list.add(plat)
    return plat_list