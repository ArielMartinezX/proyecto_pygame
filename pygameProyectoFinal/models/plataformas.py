import pygame
from auxiliar.constantes import *
from auxiliar.utils import SurfaceManager as spriter


class Platform:
    def __init__(self,x,y,w,h,type=0):
        self.image = spriter.get_surface_from_spritesheet("alguna imagen",8,8)[type]
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        