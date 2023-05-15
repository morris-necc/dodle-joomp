import pygame
import os
import sys

class Level(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, img_w, img_h, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(0,255)
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
    
    def ground(x,y,w,h):
        ground_list = pygame.sprite.Group()
        ground_dir = os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Palm Tree Island", "Sprites", "Terrain", "Terrain (32x32).png")
        ground = Level(x,y,w,h,ground_dir)
        ground_list.add(ground)
        return ground_list
    
    def platform(x,y,w,h):
        plat_list = pygame.sprite.Group()
        plat_dir = os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Palm Tree Island", "Sprites", "Terrain", "Terrain (32x32).png")
        plat = Level(x,y,w,h,plat_dir)
        plat_list.add(plat)           
        return plat_list