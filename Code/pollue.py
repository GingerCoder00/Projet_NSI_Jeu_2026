
import pygame
from dico_info_game import *
from ui_tools import UI_PNG

class Pollue:
    def __init__(self, screen, grille, data, dico_UI_anim, plan_ref):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.plan_ref = plan_ref  # référence vers le plan du jeu

        self.dico_info = Dico_info_Game()
        self.poubelle_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case ETDB"]]

        self.nbr_poubelle_spawn = 0

    def ajout_pollue(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        poubelle = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Case pollue"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            5, 0
        )

        poubelle.frame = 0
        poubelle.last_update = pygame.time.get_ticks()

        self.dico_UI_anim[0]["Poubelle"][len(self.dico_UI_anim[0]["Poubelle"])] = poubelle
        self.grille.grille[ligne][colonne] = "pollue"
        self.nbr_poubelle_spawn += 1

    def anim_pollue(self):
        FRAME_DELAY = 120  # ms
        now = pygame.time.get_ticks()

        for poubelle in self.dico_UI_anim[self.plan_ref()]["Poubelle"].values():
            if now - poubelle.last_update >= FRAME_DELAY:
                poubelle.frame = (poubelle.frame + 1) % len(self.dico_info.type_cases["Case pollue"])
                poubelle.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                poubelle.IMG_PATH = self.dico_info.type_cases["Case pollue"][poubelle.frame]
                poubelle.img_base = pygame.image.load(poubelle.IMG_PATH).convert_alpha()