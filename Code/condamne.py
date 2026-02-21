
import pygame
from dico_info_game import *
from ui_tools import UI_PNG

class Condamne:
    def __init__(self, screen, grille, data, dico_UI_anim, plan_ref):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.plan_ref = plan_ref  # référence vers le plan du jeu

        self.dico_info = Dico_info_Game()
        self.croix_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Terre inutilisable"]]

        self.nbr_croix_spawn = 0

    def ajout_condamne(self, ligne, colonne):

        # Vérification des bornes (sécurité)
        if not (0 <= ligne < self.grille.lignes and 0 <= colonne < self.grille.colonnes):
            return

    # Empêche de condamner une case déjà condamnée
        if self.grille.grille[ligne][colonne] == "condamne":
            return

        x, y = self.grille.placement_grille(colonne, ligne)

        croix = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Terre inutilisable"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            5, 0
        )

        croix.frame = 0
        croix.last_update = pygame.time.get_ticks()
        croix.ligne = ligne
        croix.colonne = colonne

        self.grille.grille[ligne][colonne] = "condamne"

        self.dico_UI_anim[0]["Croix"][len(self.dico_UI_anim[0]["Croix"])] = croix
        self.nbr_croix_spawn += 1

    def anim_condamne(self):
        FRAME_DELAY = 120 # en ms
        now = pygame.time.get_ticks()

        for croix in self.dico_UI_anim[self.plan_ref()]["Croix"].values():
            if now - croix.last_update >= FRAME_DELAY:
                croix.frame = (croix.frame + 1) % len(self.croix_frames)
                croix.last_update = now

                # Juste changer la surface, PAS recharger
                croix.img_base = self.croix_frames[croix.frame]