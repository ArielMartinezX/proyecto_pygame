import pygame
from auxiliar.utils import SurfaceManager as sf

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        # self.image = pygame.Surface((30, 10))
        # self.image.fill((255, 0, 0))
        # self.image = pygame.image.load('assets/graphics/fire_shoot.png')
        self.image_r = pygame.image.load(r'assets\graphics\fire_shoot.png')
        self.image_l = pygame.transform.rotate(self.image_r,180)
        self.image = self.image_r
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.__direction = direction
    
    def update(self):
        if self.__direction:
            self.image = self.image_r
            self.rect.x += 10
        else:
            self.image = self.image_l
            self.rect.x -= 10
        
        if self.rect.x <= 10 or self.rect.x >= 790:
            self.kill()