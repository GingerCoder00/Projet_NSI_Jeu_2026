import pygame
from ui_tools import *
from random import random
from data import *
from grille import *
from dico_info_game import *

class Flamme:
    def __init__(self, screen, grille, data, dico_UI_anim, plan_ref):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.plan_ref = plan_ref  # référence vers le plan du jeu

        self.dico_info = Dico_info_Game()
        self.fire_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case ETDB"]]

        self.file_propagation = []
        self.last_fire_update = pygame.time.get_ticks()
        self.fire_delay = 1200

        self.nbr_flammes_spawn = 0

    def ajout_feu(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        flamme = UI_PNG(self.screen, self.dico_info.type_cases["Case ETDB"][0], (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0)

        flamme.frame = 0
        flamme.last_update = pygame.time.get_ticks()

        plan = self.plan_ref()
        self.dico_UI_anim[plan]["Flamme"][self.nbr_flammes_spawn] = flamme

        self.nbr_flammes_spawn += 1

    def anim_feu(self):
        frame_delay = 105  # ms
        now = pygame.time.get_ticks()

        for flamme in self.dico_UI_anim[self.plan_ref()]["Flamme"].values():
            if now - flamme.last_update >= frame_delay:
                flamme.frame = (flamme.frame + 1) % len(self.dico_info.type_cases["Case ETDB"])
                flamme.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                flamme.img_base = self.fire_frames[flamme.frame]

    def proba_propagation(self):
        """
        Retourne une probabilité entre 0 et 1
        dépendante de la température
        """
        # Base minimale
        base = 0.15  

        # Influence température (0 → 100)
        influence = self.data.temperature / 150  

        # Limite max
        return min(0.85, base + influence)
    
    def puissance_feu(self):
        '''
        Détermine la profondeur de propagation
        '''
        return 3 + int(self.data.temperature / 25)

    def propagation_feu(self, ligne, colonne, puissance):
        if puissance <= 0:
            return

        if self.grille.grille[ligne][colonne] in [(0,0,255), "feu"]:
            return
        else:
            self.grille.grille[ligne][colonne] = "feu"
            self.ajout_feu(ligne, colonne)

            proba = self.proba_propagation()

            # Haut
            if ligne > 0 and random() < proba:
                self.file_propagation.append((ligne - 1, colonne, puissance - 1))

            # Bas
            if ligne < self.grille.lignes - 1 and random() < proba:
                self.file_propagation.append((ligne + 1, colonne, puissance - 1))

            # Gauche
            if colonne > 0 and random() < proba:
                self.file_propagation.append((ligne, colonne - 1, puissance - 1))

            # Droite
            if colonne < self.grille.colonnes - 1 and random() < proba:
                self.file_propagation.append((ligne, colonne + 1, puissance - 1))


    def update_propagation_feu(self):
        now = pygame.time.get_ticks()

        if now - self.last_fire_update < self.fire_delay:
            return

        self.last_fire_update = now

        # On prend une vague complète
        vague = self.file_propagation.copy()
        self.file_propagation.clear()

        for ligne, colonne, puissance in vague:
            self.propagation_feu(ligne, colonne, puissance)
    