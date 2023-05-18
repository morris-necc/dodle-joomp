import pygame
import os
import sys
import random
ALPHA = (0, 255, 0)
class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
        self.tx = self.ty = 32

    def die(self):
        self.kill()
        del self
        return 0

def platform(x, y, plat_list, type, length):
    if type == 1:
        plat_dir = os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Palm Tree Island", "Sprites", "Terrain", "Terrain (32x32).png")
    for i in range(length):
        plat = Platform(x+i*32, y, plat_dir)
        plat_list.add(plat)
    return plat_list
