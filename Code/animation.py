import pygame
from ui_tools import UI_PNG
from grille import *


class Animation:

    def __init__(self, screen, plan_ref, dico_UI_anim, grille):
        self.screen = screen
        self.plan_ref = plan_ref
        self.dico_UI_anim = dico_UI_anim
        self.grille = grille

        self.animations = {}
        self.next_id = 0

    def ajouter_animation(self, frames_paths, position, taille, frame_delay=80):
        """
        frames_paths : liste de chemins d'images
        position : (x, y)
        taille : (largeur, hauteur)
        """

        x, y = position
        w, h = taille

        animation = UI_PNG(
            self.screen,
            frames_paths[0],
            (x, y, w, h),
            5,
            0
        )

        animation.frames = [pygame.image.load(path).convert_alpha() for path in frames_paths]
        animation.frame_index = 0
        animation.last_update = pygame.time.get_ticks()
        animation.frame_delay = frame_delay
        animation.total_frames = len(animation.frames)

        self.animations[self.next_id] = animation
        self.next_id += 1

    def update(self):
        now = pygame.time.get_ticks()

        for key, anim in list(self.animations.items()):

            if now - anim.last_update >= anim.frame_delay:
                anim.frame_index += 1
                anim.last_update = now

                if anim.frame_index >= anim.total_frames:
                    del self.animations[key]
                    continue

                anim.img_base = anim.frames[anim.frame_index]

    def draw(self):
        for anim in self.animations.values():
            anim.create()

    def scale(self, scale, ligne, colonne, from_top=0):
        largeur_anim = self.grille.case_Long * scale
        hauteur_anim = self.grille.case_larg * scale

        x, y = self.grille.placement_grille(colonne, ligne)

        x_center = x + self.grille.case_Long / 2
        y_center = y + self.grille.case_larg / 2

        # Position initiale au-dessus si demandé
        y_center_initial = y_center - hauteur_anim * from_top  # au-dessus de la case

        return ((largeur_anim, hauteur_anim), (x_center - largeur_anim / 2, y_center_initial - hauteur_anim / 2))