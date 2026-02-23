import pygame
from ui_tools import UI_PNG
from dico_info_game import *
from random import randint

class CaseBrulee:

    def __init__(self, screen, grille, ligne, colonne, dico_UI_interact, plan_ref):
        self.screen = screen
        self.grille = grille
        self.ligne = ligne
        self.colonne = colonne
        self.dico_UI_interact = dico_UI_interact
        self.plan_ref = plan_ref

        self.dico_info = Dico_info_Game()

        self.spawn_time = pygame.time.get_ticks()
        self.base_regen_time = 8000  

        x, y = self.grille.placement_grille(colonne, ligne)

        self.img = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Case brulee"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            1,
            0
        )

        self.img.ligne = ligne
        self.img.colonne = colonne

    def temps_regeneration(self, meteo):
        regen = self.base_regen_time

        if meteo.pluie_active:
            regen *= 0.6

        return regen

    def update(self, meteo):
        now = pygame.time.get_ticks()

        if now - self.spawn_time >= self.temps_regeneration(meteo):
            self.transformer_en_herbe()
            return True

        return False

    def transformer_en_herbe(self):
        plan = self.plan_ref()

        # Mise à jour logique
        self.grille.grille[self.ligne][self.colonne] = (0,255,0)

        # Création herbe
        x, y = self.grille.placement_grille(self.colonne, self.ligne)

        case_herbe = UI_PNG(
            self.screen,
            self.dico_info.type_cases[(0,255,0)][
                randint(0, len(self.dico_info.type_cases[(0,255,0)]) - 1)
            ],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            1,
            0
        )

        case_herbe.ligne = self.ligne
        case_herbe.colonne = self.colonne

        key = self.ligne * self.grille.colonnes + self.colonne
        self.dico_UI_interact[plan]["Case"][key] = case_herbe