import pygame
import os

class Meteo:
    def __init__(self, screen, zone_grille_x, zone_grille_y, zone_largeur, zone_hauteur, plan_ref):
        self.screen = screen

        self.zone_x = zone_grille_x
        self.zone_y = zone_grille_y
        self.zone_L = zone_largeur
        self.zone_l = zone_hauteur
        self.last_frame = pygame.time.get_ticks()
        self.plan_ref = plan_ref  # référence vers le plan du jeu

        self.BASE_DIR = os.path.dirname(__file__)

        self.RAIN_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_effet_pluie", "sprite_pluie_")
        self.sprite_pluie = [pygame.image.load(f"{self.RAIN_PATH}{str(i).zfill(2)}.png").convert() for i in range(23)] # Importation des 23 frames
        self.sprite_pluie = [pygame.transform.scale(elt, (self.zone_L, self.zone_l)) for elt in self.sprite_pluie] # Convertion des frames pour la grille
        self.pluie_frame = 0      

    def pluie(self):
        '''
        Cette méthode gère la pluie
        '''
        now = pygame.time.get_ticks()
        rain_delay = 50 # Delai en ms

        if now - self.last_frame >= rain_delay and self.plan_ref() == 0:
            self.pluie_frame = (self.pluie_frame + 1) % len(self.sprite_pluie)
            self.last_frame = now

        image = self.sprite_pluie[self.pluie_frame]
        image.set_alpha(155)  # Change l'opacité ici

        self.screen.blit(image, (self.zone_x, self.zone_y))