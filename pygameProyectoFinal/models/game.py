import pygame, sys
from models.stage import Stage
from auxiliar.constantes import * 


class Game:
    
    def __init__(self) -> None:
        pass
    
    def run_stage(stage_name:str):
        pygame.init()
        
        screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
        clock = pygame.time.Clock()
        title = pygame.display.set_caption("PROTOTIPO")
        game = Stage(screen, SCR_HEIGHT, SCR_WIDTH, stage_name)
        back = game._Stage__stage_image
        background = pygame.image.load(back)
        background = pygame.transform.scale(background, (SCR_WIDTH, SCR_HEIGHT))
        
        
        while True:

            screen.blit(background,(0,0))
            delta_ms = clock.tick(FPS)
            game.run(delta_ms)
            
            pygame.display.update()