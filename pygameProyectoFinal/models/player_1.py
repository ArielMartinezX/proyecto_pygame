import pygame
from auxiliar.utils import SurfaceManager as sf
from models.fireball import Fireball
from auxiliar.constantes import *

# class Player(pygame.sprite.Sprite):
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_w,constraint_h, walk_speed,run_speed, jump_power, gravity, aspect_ratio, jump_limit, frame_rate, lifes, fire_cooldown):
        super().__init__()

        self.__iddle_r = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Idle_4.png', 4, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Idle_4.png', 4, 1, flip=True)
        self.__iddle_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__iddle_r]
        self.__iddle_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__iddle_l]
        self.__walk_r = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Walk_6.png',6,1)
        self.__walk_l = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Walk_6.png',6,1,flip=True)
        self.__walk_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__walk_r]
        self.__walk_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__walk_l]
        self.__jump_r = sf.get_surface_from_spritesheet(r'assets/graphics/Owlet_Monster/Owlet_Monster_Jump_8.png', 8,1)
        self.__jump_l = sf.get_surface_from_spritesheet(r'assets/graphics/Owlet_Monster/Owlet_Monster_Jump_8.png', 8,1,flip=True)
        self.__jump_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__jump_r]
        self.__jump_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__jump_l]
        self.__attack_r = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Attack2_6.png', 6,1)
        self.__attack_l = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Attack2_6.png', 6,1,flip=True)
        self.__attack_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__attack_r]
        self.__attack_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__attack_l]
        self.__death_r = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Death_8.png', 8,1)
        self.__death_l = sf.get_surface_from_spritesheet(r'assets\graphics\Owlet_Monster\Owlet_Monster_Death_8.png', 8,1, flip=True)
        self.__death_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__death_r]
        self.__death_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__death_l]
        
        
        self.__frame_rate = frame_rate
        self.__frame_rate_stay = 200
        self.__frame_rate_walk = 200
        self.__frame_rate_run = 50
        self.__frame_rate_shoot = 500
        self.__frame_rate_death = 500
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect(midbottom=pos)
        self.__lifes = lifes
        
        #animacion muerte
        self.__death_animation_times = False
        self.__death_animation_counter = 0
        #sonido muerte
        self.__game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')
        self.__game_over = False
        #donde esta mirando
        self.__is_looking_right = True
        
        #disparos
        self.__fireball_group = pygame.sprite.Group()
        self.__shoot_rate = 300
        self.__fire_cooldown = fire_cooldown
        self.__fire_ready = True
        self.__shoot_time = 0
        self.__shoot_sound = pygame.mixer.Sound('assets/sounds/fire_shoot.mp3')
        self.__damage_sound = pygame.mixer.Sound('assets/sounds/hit_sound.wav')
        # #HITBOX
        self.__ground_collition_rect = pygame.Rect(self.__rect.x + self.__rect.w//4 +6, (self.__rect.y + self.__rect.height), self.__rect.w//2 -6, 6)
        self.__collition_rect = pygame.Rect(self.__rect.x + self.__rect.w//4 +6, (self.__rect.y + self.__rect.height), self.__rect.w//2 -6, 50)
        
        #Atributos de movimiento
        self.__walk_speed = walk_speed
        self.__run_speed = run_speed
        self.__max_constraint_w = constraint_w
        self.__max_constraint_h = constraint_h
        
        #salto
        self.__jump_power = jump_power
        self.__gravity = gravity
        self.__salto = jump_power
        self.__jump_sound = pygame.mixer.Sound('assets/sounds/jump_sound.mp3')
        self.__jump_velocity = jump_power
        #plataformas
        self.__retorno = False
        
        #test salto
        self.__is_jumping = False
        
        #puntaje
        self.__puntaje = 0
    #propiedad del grupo disparo
    @property   
    def fireball_group(self):        
        return self.__fireball_group
    @property
    def rect(self):
        return self.__collition_rect
    @property
    def lifes(self):
        return self.__lifes
    @property
    def rect_ground(self):
        return self.__ground_collition_rect
    @property
    def hit(self):
        return self.__damage_sound
    @property
    def death(self):
        return self.__game_over_sound
    
    @property
    def score(self):
        return self.__puntaje
    @score.setter
    def new_score(self, value):
        self.__puntaje = value
    
    def restar_vida(self):
        if self.__lifes > 0:
            self.__lifes -= 1
        else:
            self.__lifes = 0

    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__rect.x += move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    # def __set_y_animations_preset(self,move_y,move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
    #     self.__rect.y += self.saltar()
    #     self.__rect.x += move_x
    #     self.__rect.x += self.__run_speed if self.__is_looking_right else -self.__run_speed
    #     self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
    #     self.__initial_frame = 0
    #     self.__is_jumping = True 

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms   
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0

    
    def on_platform(self, lista_plataformas):
        self.__retorno = False
        if self.__ground_collition_rect.y >= 500: # aplica gravedad. 
            self.__retorno = True
            return self.__retorno
        else:
            for plataform in lista_plataformas:
                if self.__ground_collition_rect.colliderect(plataform.ground_collition_rect):
                    self.__retorno = True
                    break
        return self.__retorno
    
    def get_inputs(self, lista_eventos, lista_plataformas):
        
        if self.__lifes > 0:    
            
            for event in lista_eventos:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.__is_jumping:
                        print("estoyt en el keydown")
                        self.__is_jumping = True
                        self.__jump_sound.play()
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.__is_right = False
                self.walk(self.__is_right)
            if keys[pygame.K_d]:
                self.__is_right = True
                self.walk(self.__is_right)
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.stay()
            if keys[pygame.K_k] and self.__fire_ready:
                self.shoot_fireball()
                self.__shoot_sound.play()
                self.__fire_ready = False
                self.__shoot_time = pygame.time.get_ticks()

        else:
            if not self.__death_animation_times: 
                self.is_dead()
                self.__death_animation_times = True


            else:
                if self.__death_animation_times and self.__initial_frame == 7:
                    self.__actual_animation = [self.__death_r[3]] if self.__is_looking_right else [self.__death_l[3]]
                    self.__initial_frame = 0    

    def is_alive(self):
        if self.__lifes > 0:
            return True
        return False

    def check_traps(self, trampas):
        if trampas:
            if self.__is_looking_right:
                self.__rect.x -= 25
            else:
                self.__rect.x += 25
            self.__rect.y -= 12
                
            self.__damage_sound.play()
            self.restar_vida()
            
            if self.__lifes == 0 and not self.__game_over:
                self.__game_over_sound.play()
                self.__game_over = True
    
    def check_body_to_body_collitions(self,cuerpo_a_cuerpo):
        if cuerpo_a_cuerpo and self.__lifes > 0:
            self.restar_vida()
            self.__damage_sound.play()
            if self.__is_looking_right:
                self.__rect.x -= 70
            else:
                self.__rect.x += 70
            self.__rect.y -= 5
    def saltar(self, lista_plataformas):
        
        if self.__is_jumping:
            if self.__salto >= -self.__jump_power:
                self.__rect.y -= self.__salto + 10
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.__rect.x -= self.__run_speed
                if keys[pygame.K_d]:
                    self.__rect.x += self.__run_speed
                self.__salto -= 0.5
            elif self.on_platform(lista_plataformas):
                self.__is_jumping = False
                self.__salto = self.__jump_power

    def is_dead(self):
        self.__frame_rate = self.__frame_rate_death
        self.__actual_animation = self.__death_r if self.__is_looking_right else self.__death_l

    def stay(self):
        self.__frame_rate = self.__frame_rate_stay
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
    
    def walk(self, look_right=True):
        self.__frame_rate = self.__frame_rate_walk
        if look_right:
            self.__set_x_animations_preset(self.__walk_speed, self.__walk_r, look_r=look_right)

        else:
            self.__set_x_animations_preset(-self.__walk_speed, self.__walk_l, look_r=look_right)

    def run(self, look_right=True):
        self.__frame_rate = self.__frame_rate_run
        if look_right:
            self.__rect.x += self.__run_speed

        else:
            self.__rect.x += -self.__run_speed

    def constraint(self):
        if self.__rect.left  <= 0 -16:
            self.__rect.left = 0 -16
        if self.__rect.right >= self.__max_constraint_w+16:
            self.__rect.right = self.__max_constraint_w+16

        if self.__rect.top <= 0:
            self.__rect.top = 0
        if self.__rect.bottom >= self.__max_constraint_h+1:
            self.__rect.bottom = self.__max_constraint_h+1
    
    def gravedad(self, lista_plataformas):
        if not self.on_platform(lista_plataformas):
            self.__rect.y += self.__gravity

    def create_fireball(self, direction):
        if direction:
            return Fireball(self.__rect.right, self.__rect.y+42, self.__is_looking_right)
        else:
            return Fireball(self.__rect.left, self.__rect.y+42, self.__is_looking_right)
            
    def shoot_fireball(self):
        self.__frame_rate = self.__frame_rate_shoot
        self.__fireball_group.add(self.create_fireball(self.__is_looking_right))
        self.__actual_animation = [self.__attack_r[2]] if self.__is_looking_right else [self.__attack_l[2]]
        self.__initial_frame = 0

    def remove_fireball(self, fireball):
        self.__fireball_group.remove(fireball)
    
    def fire_cooldown(self):
        if not self.__fire_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.__shoot_time >= self.__fire_cooldown:
                self.__fire_ready = True
                
    def draw(self, screen):
            
            # pygame.draw.rect(screen,((0,0,255)),self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)
        if DEBUG:
            self.__ground_collition_rect.midbottom = self.__rect.midbottom
            self.__collition_rect.midbottom = self.__rect.midbottom
            # pygame.draw.rect(screen,((0,0,255)),self.__rect)
            # pygame.draw.rect(screen,((255,255,255)),self.__ground_collition_rect)
            pygame.draw.rect(screen,((0,0,255)),self.__collition_rect)
        self.__ground_collition_rect.midbottom = self.__rect.midbottom
        self.__collition_rect.midbottom = self.__rect.midbottom

        # screen.blit(self.image, self.__rect)

    def update(self, screen: pygame.surface.Surface, delta_ms, lista_plataformas, lista_eventos, trampas, cuerpo_a_cuerpo):
        self.get_inputs(lista_eventos, lista_plataformas)
        self.constraint()
        self.do_animation(delta_ms)
        self.gravedad(lista_plataformas)
        self.fire_cooldown()
        self.saltar(lista_plataformas)
        self.check_traps(trampas)
        self.check_body_to_body_collitions(cuerpo_a_cuerpo)
        print(f"lifes {self.__lifes}")
        self.__fireball_group.draw(screen)
        self.__fireball_group.update()