import pygame
import math
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

class UI_Bouton:
    '''Classe qui gère les boutons'''
    def __init__(self, screen, color:tuple, color_contour:tuple, taille_font:int, taille_rect:tuple, text:str, taille_contour = 0, border_radius = 0, ampli_inflate = 0, volume_son = 0):

        # Variable Affichage
        self.screen = screen
        BASE_DIR = os.path.dirname(__file__)
        self.normal_color = color
        self.reverse_color = tuple(255 - elt for elt in color)
        self.color = self.normal_color
        self.bouton = pygame.Rect(taille_rect)
        self.t_cont = taille_contour
        self.color_contour = color_contour
        self.contour = pygame.Rect(taille_rect[0] - taille_contour, taille_rect[1] - taille_contour, taille_rect[2] + taille_contour * 2, taille_rect[3] + taille_contour * 2)
        self.text = text
        FONT_PATH = os.path.join(BASE_DIR, "font", "font_retro.ttf")
        self.font = pygame.font.Font(FONT_PATH, taille_font)
        self.bord_rad = border_radius
        self.ampli_inf = ampli_inflate
        self.flag_inflate = False
        self.tick = pygame.time.get_ticks()

        # Paramètre bruitage
        self.volume = volume_son
        SOUND_PATH = os.path.join(BASE_DIR, "sound", "click")
        self.hover_sound = pygame.mixer.Sound(f"{SOUND_PATH}.wav")
        self.click_sound = pygame.mixer.Sound(f"{SOUND_PATH}2.wav")
        
        self.flag_hover_sound = False

        # Paramètre interaction souris
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.flag_click = False


    def create(self):
        txt = self.font.render(self.text, True, (0,0,0))
        txt_rect = txt.get_rect(center=self.bouton.center)
        pygame.draw.rect(self.screen, self.color, self.bouton)
        pygame.draw.rect(self.screen, self.color_contour, self.contour, self.t_cont, self.bord_rad)
        self.screen.blit(txt, txt_rect)

    def mouse_hover(self):
        if self.contour.collidepoint((self.mouse_x, self.mouse_y)):
            if not self.flag_inflate:
                self.bouton.inflate_ip(self.ampli_inf,self.ampli_inf)
                self.contour.inflate_ip(self.ampli_inf,self.ampli_inf)
                self.flag_inflate = True
            self.color = self.reverse_color
            if not self.flag_hover_sound:
                self.hover_sound.play()
                self.flag_hover_sound = True
        else:
            self.color = self.normal_color
            self.flag_hover_sound = False
            if self.flag_inflate:
                self.bouton.inflate_ip(-self.ampli_inf,-self.ampli_inf)
                self.contour.inflate_ip(-self.ampli_inf,-self.ampli_inf)
                self.flag_inflate = False

    def mouse_is_click(self):
        if self.contour.collidepoint((self.mouse_x, self.mouse_y)):
            if self.left_click and not self.flag_click:
                self.flag_click = True
                self.click_sound.play()
                return True
        if not self.left_click:
            self.flag_click = False
        return False

    def update(self):
        self.hover_sound.set_volume(self.volume)
        self.click_sound.set_volume(self.volume)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.create()
        self.mouse_hover()

