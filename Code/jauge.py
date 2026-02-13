import pygame
from pygame.locals import QUIT
import os

pygame.init()

class Jauge:
    def __init__(self, screen, fichier:str, dimension:tuple, ampli_inflate:int, volume_son:float, niv, hover_on:bool = True):
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

    def update(self):
        self.hover_sound.set_volume(self.volume)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        if self.hover_on:
            self.mouse_hover()
        self.create()