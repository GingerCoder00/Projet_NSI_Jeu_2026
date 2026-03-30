# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
import os
from ui_tools import *

pygame.init()

class Jauge:
    '''Classe qui gère les jauges du jeu (pollution, température, destruction, etc.)'''

    def __init__(self, screen, fichier:str, nom_data:str, data_file, dimension:tuple, ampli_inflate:int, volume_son:float, frame:int, compl_zero:str = "", hover_on:bool = True, hover_info = True, nbr_frames = 7):
        
        # Surface principale d'affichage
        self.screen = screen

        # Taille de l'écran
        self.Longueur, self.largeur = self.screen.get_size()

        # Dossier de base du projet
        BASE_DIR = os.path.dirname(__file__)

        # Active ou non l'affichage des infos au hover
        self.hover_info = hover_info

        # Dimensions de la jauge
        self.x, self.y, self.L, self.l = dimension

        # Dimensions réelles (modifiées au hover)
        self.true_x = self.x
        self.true_y = self.y
        self.true_L = self.L
        self.true_l = self.l

        # Frame actuelle de la jauge
        self.frame = frame

        # Nom de la donnée affichée
        self.nom_data = nom_data

        # Fonction retournant les données du jeu
        self.data = data_file

        # Valeur actuelle de la donnée
        self.taux = self.data()

        # Nombre total de frames de la jauge
        self.nbr_frames = nbr_frames

        # Complément de nom pour les fichiers sprite
        self.compl_zero = compl_zero

        # Agrandissement de la jauge au hover
        self.ampli_inf = ampli_inflate

        # Activation du hover
        self.hover_on = hover_on

        # Ratios pour placer le texte
        self.ratio_texte = {
            "Nom_Jauge" : (0.01, 0.03),
            "Taux_Jauge" : (0.01, 0.1),
        }

        # Indique si la jauge est actuellement agrandie
        self.flag_inflate = False

        # Indique si la fenêtre d'info doit être affichée
        self.show_info = False

        # Paramètres souris
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.left_click = pygame.mouse.get_pressed()[0]
        self.flag_click = False

        # Chemin de base des sprites
        self.base_path = fichier

        # Chargement de la première image
        self.IMG_PATH = os.path.join(f"{self.base_path}{self.compl_zero}{self.frame}.png")
        self.img_base = pygame.image.load(self.IMG_PATH).convert_alpha()

        # Rectangle de collision de la jauge
        self.rect = pygame.Rect(self.true_x, self.true_y, self.true_L, self.true_l)

        # Mise à jour taille écran
        self.Longueur, self.largeur = self.screen.get_size()

        # Création de la fenêtre d'information
        self.info = UI_screen(self.screen, (176, 255, 247), (0,0,0), (self.mouse_x - self.Longueur * 0.16, self.mouse_y - self.largeur * 0.17, self.Longueur * 0.16, self.largeur * 0.17), 7, 18)

        # Chemin de base
        self.BASE_DIR = os.path.dirname(__file__)

        # Chargement de la police
        self.FONT_PATH = os.path.join(self.BASE_DIR, "font", "font_retro2.ttf")

        # Texte affichant le nom de la jauge
        self.texte_info = Texte(self.screen, (self.mouse_x + self.Longueur * self.ratio_texte["Nom_Jauge"][0], self.mouse_y + self.largeur * self.ratio_texte["Nom_Jauge"][1]), int(self.Longueur * 0.07 * 0.3), (0,0,0), f"{self.nom_data.capitalize()}", font_type = self.FONT_PATH)

        # Texte affichant la valeur de la jauge
        self.texte_stats_info = Texte(self.screen, (self.mouse_x + self.Longueur * self.ratio_texte["Taux_Jauge"][0], self.mouse_y + self.largeur * self.ratio_texte["Taux_Jauge"][1]), int(self.largeur * 0.07 * 0.4), (0,0,0), f"{round(getattr(self.taux, self.nom_data), 1)}", font_type = self.FONT_PATH)

        # Paramètres du bruitage
        self.volume = volume_son
        SOUND_PATH = os.path.join(BASE_DIR, "sound", "click")
        self.hover_sound = pygame.mixer.Sound(f"{SOUND_PATH}.wav")
        self.flag_hover_sound = False


    def create(self):
        '''Affiche la jauge à l'écran'''

        # Redimensionnement de l'image
        self.img = pygame.transform.scale(self.img_base, (int(self.true_L), int(self.true_l)))

        # Mise à jour du rectangle
        self.rect = pygame.Rect(self.true_x, self.true_y, self.true_L, self.true_l)

        # Affichage de la jauge
        self.screen.blit(self.img, (self.true_x, self.true_y))


    def set_frame(self, new_frame):
        '''
        Change la frame de la jauge
        '''

        # Limite la frame dans l'intervalle autorisé
        new_frame = max(0, min(self.nbr_frames - 1, new_frame))

        # Si la frame change
        if new_frame != self.frame:

            self.frame = new_frame

            # Chargement du nouveau sprite
            self.IMG_PATH = os.path.join(f"{self.base_path}{self.compl_zero}{self.frame}.png")
            self.img_base = pygame.image.load(self.IMG_PATH).convert_alpha()


    def mouse_hover(self):
        '''
        Gère les interactions souris avec la jauge
        '''

        # Si la souris est sur la jauge
        if self.rect.collidepoint((self.mouse_x, self.mouse_y)):

            self.show_info = True

            # Agrandissement de la jauge
            if not self.flag_inflate:

                self.true_L += self.ampli_inf
                self.true_l += self.ampli_inf
                self.true_x -= self.ampli_inf // 2
                self.true_y -= self.ampli_inf // 2

                self.flag_inflate = True

            # Lecture du son de hover
            if not self.flag_hover_sound:

                self.hover_sound.play()
                self.flag_hover_sound = True

            # Mise à jour position de la fenêtre info
            if self.hover_info:

                self.info.x = min(self.mouse_x - self.Longueur * 0.16, self.screen.get_width() - self.info.L)
                self.info.y = min(self.mouse_y - self.largeur * 0.17, self.screen.get_height() - self.info.l)

                self.texte_info.x = self.info.x + self.Longueur * self.ratio_texte["Nom_Jauge"][0]
                self.texte_info.y = self.info.y + self.largeur * self.ratio_texte["Nom_Jauge"][1]

        else:

            # Désactivation info
            self.show_info = False
            self.flag_hover_sound = False

            # Retour taille normale
            if self.flag_inflate:

                self.true_L -= self.ampli_inf
                self.true_l -= self.ampli_inf
                self.true_x += self.ampli_inf // 2
                self.true_y += self.ampli_inf // 2

                self.flag_inflate = False


    def update(self):
        '''
        Met à jour la jauge à chaque frame
        '''

        # Mise à jour du volume
        self.hover_sound.set_volume(self.volume)

        # Mise à jour position souris
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Vérifie clic souris
        self.left_click = pygame.mouse.get_pressed()[0]

        # Création / affichage jauge
        self.create()

        # Gestion hover
        if self.hover_on:
            self.mouse_hover()

        # Mise à jour des données
        self.taux = self.data()

        # Mise à jour du texte de la valeur
        self.texte_stats_info = Texte(self.screen, (self.info.x + self.Longueur * self.ratio_texte["Taux_Jauge"][0], self.info.y + self.largeur * self.ratio_texte["Taux_Jauge"][1]), int(self.Longueur * 0.07 * 0.4), (0,0,0), f"{round(getattr(self.taux, self.nom_data), 1)}", font_type = self.FONT_PATH)