class UI_screen:
    '''Classe qui gère les interfaces UI'''
    def __init__(self, screen, color:tuple, color_contour:tuple, taille_rect:tuple,taille_contour:int = 0, border_radius:int = 0, pulse = True):

        self.start_time = pygame.time.get_ticks()  # temps de départ
        self.clock = pygame.time.Clock()

        # Variable Affichage
        self.screen = screen
        self.longueur, self.largeur = screen.get_size()
        self.pulse = pulse
        self.color = color
        self.color_contour = color_contour
        self.x, self.y, self.L, self.l = taille_rect
        self.true_L = self.L
        self.true_l = self.l
        self.centre_rect = (self.x + self.L // 2, self.y + self.l // 2)
        self.t_cont = taille_contour
        self.bord_rad = border_radius


        # Paramètre interaction souris
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.flag_click = False


    def create(self):
        # On garde le centre dynamique
        centre_x = self.x + self.L // 2
        centre_y = self.y + self.l // 2

        self.rect = pygame.Rect(0, 0, self.true_L, self.true_l)
        self.rect.center = (centre_x, centre_y)

        self.contour = pygame.Rect(
            0, 0,
            self.true_L + self.t_cont * 2,
            self.true_l + self.t_cont * 2
        )
        self.contour.center = (centre_x, centre_y)

        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=self.bord_rad - 6)
        pygame.draw.rect(self.screen, self.color_contour, self.contour, self.t_cont, border_radius=self.bord_rad)



    def animation_pulse(self):
        self.temps = pygame.time.get_ticks() / 1000
        self.pulsation_sin = 1 + 0.02 * math.sin(self.temps * 2)
        self.true_L = int(self.L * self.pulsation_sin)
        self.true_l = int(self.l * self.pulsation_sin)

    def update(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.create()
        if self.pulse:
            self.animation_pulse()

class UI_PNG:
    def __init__(self, screen, fichier:str, dimension:tuple, ampli_inflate:int, volume_son:float, hover_on:bool = True):
        self.screen = screen
        BASE_DIR = os.path.dirname(__file__)
        self.x, self.y, self.L, self.l = dimension
        self.true_x = self.x
        self.true_y = self.y
        self.true_L = self.L
        self.true_l = self.l
        self.ampli_inf = ampli_inflate
        self.hover_on = hover_on
        self.flag_inflate = False
        self.IMG_PATH = os.path.join(BASE_DIR, "sprite", fichier)
        self.img_base = pygame.image.load(self.IMG_PATH).convert_alpha()
        self.rect = pygame.Rect(self.true_x, self.true_y, self.true_L, self.true_l)

        # Paramètre bruitage
        self.volume = volume_son
        SOUND_PATH = os.path.join(BASE_DIR, "sound", "click")
        self.hover_sound = pygame.mixer.Sound(f"{SOUND_PATH}.wav")
        self.click_sound = pygame.mixer.Sound(f"{SOUND_PATH}2.wav")
        
        self.flag_hover_sound = False

        # Paramètre interaction souris
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.flag_click = False

    def create(self):
        self.img = pygame.transform.scale(self.img_base, (int(self.true_L), int(self.true_l)))
        self.rect = pygame.Rect(self.true_x, self.true_y, self.true_L, self.true_l)
        self.screen.blit(self.img, (self.true_x, self.true_y))

    def mouse_hover(self):
        if self.rect.collidepoint((self.mouse_x, self.mouse_y)):
            if not self.flag_inflate:
                self.true_L += self.ampli_inf
                self.true_l += self.ampli_inf
                self.true_x -= self.ampli_inf // 2
                self.true_y -= self.ampli_inf // 2
                self.flag_inflate = True
            if not self.flag_hover_sound:
                self.hover_sound.play()
                self.flag_hover_sound = True
        else:
            self.flag_hover_sound = False
            if self.flag_inflate:
                self.true_L -= self.ampli_inf
                self.true_l -= self.ampli_inf
                self.true_x += self.ampli_inf // 2
                self.true_y += self.ampli_inf // 2
                self.flag_inflate = False

    def mouse_is_click(self):
        if self.rect.collidepoint((self.mouse_x, self.mouse_y)):
            if self.left_click and not self.flag_click:
                self.flag_click = True
                self.click_sound.play()
                return True
        if not self.left_click:
            self.flag_click = False
        return False

    def update(self):
        self.hover_sound.set_volume(self.volume)
        self.click_sound.set_volume(self.volume * 0.5)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.create()
        if self.hover_on:
            self.mouse_hover()  

class InputText:
    def __init__(self, screen, size, taille_font = 60, text=""):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(size[0], size[1], size[2], size[3])
        self.font = pygame.font.Font(None, taille_font)
        self.text = text
        self.last_message = ""
        self.txt_surface = self.font.render(text, True, (255,255,255))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                print("Texte saisi :", self.text)
                self.last_message = self.text
                self.text = ""
            elif len(self.text) < 24:
                self.text += event.unicode

            self.txt_surface = self.font.render(self.text, True, (24, 255, 3))

    def animation(self):
        self.var = int(180 + 60 * math.sin(self.time * 3))

    def create(self):
        # Dessin du texte
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 20))
        # Dessin du rectangle
        pygame.draw.rect(self.screen, (self.var, self.var, 255), self.rect, 3, 10)

    def get_last_message(self):
        last = self.last_message
        self.last_message = ""
        return last

    def update(self):
        self.clock.tick(60)
        self.time = pygame.time.get_ticks() / 1000
        self.animation()
        self.create()
        for event in pygame.event.get():
            self.handle_event(event)

class Texte:
    def __init__(self, screen, position_texte:tuple, size_texte:int, color:tuple, text:str, sin_effect:bool = False, font_type:str = "font/sans_sherif.otf"):
        self.screen = screen
        BASE_DIR = os.path.dirname(__file__)
        self.x, self.y = position_texte
        self.font_size = size_texte
        self.text = text
        self.color = color
        self.font_type = font_type
        self.clock = pygame.time.Clock()
        FONT_PATH = os.path.join(BASE_DIR, font_type)
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.sin_effect = sin_effect

    def create(self):
        txt = self.font.render(self.text, True, self.color)
        self.screen.blit(txt, (self.x, self.y))

    def animation(self):
        self.var = int(180 + 60 * math.sin(self.time * 3))
        self.color[0] = self.var
        self.color[1] = self.var

    def update(self):
        self.clock.tick(60)
        self.time = pygame.time.get_ticks() / 1000
        self.create()
        if self.sin_effect:
            self.animation()