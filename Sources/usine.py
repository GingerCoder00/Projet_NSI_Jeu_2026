# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from ui_tools import UI_PNG  # Pour gérer les images PNG interactives
from data import *
from grille import *  # Gestion de la grille de placement
from dico_info_game import *  # Informations sur les types de cases
from condamne import *  # Gestion des cases "condamnées" autour des bâtiments
from animation import *  # Gestion des animations


class Usine:
    '''Classe représentant les usines du jeu'''

    def __init__(self, screen, grille, data, dico_UI_anim, plan_ref):
        self.screen = screen  # écran Pygame
        self.grille = grille  # instance de la grille de placement
        self.data = data  # données du jeu
        self.dico_UI_anim = dico_UI_anim  # dictionnaire des animations UI
        self.plan_ref = plan_ref  # fonction qui renvoie le plan actuel du jeu

        # Gestion des animations pour les usines
        self.animation = Animation(screen, plan_ref, dico_UI_anim, grille)
        self.BASE_DIR = os.path.dirname(__file__)  # dossier courant

        # Gestion des cases "condamnées" autour des usines
        self.condamne = Condamne(screen, grille, data, dico_UI_anim, plan_ref)

        # Dictionnaire info du jeu
        self.dico_info = Dico_info_Game()

        # Chargement des frames des usines (pour animation)
        self.usine_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Usine"]]

        # Compteur du nombre d'usines ajoutées
        self.nbr_usines_spawn = 0

        # Sons possibles lors de l'apparition d'une usine
        self.SOUND_USINE_PATH = [os.path.join(self.BASE_DIR, "sound", f"chute{i}") for i in range(1,4)]


    def ajout_usine(self, ligne, colonne):
        '''Ajoute une usine à la grille et initialise son animation et les cases autour'''

        # Calcul de la position sur l'écran à partir de la grille
        x, y = self.grille.placement_grille(colonne, ligne)

        # Création du PNG interactif représentant l'usine
        usine = UI_PNG(self.screen, self.dico_info.type_cases["Usine"][0], (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0)  # 5 = agrandissement hover, 0 = volume son

        # Initialisation des propriétés de l'usine
        usine.frame = 0  # frame courante pour l'animation
        usine.last_update = pygame.time.get_ticks()  # timestamp dernière frame
        usine.ligne = ligne
        usine.colonne = colonne

        # Préparation des frames pour l'animation de spawn de l'usine
        frames = [os.path.join(self.BASE_DIR, "sprite", "sprite_usine", f"sprite_usine_spawn_{str(i).zfill(2)}.png") for i in range(19)]
        self.animation.ajouter_animation(frames, self.animation.scale(5, ligne, colonne)[1], self.animation.scale(5, ligne, colonne)[0], frame_delay = 40)

        # Récupération du plan de jeu actuel
        plan = self.plan_ref()

        # Ajout de l'usine au dictionnaire d'animations
        self.dico_UI_anim[plan]["Usine"][self.nbr_usines_spawn] = usine

        # Marquer la case de la grille comme "usine"
        self.grille.grille[ligne][colonne] = "usine"

        # Liste des positions autour de l'usine à "condamner"
        self.position_init = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                              (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                              (0, -2), (0, -1), (0, 1), (0, 2),
                              (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                              (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]

        # Parcours des positions autour et ajout des cases "condamnées"
        for d_ligne, d_colonne in self.position_init:
            new_ligne = ligne + d_ligne
            new_colonne = colonne + d_colonne
            self.condamne.ajout_condamne(new_ligne, new_colonne)

        # Incrémentation du compteur d'usines ajoutées
        self.nbr_usines_spawn += 1

        # Lecture d'un son aléatoire lors du spawn
        self.usine_sound = pygame.mixer.Sound(f"{self.SOUND_USINE_PATH[randint(0,2)]}.wav")
        self.usine_sound.set_volume(0.05)
        self.usine_sound.play()


    def anim_usine(self):
        '''Anime toutes les usines en faisant défiler les frames'''

        frame_delay = 120  # délai entre frames en millisecondes
        now = pygame.time.get_ticks()

        # Parcours de toutes les usines du plan actuel
        for usine in self.dico_UI_anim[self.plan_ref()]["Usine"].values():
            if now - usine.last_update >= frame_delay:
                # passage à la frame suivante
                usine.frame = (usine.frame + 1) % len(self.usine_frames)
                usine.last_update = now

                # Mise à jour de l'image affichée
                usine.img_base = self.usine_frames[usine.frame]