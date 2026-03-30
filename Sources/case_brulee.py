# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from ui_tools import UI_PNG
from dico_info_game import *
from random import randint

class CaseBrulee:
    '''
    Cette classe permet de gérer les cases brûlé qui apparaissent après qu'une flamme se soit éteinte
    '''

    def __init__(self, screen, grille, ligne, colonne, dico_UI_interact, plan_ref):
        self.screen = screen
        self.grille = grille
        self.ligne = ligne
        self.colonne = colonne
        self.dico_UI_interact = dico_UI_interact
        self.plan_ref = plan_ref

        self.dico_info = Dico_info_Game()

        self.spawn_time = pygame.time.get_ticks()
        self.base_regen_time = 8000      # Temps de régénération d'une case brûlée. Après la régénération, elle devient de l'herbe

        x, y = self.grille.placement_grille(colonne, ligne)

        self.img = UI_PNG(self.screen, self.dico_info.type_cases["Case brulee"][randint(0, 1)], (x, y, self.grille.case_Long, self.grille.case_larg), 1, 0)  # On utilise la classe UI_PNG pour afficher le sprite

        self.img.ligne = ligne
        self.img.colonne = colonne

    def temps_regeneration(self, meteo):
        '''
        Cette méthode permet de calculer le temps de régénération d'une case en appliquant des conditions (pluie, canicule)
        '''
        regen = self.base_regen_time

        if meteo.pluie_active:  # On baisse le temps de régénération quand il pleut
            regen *= 0.6

        if meteo.canicule_active:  # On augmente le temps de régénération quand il y a de la canicule
            regen *= 1.2

        return regen

    def update(self, meteo):
        '''
        Cette méthode permet d'actualiser l'état d'une case brûlée
        '''
        now = pygame.time.get_ticks()

        if now - self.spawn_time >= self.temps_regeneration(meteo):  # Si le temps de régénération est finit on transforme la case en herbe
            self.transformer_en_herbe()
            return True

        return False

    def transformer_en_herbe(self):
        '''
        Cette méthode gère le cas ou une case se transforme en herbe
        '''
        plan = self.plan_ref()

        # Mise à jour de la grille
        self.grille.grille[self.ligne][self.colonne] = (0,255,0)

        # Création d'herbe
        x, y = self.grille.placement_grille(self.colonne, self.ligne)

        case_herbe = UI_PNG(self.screen, self.dico_info.type_cases[(0,255,0)][randint(0, len(self.dico_info.type_cases[(0,255,0)]) - 1)], (x, y, self.grille.case_Long, self.grille.case_larg), 1, 0) # Création du sprite

        case_herbe.ligne = self.ligne
        case_herbe.colonne = self.colonne

        key = self.ligne * self.grille.colonnes + self.colonne

        # On ajoute la case au dictionnaire graphique du jeu principal pour qu'il puisse l'afficher
        self.dico_UI_interact[plan]["Case"][key] = case_herbe  
