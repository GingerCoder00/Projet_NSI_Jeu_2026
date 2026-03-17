# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

from resp_tools import *
import os
from PIL import Image
from ui_tools import UI_PNG
from random import randint
from dico_info_game import *

class Grille:
    '''Classe qui gère la création et la gestion de la grille du jeu'''

    def __init__(self, screen, nbr_lignes:int, nbr_colonnes:int, taille_marge:int, ratio_grille:float, dico_interact:dict):

        # Surface principale d'affichage
        self.screen = screen

        # Récupération de la taille de l'écran
        self.Long, self.larg = screen.get_size()

        # Dictionnaire contenant les informations sur les cases
        self.dico_info = Dico_info_Game()

        # Dictionnaire contenant les éléments interactifs
        self.dico_interact = dico_interact

        # Nombre de lignes et colonnes de la grille
        self.lignes = nbr_lignes
        self.colonnes = nbr_colonnes

        # Taille de la marge entre les cases
        self.marge = taille_marge  

        # Dossier de base du projet
        self.BASE_DIR = os.path.dirname(__file__)

        # Outil de responsive pour adapter la grille à l'écran
        self.resp = Resp_tools(self.Long, self.larg)

        # Choix aléatoire de la map utilisée
        self.num_map = randint(0,5)

        # Rectangle de la zone où sera placée la grille
        self.rect_zone = ratio_grille

        # Coordonnées et dimensions de la zone de grille
        self.zone_x, self.zone_y, self.zone_L, self.zone_l = self.rect_zone

        # Calcul de la taille des cases
        self.case_Long = (self.zone_L - (self.colonnes + 1) * self.marge) / self.colonnes
        self.case_larg = (self.zone_l - (self.lignes + 1) * self.marge) / self.lignes

        # Création de la grille logique (terrain)
        self.grille = [["terre" for i in range(self.colonnes)] for j in range(self.lignes)]


    def color_pixel_map(self, fichier:str, x:int, y:int):
        '''
        Cette fonction lit la couleur d'un pixel
        dans l'image de la map
        '''

        # Chemin de l'image de la map
        IMG_PATH = os.path.join(self.BASE_DIR, fichier)

        # Ouverture de l'image
        img = Image.open(IMG_PATH).convert("RGBA")  # RGBA recommandé

        # Accès aux pixels de l'image
        pixels = img.load()

        # Lecture de la couleur du pixel
        r, g, b, a = pixels[x, y]

        # Retourne la couleur RGB
        return r, g, b


    def placement_grille(self, colonne:int, ligne:int):
        '''
        Calcule la position écran d'une case
        en fonction de sa position dans la grille
        '''

        # Calcul de la position X
        x = self.zone_x + self.marge + colonne * (self.case_Long + self.marge)

        # Calcul de la position Y
        y = self.zone_y + self.marge + ligne * (self.case_larg + self.marge)

        return x, y


    def crea_cases(self):
        '''
        Cette méthode crée toutes les cases de la grille
        et les ajoute au dictionnaire interactif
        '''

        # Index unique pour chaque case
        index = 0

        # Parcours des lignes
        for lignes in range(self.lignes):

            # Parcours des colonnes
            for colonnes in range(self.colonnes):

                # Calcul de la position écran
                x, y = self.placement_grille(colonnes, lignes)

                # Chemin de la map utilisée
                self.MAP_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_map", f"sprite_map_{self.num_map}.png")

                # Récupération de la couleur du pixel correspondant
                color = self.color_pixel_map(self.MAP_PATH, colonnes, lignes)

                # Choix aléatoire du sprite correspondant à cette couleur
                index_randint = randint(0, len(self.dico_info.type_cases[color]) - 1)

                # Création de la case graphique
                case = UI_PNG(self.screen, self.dico_info.type_cases[color][index_randint], (x, y, self.case_Long, self.case_larg), 5, 0)

                # Ajout de la case dans les dictionnaires interactifs
                self.dico_interact[0]["Case"][index] = case
                self.dico_interact[1]["Case"][index] = case

                # Sauvegarde de la position logique de la case
                case.ligne = lignes
                case.colonne = colonnes
                
                # Mise à jour de la grille logique
                self.grille[lignes][colonnes] = color

                # Incrément de l'index
                index += 1