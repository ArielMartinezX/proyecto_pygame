import pygame,sys
from auxiliar.utils import SurfaceManager as sf

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_w,constraint_h, walk_speed,run_speed, jump_power, gravity, aspect_ratio, jump_limit):
        super().__init__()
        
        