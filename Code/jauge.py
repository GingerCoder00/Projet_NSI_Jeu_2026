import pygame
from pygame.locals import QUIT
import os
from ui_tools import *

pygame.init()

class Jauge:
    def __init__(self, screen, fichier:str, nom_data:str, dimension:tuple, ampli_inflate:int, volume_son:float, frame:int, compl_zero:str = "", hover_on:bool = True, hover_info = True, nbr_frames = 7):
        self.screen = screen
        BASE_DIR = os.path.dirname(__file__)
        self.hover_info = hover_info
        self.x, self.y, self.L, self.l = dimension
        self.true_x = self.x
        self.true_y = self.y
        self.true_L = self.L
        self.true_l = self.l
        self.frame = frame
        self.nom_data = nom_data
        self.nbr_frames = nbr_frames
        self.compl_zero = compl_zero
        self.ampli_inf = ampli_inflate
        self.hover_on = hover_on

        self.flag_inflate = False

        self.show_info = False

        # Paramètre interaction souris
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.flag_click = False

        self.base_path = fichier
        self.IMG_PATH = os.path.join(f"{self.base_path}{self.compl_zero}{self.frame}.png")
        self.img_base = pygame.image.load(self.IMG_PATH).convert_alpha()
        self.rect = pygame.Rect(self.true_x, self.true_y, self.true_L, self.true_l)

        Longueur, largeur = self.screen.get_size()
        Longueur, largeur = self.screen.get_size()
        self.info = UI_screen(
            self.screen,
            (255,255,255),
            (0,0,0),
            (self.mouse_x, self.mouse_y, Longueur * 0.12, largeur * 0.25),
            4, 18
        )

        # Position initiale du texte (peut être proche de la souris ou dans un coin)
        self.texte_info = Texte(
            self.screen,
            (self.mouse_x + 10, self.mouse_y + 10),
            int(Longueur * 0.07 * 0.3),  # taille police
            (0,0,0),
            f"{self.nom_data}"
        )


        # Paramètre bruitage
        self.volume = volume_son
        SOUND_PATH = os.path.join(BASE_DIR, "sound", "click")
        self.hover_sound = pygame.mixer.Sound(f"{SOUND_PATH}.wav")
        self.flag_hover_sound = False


    def create(self):
        self.img = pygame.transform.scale(self.img_base, (int(self.true_L), int(self.true_l)))
        self.rect = pygame.Rect(self.true_x, self.true_y, self.true_L, self.true_l)
        self.screen.blit(self.img, (self.true_x, self.true_y))

    def set_frame(self, new_frame):
        new_frame = max(0, min(self.nbr_frames - 1, new_frame))
        if new_frame != self.frame:
            self.frame = new_frame
            self.IMG_PATH = os.path.join(f"{self.base_path}{self.compl_zero}{self.frame}.png")
            self.img_base = pygame.image.load(self.IMG_PATH).convert_alpha()

    def mouse_hover(self):
        if self.rect.collidepoint((self.mouse_x, self.mouse_y)):
            self.show_info = True
            if not self.flag_inflate:
                self.true_L += self.ampli_inf
                self.true_l += self.ampli_inf
                self.true_x -= self.ampli_inf // 2
                self.true_y -= self.ampli_inf // 2
                self.flag_inflate = True

            if not self.flag_hover_sound:
                self.hover_sound.play()
                self.flag_hover_sound = True

            if self.hover_info:
                self.info.x = min(self.mouse_x, self.screen.get_width() - self.info.L)
                self.info.y = min(self.mouse_y, self.screen.get_height() - self.info.l)
                self.texte_info.x = self.info.x + 10
                self.texte_info.y = self.info.y + 10

        else:
            self.show_info = False
            self.flag_hover_sound = False
            if self.flag_inflate:
                self.true_L -= self.ampli_inf
                self.true_l -= self.ampli_inf
                self.true_x += self.ampli_inf // 2
                self.true_y += self.ampli_inf // 2
                self.flag_inflate = False



    def update(self):
        self.hover_sound.set_volume(self.volume)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.create()
        if self.hover_on:
            self.mouse_hover()