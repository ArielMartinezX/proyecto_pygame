import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_w, walk_speed, gravity, aspect_ratio):
        super().__init__()
        self.image = pygame.image.load(r'assets\graphics\Jump(32x32).png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width() * aspect_ratio ,
                        self.image.get_height() * aspect_ratio))
        self.rect = self.image.get_rect(midbottom=pos)

        #hitbox
        self.__hitbox = pygame.Rect(self.rect.x , self.rect.y, self.rect.width, self.rect.height)

        #Atributos de movimiento
        self.__walk_speed = walk_speed
        self.__max_constraint_w = constraint_w
        self.__gravity = gravity
        
        #donde esta mirando
        self.__is_right = False

    def constrain(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.__is_right = True
        if self.rect.right >= self.__max_constraint_w:
            self.rect.right = self.__max_constraint_w
            self.__is_right = False
    
    def movement(self):
        if not self.__is_right:
            self.rect.x += -self.__walk_speed 
        else:
            self.rect.x += self.__walk_speed        
    
    def draw(self):
        pass
    
    def update(self, screen: pygame.surface.Surface):
        self.movement()
        self.constrain()