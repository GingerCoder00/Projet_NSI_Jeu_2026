import pygame
import os
from random import randint, random

class Meteo:

    def __init__(self, screen, zone_grille_x, zone_grille_y,
                 zone_largeur, zone_hauteur,
                 plan_ref, data, grille, flamme):

        self.screen = screen
        self.plan_ref = plan_ref
        self.data = data
        self.grille = grille
        self.flamme = flamme

        self.zone_x = zone_grille_x
        self.zone_y = zone_grille_y
        self.zone_L = zone_largeur
        self.zone_l = zone_hauteur

        self.last_frame = pygame.time.get_ticks()
        self.last_event = pygame.time.get_ticks()

        self.BASE_DIR = os.path.dirname(__file__)

        # PLUIE SPRITES
        self.RAIN_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_effet_pluie", "sprite_pluie_")
        self.sprite_pluie = [pygame.image.load(f"{self.RAIN_PATH}{str(i).zfill(2)}.png").convert() for i in range(23)]
        self.sprite_pluie = [pygame.transform.scale(elt, (self.zone_L, self.zone_l)) for elt in self.sprite_pluie]
        self.pluie_frame = 0

        # ÉTATS
        self.current_event = None
        self.event_duration = 9000

        self.pluie_active = False
        self.canicule_active = False
        self.vent_active = False
        self.gel_active = False
        self.smog_active = False
        self.orage_active = False

        # Orage visuel
        self.flash_alpha = 0

        self.events = [
                ["pluie", 0.6],
                ["canicule", 0.3],
                ["gel", 0.45],
                ["orage", 0.4],
                ["tornade", 0.35],
                ["inondation", 0.25],
                ["reforestation", 0.8],
                ["intervention ecologiste", 0.5],
                ["sécheresse ciblée", 0.3],
                ["epidemie", 0.4],
                ["météorite", 0.1],
                ["Nuage", 1],      # Les nuages sont des événements constant pendant tout le jeu pour apporter de la vie
                [None, 1]
            ]

    def update_event(self):

        now = pygame.time.get_ticks()

        if now - self.last_event > self.event_duration:

            self.last_event = now

            self.current_event = self.events[randint(0, len(self.events)-1)]

            self.pluie_active = self.current_event == "pluie"
            self.canicule_active = self.current_event == "canicule"
            self.vent_active = self.current_event == "vent"
            self.gel_active = self.current_event == "gel"
            self.smog_active = self.current_event == "smog"
            self.orage_active = self.current_event == "orage"

    def pluie(self):

        if not self.pluie_active:
            return

        now = pygame.time.get_ticks()
        rain_delay = 50

        if now - self.last_frame >= rain_delay:
            self.pluie_frame = (self.pluie_frame + 1) % len(self.sprite_pluie)
            self.last_frame = now

        image = self.sprite_pluie[self.pluie_frame]
        image.set_alpha(120)
        self.screen.blit(image, (self.zone_x, self.zone_y))

        # Effets gameplay
        self.data.eau += 0.03
        self.data.biodiversite += 0.02

    def canicule(self):

        if not self.canicule_active:
            return

        self.data.eau -= 0.04
        self.data.biodiversite -= 0.02

    def orage(self):

        if not self.orage_active:
            return

        # Flash visuel
        if random() < 0.05:
            self.flash_alpha = 150

        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((self.zone_L, self.zone_l))
            flash_surface.fill((255,255,255))
            flash_surface.set_alpha(self.flash_alpha)
            self.screen.blit(flash_surface, (self.zone_x, self.zone_y))
            self.flash_alpha -= 10

        # Chance de déclencher un feu
        if random() < 0.02:

            ligne = randint(0, self.grille.lignes - 1)
            colonne = randint(0, self.grille.colonnes - 1)

            if self.grille.grille[ligne][colonne] == (0,50,0):
                self.flamme.propagation_feu(
                    ligne,
                    colonne,
                    puissance=3,
                    spawn_anim=True
                )
    
    def gel(self):

        if not self.gel_active:
            return

        # Ralentit propagation via malus
        pass

    def update(self):

        if self.plan_ref() != 0:
            return

        self.update_event()

        self.pluie()
        self.canicule()
        self.gel()
        self.orage()