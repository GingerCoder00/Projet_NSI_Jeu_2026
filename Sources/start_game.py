# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
import os
from ui_tools import *
from animation import *
from resp_tools import *
from notification import *
from phrases_notif import PHRASES_AIDE_START

# Initialisation des modules Pygame nécessaires
pygame.init()
pygame.mixer.init()
pygame.font.init()


class StartGame:
    """
    Classe gérant l'écran de démarrage du jeu.
    Elle s'occupe de l'affichage des règles, jauges, pouvoirs,
    boutons START / RETOUR et des notifications d'aide.
    """
    def __init__(self, screen):

        self.screen = screen
        self.Long, self.larg = screen.get_size()  # dimensions de l'écran
        self.BASE_DIR = os.path.dirname(__file__)  # chemin du dossier du script

        self.resp = Resp_tools(self.Long, self.larg)  # outil pour positions responsives

        # Police du texte
        FONT_PATH = os.path.join(self.BASE_DIR, "font", "font_retro.ttf")
        self.font = pygame.font.Font(FONT_PATH, 20)

        self.start_time = pygame.time.get_ticks()  # Temps au lancement
        self.clock = pygame.time.Clock()            # Clock pour FPS et timing
        self.running = True                          # Contrôle de la boucle principale
        
        # Ratios pour placer les éléments UI de manière responsive
        self.ratio_objet = {
            "Rect_Fond": (0, 0, 1, 1),
            "Rect_Info_Pouvoir": (0.43, 0.05, 0.53, 0.9),
            "Rect_Info_Start": (0.04, 0.05, 0.35, 0.9),
            "Rect_Regle": (0.075, 0.1, 0.28, 0.45),
            "Rect_Jauge": (0.6, 0.1, 0.33, 0.3),
            "Rect_Pouvoir_Feu": (0.6, 0.46, 0.33, 0.2),
            "Rect_Pouvoir_Guerre": (0.6, 0.71, 0.33, 0.2),
            "Bouton_Retour": (0.111, 0.79, 0.2, 0.1, 0.2),
            "Bouton_Start": (0.089, 0.61, 0.25, 0.15, 0.22),
            "Jauge_Bio": (0.495, 0.08, 0.05, 0.34),
            "Bouton_Feu": (0.47, 0.47, 0.1, 0.18),
            "Bouton_Guerre" : (0.47, 0.72, 0.1, 0.18),
        }

        # Chemins vers les sprites
        self.JAUGE_BIO_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_biodiversite", "sprite_jauge_biodiversite_4.png")
        self.JAUGE_TOTAL_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_total", "sprite_jauge_total_08.png")
        self.BOUTON_FEU_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_feu", "sprite_bouton_feu_0.png")
        self.BOUTON_GUERRE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_guerre", "sprite_bouton_guerre_0.png")

        # Création des rectangles et zones UI principales
        self.dico_UI = {
            "Rect_Fond": UI_screen(self.screen, (31, 191, 184), (31, 191, 184), self.resp.resp(*self.ratio_objet["Rect_Fond"]), pulse=False),
            "Rect_Info_Pouvoir": UI_screen(self.screen, (5, 113, 108), (25, 120, 165), self.resp.resp(*self.ratio_objet["Rect_Info_Pouvoir"]), taille_contour=6, border_radius=12, pulse=False),
            "Rect_Info_Start": UI_screen(self.screen, (5, 113, 108), (25, 120, 165), self.resp.resp(*self.ratio_objet["Rect_Info_Start"]), taille_contour=6, border_radius=12, pulse=False),
            "Rect_Regle": UI_screen(self.screen, (230, 134, 57), (230, 193, 110), self.resp.resp(*self.ratio_objet["Rect_Regle"]), taille_contour=6, border_radius=12, pulse=False),
            "Rect_Jauge": UI_screen(self.screen, (230, 134, 57), (230, 193, 110), self.resp.resp(*self.ratio_objet["Rect_Jauge"]), taille_contour=6, border_radius=12, pulse=False),
            "Rect_Pouvoir_Feu": UI_screen(self.screen, (230, 134, 57), (230, 193, 110), self.resp.resp(*self.ratio_objet["Rect_Pouvoir_Feu"]), taille_contour=6, border_radius=12, pulse=False),
            "Rect_Pouvoir_Guerre": UI_screen(self.screen, (230, 134, 57), (230, 193, 110), self.resp.resp(*self.ratio_objet["Rect_Pouvoir_Guerre"]), taille_contour=6, border_radius=12, pulse=False),
        }

        # Boutons interactifs
        self.dico_UI_interact = {
            "Bouton_Retour": UI_Bouton(self.screen, (232, 221, 67), (0,0,0), self.resp.resp_font(self.ratio_objet["Bouton_Retour"][2], self.ratio_objet["Bouton_Retour"][4]), self.resp.resp(*self.ratio_objet["Bouton_Retour"][:4]), "RETOUR", taille_contour = 6, border_radius = 12, ampli_inflate = 16, volume_son = 0.05),
            "Bouton_Start": UI_Bouton(self.screen, (232, 221, 67), (0,0,0), self.resp.resp_font(self.ratio_objet["Bouton_Start"][2], self.ratio_objet["Bouton_Start"][4]), self.resp.resp(*self.ratio_objet["Bouton_Start"][:4]), "START", taille_contour = 6, border_radius = 12, ampli_inflate = 16, volume_son = 0.05),
        }

        # Sprites statiques
        self.dico_PNG = {
            "Jauge_Bio" : UI_PNG(self.screen, self.JAUGE_BIO_PATH, self.resp.resp(*self.ratio_objet["Jauge_Bio"]), 0, 0, hover_on = False),
            "Bouton_Feu" : UI_PNG(self.screen, self.BOUTON_FEU_PATH, self.resp.resp(*self.ratio_objet["Bouton_Feu"]), 0, 0, hover_on = False),
            "Bouton_Guerre" : UI_PNG(self.screen, self.BOUTON_GUERRE_PATH, self.resp.resp(*self.ratio_objet["Bouton_Guerre"]), 0, 0, hover_on = False),
        }

        # Notifications d'aide
        self.notification1 = Notification_gestion(self.screen, self.dico_UI["Rect_Regle"], (0, 0, 0), font_size_ratio = 0.065, diff_y = 25, volume_sound = 0)
        self.notification2 = Notification_gestion(self.screen, self.dico_UI["Rect_Jauge"], (0, 0, 0), font_size_ratio = 0.1, diff_y = 25, volume_sound = 0)
        self.notification3 = Notification_gestion(self.screen, self.dico_UI["Rect_Pouvoir_Feu"], (0, 0, 0), font_size_ratio = 0.123, diff_y = 25, volume_sound = 0)
        self.notification4 = Notification_gestion(self.screen, self.dico_UI["Rect_Pouvoir_Guerre"], (0, 0, 0), font_size_ratio = 0.123, diff_y = 25, volume_sound = 0)

        # Ajout des phrases d'aide
        phrases = PHRASES_AIDE_START
        self.notification1.ajouter(phrases[0])
        self.notification2.ajouter(phrases[1])
        self.notification3.ajouter(phrases[2])
        self.notification4.ajouter(phrases[3])


    # Gestion de sortie ou bouton retour
    def exit(self):
        """Vérifie si le joueur ferme la fenêtre ou clique sur RETOUR"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.dico_UI_interact["Bouton_Retour"].mouse_is_click():
            self.running = False

    # Vérifie si START est cliqué
    def start(self):
        return self.dico_UI_interact["Bouton_Start"].mouse_is_click()
    
    # Vérifie si RETOUR est cliqué
    def retour(self):
        return self.dico_UI_interact["Bouton_Retour"].mouse_is_click()

    # Affichage des stats (FPS et timer)
    def stats(self):
        if pygame.key.get_pressed()[pygame.K_F1]:
            txt = self.font.render(f"FPS : {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.screen.blit(txt, (10, 10))
            txt = self.font.render(f"Timer : {self.temps_ecoule}", True, (255,255,255))  # Temps écoulé
            self.screen.blit(txt, (10,25))

    # Dessine l'ensemble de l'écran de start
    def draw(self):
        self.screen.fill((0, 0, 0))

        # Mise à jour des rectangles UI
        for interfaces in self.dico_UI.values():
            interfaces.update()

        # Mise à jour des boutons interactifs
        for objet in self.dico_UI_interact.values():
            objet.update()

        # Mise à jour des PNG
        for png in self.dico_PNG.values():
            png.create()

        # Mise à jour des notifications
        self.notification1.update(); self.notification1.draw()
        self.notification2.update(); self.notification2.draw()
        self.notification3.update(); self.notification3.draw()
        self.notification4.update(); self.notification4.draw()
        
        # Affichage optionnel des stats
        self.stats()

        pygame.display.update()  # Mise à jour de l'affichage (plus léger que flip())

    # Boucle principale du StartGame (appelée depuis le jeu)
    def run(self):
        self.clock.tick(60)  # Limite FPS à 60
        self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000
        self.exit()           # Vérifie sortie ou retour
        self.draw()           # Affiche tout à l'écran