import pygame, random
from auxiliar.constantes import *
from models.player_1 import Player
from models.enemy import Enemy
from models.objetos import Objetos
from models.plataformas import Platform

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_h, limit_w, stage_name:str):
        self.__configs = open_configs().get(stage_name)
        self.__player_configs = self.__configs.get('player')
        self.__player_sprite = Player((limit_w / 2, limit_h),limit_w, 500,#limite pantalla
                                    self.__player_configs.get('walk_speed'),
                                    self.__player_configs.get('run_speed'),
                                    self.__player_configs.get('jump_power'),
                                    self.__player_configs.get('gravity'),
                                    self.__player_configs.get('aspect_ratio'),
                                    self.__player_configs.get('jump_limit'),
                                    self.__player_configs.get('frame_rate'),
                                    self.__player_configs.get('lifes'),
                                    self.__player_configs.get('fire_cooldown'),)
        #configuraciones de stage
        self.__stage_configs = self.__configs.get('stage')
        #configuraciones de enemigos
        self.__enemy_configs = self.__configs.get('enemy')
        
        #creo grupo jugador y enemigos
        self.player = pygame.sprite.GroupSingle(self.__player_sprite)
        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.create_enemies()
        #del json obtengo configuraciones del stage
        self.__stage_configs = self.__configs.get('stage')
        self.__stage_image = self.__stage_configs.get('stage_background')
        self.__stage_music = self.__stage_configs.get('stage_music')
        self.__stage_win = pygame.mixer.Sound(self.__stage_configs.get('stage_win'))
        # self.__max_enemies = self.__stage_configs.get('max_enemies_amount')
        # self.__coordenadas_enemigos = self.__stage_configs.get('coords_enemies')
        #limites del stage
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        #pantalla principal
        self.__main_screen = screen
        self.__tiempo_transcurrido = 0

        #game over
        self.game_over_sound = False
        #game win
        self.game_win_sound = False
        
        #plataformas
        self.__lista_plataformas = []
        self.crear_plataformas()
        
        #objetos
        self.create_objetcs()
    
    @property
    def stage_image(self):
        return self.__stage_image
    @property
    def stage_music(self):
        return self.__stage_music
    
    def crear_plataformas(self):
        self.__lista_plataformas.append(Platform(0,500,SCR_WIDTH,40))
        # self.__lista_plataformas.append(Platform(400,200,40,40))
        self.__lista_plataformas.append(Platform(280,400,40,40))
        self.__lista_plataformas.append(Platform(180,300,200,40))
        self.__lista_plataformas.append(Platform(380,400,40,40))
        self.__lista_plataformas.append(Platform(380,200,200,40))
        
    def plataformas(self):
        for platform in self.__lista_plataformas:
            platform.draw(self.__main_screen)
    def enemigos(self):
        for enemy in self.enemies:
            enemy.draw(self.__main_screen)
    
    def create_objetcs(self):
        # self.objects.add(Objetos(400+20,200, 2, 100))
        self.objects.add(Objetos(280+20,400, 2, 100))
        self.objects.add(Objetos(180+20,400, 2, 100))
        self.objects.add(Objetos(380+20,400, 2, 100))
        # print(f"len de objetos {len(self.objects)}")
    
    def create_enemies(self):
        for _ in range(self.__stage_configs.get('max_enemies_amount')):
            walk_speed = random.randint(self.__enemy_configs.get('enemy_min_speed'),
                                self.__enemy_configs.get('enemy_max_speed'))
            coord_x = random.randint(50,750)
            new_enemy = Enemy((coord_x,50), SCR_WIDTH,500, walk_speed,
                            self.__enemy_configs.get('gravity'),
                            self.__enemy_configs.get('aspect_ratio'),
                            self.__enemy_configs.get('shoot_percentage'),
                            self.__enemy_configs.get('frame_rate'))
            self.enemies.add(new_enemy)
    
    def objetos(self):
        for objeto in self.objects:
            objeto.draw(self.__main_screen)
    
    def shoot_collisions(self):
        for fireball in self.player.sprite.fireball_group:
            hits = pygame.sprite.spritecollide(fireball, self.enemies, True)
            if hits:
                self.player.sprite.hit.play()
                self.player.sprite.remove_fireball(fireball)  
            if not self.enemies and not self.game_win_sound:
                self.__stage_win.play()
                self.game_win_sound = True
                
        for enemy in self.enemies:
            for fireball in enemy.fireball_group:
                hits = pygame.sprite.spritecollide(fireball, self.player, False)
                if hits:
                    if self.player.sprite.lifes > 0:
                        self.player.sprite.hit.play()
                    self.player.sprite.restar_vida()
                    enemy.fireball_group.remove(fireball)
                    if self.player.sprite.lifes == 0 and not self.game_over_sound:
                        self.player.sprite.death.play() 
                        self.game_over_sound = True
                        
    
    def objects_collitions(self):
            pygame.sprite.spritecollide(self.player.sprite, self.objects, True)
            
    
    def run(self, delta_ms, lista_eventos):
        self.__tiempo_transcurrido += delta_ms
        if self.__tiempo_transcurrido >= 17:
            self.plataformas()
            self.enemigos()
            self.objetos()
            self.objects_collitions()
            self.objects.update(self.__main_screen, delta_ms)
            # self.objects.draw(self.__main_screen)
            self.enemies.update(self.__main_screen, delta_ms, self.__lista_plataformas)
            # self.enemies.draw(self.__main_screen)
            self.player.update(self.__main_screen, delta_ms, self.__lista_plataformas, lista_eventos)
            self.player.sprite.draw(self.__main_screen)
            self.shoot_collisions()
            # print(f'player_y {self.player.sprite.rect.y}')
        else:
            self.__tiempo_transcurrido = 0