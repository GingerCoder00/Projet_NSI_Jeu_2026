# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from ui_tools import UI_PNG
from grille import *


class Animation:
    '''
    Cette classe gère une animation ponctuelle
    '''

    def __init__(self, screen, plan_ref, dico_UI_anim, grille):
        self.screen = screen
        self.plan_ref = plan_ref
        self.dico_UI_anim = dico_UI_anim
        self.grille = grille

        # Stockage des animations
        self.animations = {}

        # ID de la prochaine frame
        self.next_id = 0

    def ajouter_animation(self, frames_paths, position, taille, frame_delay=80):
        '''
        Cette méthode permet d'ajouter une animation à une position et une taille donnée. Il faut aussi mettre en paramètre le chemin de 
        chaques frames dans le disque
        '''

        x, y = position
        w, h = taille

        animation = UI_PNG(self.screen, frames_paths[0], (x, y, w, h), 5, 0)  # Utilisation de la classe UI_PNG pour afficher l'image

        # Ajout d'attributs pour l'animation, ils permettront de mieux animer celle ci
        animation.frames = [pygame.image.load(path).convert_alpha() for path in frames_paths]
        animation.frame_index = 0
        animation.last_update = pygame.time.get_ticks()
        animation.frame_delay = frame_delay
        animation.total_frames = len(animation.frames)
        anim_id = self.next_id

        self.animations[self.next_id] = animation
        self.next_id += 1

        return anim_id

    def update(self):
        '''
        Cette méthode permet de gérer l'animation en changeant progressivement les frames avec un certain delai
        '''

        now = pygame.time.get_ticks()

        for key, anim in list(self.animations.items()):

            if now - anim.last_update >= anim.frame_delay:  # Quand le delai est atteint on change la frame
                anim.frame_index += 1
                anim.last_update = now

                if anim.frame_index >= anim.total_frames:  # Quand le nombre de frame total est atteint, supprime tout, en effet cette classe permet de gerer seulement les animation ponctuelles
                    del self.animations[key]
                    continue

                anim.img_base = anim.frames[anim.frame_index]

    def draw(self):
        '''
        Cette méthode permet de d'afficher à l'écran les sprites
        '''
        for anim in self.animations.values():
            anim.create()

    def scale(self, scale, ligne, colonne, from_top = 0):
        '''
        Cette méthode peut être utilisée pour modifier la taille d'une animation ou corriger sa position
        '''
        largeur_anim = self.grille.case_Long * scale
        hauteur_anim = self.grille.case_larg * scale

        x, y = self.grille.placement_grille(colonne, ligne)

        x_center = x + self.grille.case_Long / 2
        y_center = y + self.grille.case_larg / 2

        # Position initiale au-dessus si demandé
        y_center_initial = y_center - hauteur_anim * from_top  # au-dessus de la case

        return ((largeur_anim, hauteur_anim), (x_center - largeur_anim / 2, y_center_initial - hauteur_anim / 2)) # On retourne les nouvelles valeurs de position et de taille
