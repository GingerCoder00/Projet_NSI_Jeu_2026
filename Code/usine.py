import pygame
from ui_tools import UI_PNG
from data import *
from grille import *
from dico_info_game import *
from condamne import *

class Usine:
    def __init__(self, screen, grille, data, dico_UI_anim, plan_ref):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.plan_ref = plan_ref  # référence vers le plan du jeu

        self.condamne = Condamne(screen, grille, data, dico_UI_anim, plan_ref)

        self.dico_info = Dico_info_Game()
        self.usine_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Usine"]]

        self.nbr_usines_spawn = 0

    def ajout_usine(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        usine = UI_PNG(self.screen, self.dico_info.type_cases["Usine"][0], (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0)

        usine.frame = 0
        usine.last_update = pygame.time.get_ticks()

        plan = self.plan_ref()
        self.dico_UI_anim[plan]["Usine"][self.nbr_usines_spawn] = usine
        self.grille.grille[ligne][colonne] = "usine"

        self.position_init = [(-1, -1), (-1, 0), (-1, 1),
                              (0, -1), (0, 1),
                              (1, -1), (1, 0), (1, 1)]
        
        for d_ligne, d_colonne in self.position_init:
            new_ligne = ligne + d_ligne
            new_colonne = colonne + d_colonne

            # Vérification des bornes
            self.condamne.ajout_condamne(new_ligne, new_colonne)

        self.nbr_usines_spawn += 1

    def anim_usine(self):
        frame_delay = 120  # ms
        now = pygame.time.get_ticks()

        for usine in self.dico_UI_anim[self.plan_ref()]["Usine"].values():
            if now - usine.last_update >= frame_delay:
                usine.frame = (usine.frame + 1) % len(self.usine_frames)
                usine.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                usine.img_base = self.usine_frames[usine.frame]