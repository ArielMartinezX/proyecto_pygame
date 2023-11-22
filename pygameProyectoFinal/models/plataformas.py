import pygame
from auxiliar.constantes import *
from auxiliar.utils import SurfaceManager as spriter

"""
debug (constante)



"""

class Platform:
    def __init__(self,x,y,w,h,type=0):
        self.image = pygame.image.load(r'assets\graphics\piso.png')
        # self.image = spriter.get_surface_from_spritesheet("alguna imagen",1,1)[type]
        self.image = pygame.transform.scale(self.image,(w,h))
        self.__rect = self.image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__ground_collition_rect = pygame.Rect(self.__rect.x , self.__rect.y, self.__rect.w, self.__rect.h-39)

    @property
    def ground_collition_rect(self):
        return self.__ground_collition_rect
    
    @property
    def rect(self):
        return self.__rect
    
    def draw(self, screen):
        # if DEBUG:
        #     # pygame.draw.rect(screen, ((255,0,0)), self.__rect)
        #     pygame.draw.rect(screen, ((0,255,0)), self.__ground_collition_rect)
        screen.blit(self.image, self.__rect)
        screen.blit(self.image, self.__ground_collition_rect)
        if DEBUG:
            # pygame.draw.rect(screen, ((255,0,0)), self.__rect)
            pygame.draw.rect(screen, ((255,255,255)), self.__ground_collition_rect)
        