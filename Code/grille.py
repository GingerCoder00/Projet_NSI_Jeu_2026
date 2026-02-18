import pygame
from resp_tools import *
import os
from PIL import Image
from ui_tools import UI_PNG
from random import randint
from dico_info_game import *

class Grille:
    def __init__(self, screen, nbr_lignes:int, nbr_colonnes:int, taille_marge:int, ratio_grille:float, dico_interact:dict):

        self.screen = screen
        self.Long, self.larg = screen.get_size()
        self.dico_info = Dico_info_Game()
        self.dico_interact = dico_interact

        # Gestion du nombre de cases
        self.lignes = nbr_lignes
        self.colonnes = nbr_colonnes
        self.marge = taille_marge  # marge entre les cases

        self.BASE_DIR = os.path.dirname(__file__)

        self.resp = Resp_tools(self.Long, self.larg)
        self.num_map = randint(0,3)

        self.rect_zone = ratio_grille

        self.zone_x, self.zone_y, self.zone_L, self.zone_l = self.rect_zone
        self.case_Long = (self.zone_L - (self.colonnes + 1) * self.marge) / self.colonnes
        self.case_larg = (self.zone_l - (self.lignes + 1) * self.marge) / self.lignes

        self.grille = [["terre" for i in range(self.colonnes)] for j in range(self.lignes)]

    def color_pixel_map(self, fichier:str, x:int, y:int):
        IMG_PATH = os.path.join(self.BASE_DIR, fichier)
        img = Image.open(IMG_PATH).convert("RGBA")  # RGBA recommandé
        pixels = img.load()

        # Lire un pixel
        r, g, b, a = pixels[x, y]
        return r, g, b

    def placement_grille(self, ligne:int, colonne:int):
        x = self.zone_x + self.marge + ligne * (self.case_Long + self.marge)
        y = self.zone_y + self.marge +  colonne * (self.case_larg + self.marge)
        return x, y

    def crea_cases(self):
        # Création des cases
        index = 0
        for lignes in range(self.lignes):
            for colonnes in range(self.colonnes):
                x, y = self.placement_grille(colonnes, lignes)
                self.MAP_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_map", f"map_{self.num_map}.png")
                color = self.color_pixel_map(self.MAP_PATH, colonnes, lignes)
                self.dico_interact[0]["Case"][index] = UI_PNG(self.screen, self.dico_info.type_cases[color][randint(0,3)], (x, y, self.case_Long, self.case_larg), 5, 0.03)
                self.dico_interact[1]["Case"][index] = UI_PNG(self.screen, self.dico_info.type_cases[color][randint(0,3)], (x, y, self.case_Long, self.case_larg), 5, 0.03)
                self.grille[lignes][colonnes] = color
                index += 1