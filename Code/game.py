import pygame
import os
from ui_tools import *
from jauge import *
from data import *
from meteo import *
from resp_tools import *
from grille import *
from dico_info_game import *
from flamme import *
from condamne import *
from pollue import *
from usine import *
from pouvoir import *
from animation import *
from notification import *
from start_game import StartGame
from endgame import EndGame
from save import score

pygame.init()
pygame.mixer.init()
pygame.font.init()

class Game:
    '''Classe qui gère le Jeu'''
    def __init__(self, screen):

        self.Long, self.larg = screen.get_size()

        self.BASE_DIR = os.path.dirname(__file__)

        self.screen = screen

        self.score_path = os.path.join(self.BASE_DIR, "best_score.txt")

        self.start_game = StartGame(self.screen)

        # Gestion du temps
        self.start_time = pygame.time.get_ticks()  # Temps de départ après l'initialisation de pygame
        self.clock = pygame.time.Clock() # Initialisation de l'horloge interne du jeu
        self.temps_ecoule = 0
        self.chrono = 0

        # Gestion du texte et importation de la police
        FONT_PATH = os.path.join(self.BASE_DIR, "font", "sans_sherif.otf")
        self.font = pygame.font.Font(FONT_PATH, 20)

        # Active et désactive la boucle de jeu
        self.running = True
        self.return_main_menu = True

        self.resp = Resp_tools(self.Long, self.larg)

        # Gestion des ratios de chaques objets graphiques pour la responsive
        self.ratio_objet = {
            "Rect_bouton": (0.01, 0.01, 0.75, 0.75),
            "Rect_jauge": (0.775, 0.01, 0.214, 0.975),
            "Rect_stats": (0.01, 0.789, 0.75, 0.1975),
            "Rect_notif": (0.024, 0.808, 0.38, 0.158),
            "Rect_power": (0.426, 0.808, 0.32, 0.158),
            "Texte_temps_chrono": (0.82, 0.05, 0.06),
            "Jauge_pollution": (0.791, 0.17, 0.039, 0.25),
            "Jauge_bio": (0.86, 0.17, 0.039, 0.25),
            "Jauge_niv_ocean": (0.93, 0.17, 0.039, 0.25),
            "Jauge_social": (0.791, 0.45, 0.039, 0.25),
            "Jauge_temp": (0.86, 0.45, 0.039, 0.25),
            "Jauge_nourriture": (0.93, 0.45, 0.039, 0.25),
            "Jauge_total": (0.78, 0.75, 0.205, 0.07),
            "Bouton_Feu": (0.434, 0.821, 0.047, 0.083),
            "Bouton_Usine" : (0.4844, 0.873, 0.047, 0.083),
            "Bouton_Guerre" : (0.5356, 0.821, 0.047, 0.083),
            "Bouton_Canicule" : (0.5875, 0.873, 0.047, 0.083),
            "Bouton_Maree_Noire" : (0.6389, 0.821, 0.047, 0.083),
            "Bouton_Desinformation" : (0.691, 0.873, 0.047, 0.083),
            "Bouton_Continuer" : (0.375, 0.12, 0.25, 0.15, 0.15),
            "Bouton_Option" : (0.375, 0.32, 0.25, 0.15, 0.18),
            "Bouton_Menu_Principal" : (0.375, 0.52, 0.25, 0.15, 0.1),
            "Bouton_Quitter" : (0.375, 0.72, 0.25, 0.15, 0.18),
            "Rect_Pause" : (0.3, 0.04, 0.4, 0.93),

            # Plan 1
            "Retour1" : (0.73, 0.22, 0.12, 0.07, 0.215),
            "Settings" : (0.125, 0.19, 0.75, 0.65),
            "Settings_select" : (0.14, 0.21, 0.20, 0.61),
            "Settings_modif" : (0.36, 0.39, 0.5, 0.43),
            "Son" : (0.165, 0.27, 0.15, 0.07, 0.215),
            "Couper_Son": (0.4, 0.5, 0.1, 0.2),
            "Couper_Music": (0.55, 0.5, 0.1, 0.2),
            "Text_setting" : (0.37, 0.25, 0.1775),
        }

        self.dico_info = Dico_info_Game()

        # Gestion des bruitages et de la musique
        self.son_off_on = ["son_on_off/son_on.png", "son_on_off/son_off.png"]
        self.son_actif = 0 # A comme rôle un indice dans le tableau self.son_off_on

        self.music_off_on = ["music_on_off/music_on.png", "music_on_off/music_off.png"]
        self.music_actif = 0 # A comme rôle un indice dans le tableau self.music_off_on
        self.current_music = None

        # Variable affichage
        # Num plan : {-1:start game, 0:grille, 1:pause}
        self.plan = -1
        self.sous_plan = 0

        self.BLACK_SCREEN_PATH =  os.path.join(self.BASE_DIR, "sprite", "sprite_ecran_noir")
        self.ecran_noir = pygame.image.load(f"{self.BLACK_SCREEN_PATH}.png").convert()  
        self.ecran_noir = pygame.transform.scale(self.ecran_noir, (self.Long, self.larg)) 
        self.ecran_noir.set_alpha(155)
       
        self.BOUTON_FEU_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_feu", "sprite_bouton_feu_0.png")
        self.BOUTON_USINE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_usine", "sprite_bouton_usine_0.png")
        self.BOUTON_GUERRE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_guerre", "sprite_bouton_guerre_0.png")
        self.BOUTON_CANICULE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_canicule", "sprite_bouton_canicule_6.png")
        self.BOUTON_MAREE_NOIRE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_maree_noire", "sprite_bouton_maree_noire_0.png")
        self.BOUTON_DESINFORMATION_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_desinformation", "sprite_bouton_desinformation_0.png")

        # Gestion des éléments intéractifs
        self.dico_UI_interact = {
            -1:{
                "Case": {},
                "CaseBrulee": {},
                "Bouton" : {}
            },
            0:{
                "Case": {},
                "CaseBrulee": {},

                "Bouton" : {
                    "Bouton_Feu" : UI_PNG(self.screen, self.BOUTON_FEU_PATH, self.resp.resp(self.ratio_objet["Bouton_Feu"][0], self.ratio_objet["Bouton_Feu"][1], self.ratio_objet["Bouton_Feu"][2], self.ratio_objet["Bouton_Feu"][3]), 8, 0.03),
                    "Bouton_Usine" : UI_PNG(self.screen, self.BOUTON_USINE_PATH, self.resp.resp(self.ratio_objet["Bouton_Usine"][0], self.ratio_objet["Bouton_Usine"][1], self.ratio_objet["Bouton_Usine"][2], self.ratio_objet["Bouton_Usine"][3]), 8, 0.03),
                    "Bouton_Guerre" : UI_PNG(self.screen, self.BOUTON_GUERRE_PATH, self.resp.resp(self.ratio_objet["Bouton_Guerre"][0], self.ratio_objet["Bouton_Guerre"][1], self.ratio_objet["Bouton_Guerre"][2], self.ratio_objet["Bouton_Guerre"][3]), 8, 0.03),
                    "Bouton_Canicule" : UI_PNG(self.screen, self.BOUTON_CANICULE_PATH, self.resp.resp(self.ratio_objet["Bouton_Canicule"][0], self.ratio_objet["Bouton_Canicule"][1], self.ratio_objet["Bouton_Canicule"][2], self.ratio_objet["Bouton_Canicule"][3]), 8, 0.03),
                    "Bouton_Maree_Noire" : UI_PNG(self.screen, self.BOUTON_MAREE_NOIRE_PATH, self.resp.resp(self.ratio_objet["Bouton_Maree_Noire"][0], self.ratio_objet["Bouton_Maree_Noire"][1], self.ratio_objet["Bouton_Maree_Noire"][2], self.ratio_objet["Bouton_Maree_Noire"][3]), 8, 0.03),
                    "Bouton_Desinformation" : UI_PNG(self.screen, self.BOUTON_DESINFORMATION_PATH, self.resp.resp(self.ratio_objet["Bouton_Desinformation"][0], self.ratio_objet["Bouton_Desinformation"][1], self.ratio_objet["Bouton_Desinformation"][2], self.ratio_objet["Bouton_Desinformation"][3]), 8, 0.03),
                },
            },
            1:{
                "Case": {},
                "CaseBrulee": {},

                "Bouton" : {
                    "Bouton_Feu" : UI_PNG(self.screen, self.BOUTON_FEU_PATH, self.resp.resp(self.ratio_objet["Bouton_Feu"][0], self.ratio_objet["Bouton_Feu"][1], self.ratio_objet["Bouton_Feu"][2], self.ratio_objet["Bouton_Feu"][3]), 8, 0.03),
                    "Bouton_Usine" : UI_PNG(self.screen, self.BOUTON_USINE_PATH, self.resp.resp(self.ratio_objet["Bouton_Usine"][0], self.ratio_objet["Bouton_Usine"][1], self.ratio_objet["Bouton_Usine"][2], self.ratio_objet["Bouton_Usine"][3]), 8, 0.03),
                    "Bouton_Guerre" : UI_PNG(self.screen, self.BOUTON_GUERRE_PATH, self.resp.resp(self.ratio_objet["Bouton_Guerre"][0], self.ratio_objet["Bouton_Guerre"][1], self.ratio_objet["Bouton_Guerre"][2], self.ratio_objet["Bouton_Guerre"][3]), 8, 0.03),
                    "Bouton_Canicule" : UI_PNG(self.screen, self.BOUTON_CANICULE_PATH, self.resp.resp(self.ratio_objet["Bouton_Canicule"][0], self.ratio_objet["Bouton_Canicule"][1], self.ratio_objet["Bouton_Canicule"][2], self.ratio_objet["Bouton_Canicule"][3]), 8, 0.03),
                    "Bouton_Maree_Noire" : UI_PNG(self.screen, self.BOUTON_MAREE_NOIRE_PATH, self.resp.resp(self.ratio_objet["Bouton_Maree_Noire"][0], self.ratio_objet["Bouton_Maree_Noire"][1], self.ratio_objet["Bouton_Maree_Noire"][2], self.ratio_objet["Bouton_Maree_Noire"][3]), 8, 0.03),
                    "Bouton_Desinformation" : UI_PNG(self.screen, self.BOUTON_DESINFORMATION_PATH, self.resp.resp(self.ratio_objet["Bouton_Desinformation"][0], self.ratio_objet["Bouton_Desinformation"][1], self.ratio_objet["Bouton_Desinformation"][2], self.ratio_objet["Bouton_Desinformation"][3]), 8, 0.03),
                },
            }
        }

        self.dico_UI_pause = {
            0:{ 
            },
            1:{
                "Rect_Pause" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_Pause"][0], self.ratio_objet["Rect_Pause"][1], self.ratio_objet["Rect_Pause"][2], self.ratio_objet["Rect_Pause"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Bouton_Continuer" : UI_Bouton(self.screen, (158, 253, 56), (0,0,0), self.resp.resp_font(self.ratio_objet["Bouton_Continuer"][2], self.ratio_objet["Bouton_Continuer"][4]), self.resp.resp(self.ratio_objet["Bouton_Continuer"][0], self.ratio_objet["Bouton_Continuer"][1], self.ratio_objet["Bouton_Continuer"][2], self.ratio_objet["Bouton_Continuer"][3]), "CONTINUER", 4, 12, 16, 0.05),
                "Bouton_Option" : UI_Bouton(self.screen, (158, 253, 56), (0,0,0), self.resp.resp_font(self.ratio_objet["Bouton_Option"][2], self.ratio_objet["Bouton_Option"][4]), self.resp.resp(self.ratio_objet["Bouton_Option"][0], self.ratio_objet["Bouton_Option"][1], self.ratio_objet["Bouton_Option"][2], self.ratio_objet["Bouton_Option"][3]), "OPTION", 4, 12, 16, 0.05),
                "Bouton_Menu_Principal" : UI_Bouton(self.screen, (158, 253, 56), (0,0,0), self.resp.resp_font(self.ratio_objet["Bouton_Menu_Principal"][2], self.ratio_objet["Bouton_Menu_Principal"][4]), self.resp.resp(self.ratio_objet["Bouton_Menu_Principal"][0], self.ratio_objet["Bouton_Menu_Principal"][1], self.ratio_objet["Bouton_Menu_Principal"][2], self.ratio_objet["Bouton_Menu_Principal"][3]), "MENU PRINCIPAL", 4, 12, 16, 0.05),
                "Bouton_Quitter" : UI_Bouton(self.screen, (158, 253, 56), (0,0,0), self.resp.resp_font(self.ratio_objet["Bouton_Quitter"][2], self.ratio_objet["Bouton_Quitter"][4]), self.resp.resp(self.ratio_objet["Bouton_Quitter"][0], self.ratio_objet["Bouton_Quitter"][1], self.ratio_objet["Bouton_Quitter"][2], self.ratio_objet["Bouton_Quitter"][3]), "QUITTER", 4, 12, 16, 0.05),
            },
            2:{
                "rect_settings" : UI_screen(self.screen, (16,52,166), (255,255,255), self.resp.resp(self.ratio_objet["Settings"][0], self.ratio_objet["Settings"][1], self.ratio_objet["Settings"][2], self.ratio_objet["Settings"][3]), taille_contour = 6, border_radius = 12),
                "rect_settings_select" : UI_screen(self.screen, (237,189,178), (0,0,0), self.resp.resp(self.ratio_objet["Settings_select"][0], self.ratio_objet["Settings_select"][1], self.ratio_objet["Settings_select"][2], self.ratio_objet["Settings_select"][3]), taille_contour = 4, border_radius = 12),
                "rect_settings_modif" : UI_screen(self.screen, (237,189,178), (0,0,0), self.resp.resp(self.ratio_objet["Settings_modif"][0], self.ratio_objet["Settings_modif"][1], self.ratio_objet["Settings_modif"][2], self.ratio_objet["Settings_modif"][3]), taille_contour = 4, border_radius = 12),
                "Text_setting" : Texte(self.screen, self.resp.resp_text(self.ratio_objet["Text_setting"][0], self.ratio_objet["Text_setting"][1]), self.resp.resp_font(self.ratio_objet["Text_setting"][0], self.ratio_objet["Text_setting"][2]), (255,255,255), "SETTINGS", font_type = "font/font_retro.ttf"),
                "Retour1": UI_Bouton(self.screen, (4, 139, 154), (0,0,0), self.resp.resp_font(self.ratio_objet["Retour1"][2], self.ratio_objet["Retour1"][4]), self.resp.resp(self.ratio_objet["Retour1"][0], self.ratio_objet["Retour1"][1], self.ratio_objet["Retour1"][2], self.ratio_objet["Retour1"][3]), "RETOUR", 5, 12, 16, 0.05),
                "Son": UI_Bouton(self.screen, (23, 167, 232), (0,0,0), self.resp.resp_font(self.ratio_objet["Son"][2], self.ratio_objet["Son"][4]), self.resp.resp(self.ratio_objet["Son"][0], self.ratio_objet["Son"][1], self.ratio_objet["Son"][2], self.ratio_objet["Son"][3]), "SON", 5, 12, 16, 0.05),
            }
        }


        self.grille = Grille(self.screen, 19, 30, 3.5, self.resp.resp(self.ratio_objet["Rect_bouton"][0], self.ratio_objet["Rect_bouton"][1], self.ratio_objet["Rect_bouton"][2], self.ratio_objet["Rect_bouton"][3]), self.dico_UI_interact)


        # Gestion des éléments graphiques non intéractif
        self.dico_UI = {
            0:{
                "Rect_bouton" : UI_screen(self.screen, (88, 41, 0), (255,255,255), self.grille.rect_zone, taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_jauge" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_jauge"][0], self.ratio_objet["Rect_jauge"][1], self.ratio_objet["Rect_jauge"][2], self.ratio_objet["Rect_jauge"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_stats" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_stats"][0], self.ratio_objet["Rect_stats"][1], self.ratio_objet["Rect_stats"][2], self.ratio_objet["Rect_stats"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_notif" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_notif"][0], self.ratio_objet["Rect_notif"][1], self.ratio_objet["Rect_notif"][2], self.ratio_objet["Rect_notif"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Rect_power" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_power"][0], self.ratio_objet["Rect_power"][1], self.ratio_objet["Rect_power"][2], self.ratio_objet["Rect_power"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Texte_temps_chrono" : Texte(self.screen, self.resp.resp_text(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][1]), self.resp.resp_font(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][2]), (0,0,0), f"{self.temps_ecoule}", font_type = "font/pixellari.ttf")
            },
            1:{
                "Rect_bouton" : UI_screen(self.screen, (88, 41, 0), (255,255,255), self.grille.rect_zone, taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_jauge" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_jauge"][0], self.ratio_objet["Rect_jauge"][1], self.ratio_objet["Rect_jauge"][2], self.ratio_objet["Rect_jauge"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_stats" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_stats"][0], self.ratio_objet["Rect_stats"][1], self.ratio_objet["Rect_stats"][2], self.ratio_objet["Rect_stats"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_notif" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_notif"][0], self.ratio_objet["Rect_notif"][1], self.ratio_objet["Rect_notif"][2], self.ratio_objet["Rect_notif"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Rect_power" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_power"][0], self.ratio_objet["Rect_power"][1], self.ratio_objet["Rect_power"][2], self.ratio_objet["Rect_power"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Texte_temps_chrono" : Texte(self.screen, self.resp.resp_text(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][1]), self.resp.resp_font(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][2]), (0,0,0), f"{self.temps_ecoule}", font_type = "font/pixellari.ttf"),
            },
            2:{
                "Rect_bouton" : UI_screen(self.screen, (88, 41, 0), (255,255,255), self.grille.rect_zone, taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_jauge" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_jauge"][0], self.ratio_objet["Rect_jauge"][1], self.ratio_objet["Rect_jauge"][2], self.ratio_objet["Rect_jauge"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_stats" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_stats"][0], self.ratio_objet["Rect_stats"][1], self.ratio_objet["Rect_stats"][2], self.ratio_objet["Rect_stats"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_notif" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_notif"][0], self.ratio_objet["Rect_notif"][1], self.ratio_objet["Rect_notif"][2], self.ratio_objet["Rect_notif"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Rect_power" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp.resp(self.ratio_objet["Rect_power"][0], self.ratio_objet["Rect_power"][1], self.ratio_objet["Rect_power"][2], self.ratio_objet["Rect_power"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Texte_temps_chrono" : Texte(self.screen, self.resp.resp_text(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][1]), self.resp.resp_font(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][2]), (0,0,0), f"{self.temps_ecoule}", font_type = "font/pixellari.ttf"),
            }
        }

        # Gestion des sprites ou surfaces des sous-plans
        self.setting_UI = {
            0:{
            },
            1:{
            "Couper_Son": UI_PNG(self.screen, self.son_off_on[self.son_actif], self.resp.resp(self.ratio_objet["Couper_Son"][0], self.ratio_objet["Couper_Son"][1], self.ratio_objet["Couper_Son"][2], self.ratio_objet["Couper_Son"][3]), 15, 0.05),
            "Couper_Music": UI_PNG(self.screen, self.music_off_on[self.music_actif], self.resp.resp(self.ratio_objet["Couper_Music"][0], self.ratio_objet["Couper_Music"][1], self.ratio_objet["Couper_Music"][2], self.ratio_objet["Couper_Music"][3]), 15, 0.05),
            },
            2:{
            },
        }

        self.notification = Notification_gestion(self.screen, self.dico_UI[0]["Rect_notif"])
        self.data = Data(self.grille, self.notification)

        self.JAUGE_POLLUTION_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_pollution", "sprite_jauge_pollution_")
        self.JAUGE_BIO_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_biodiversite", "sprite_jauge_biodiversite_")
        self.JAUGE_NIV_OCEAN_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_niv_ocean", "sprite_jauge_niv_ocean_")
        self.JAUGE_NOURRITURE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_nourriture", "sprite_jauge_nourriture_")
        self.JAUGE_SOCIAL_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_social", "sprite_jauge_social_")
        self.JAUGE_TEMP_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_temp", "sprite_jauge_temp_")
        self.JAUGE_TOTAL_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_jauge_total", "sprite_jauge_total_")

        # Gestion des éléments en animations
        self.dico_UI_anim = {
            0:{
                "Flamme" : {
                },
                "Poubelle" : {
                },
                "Croix" : {
                },
                "Usine" : {
                },
                "Jauge" : {
                    "Jauge_pollution" : Jauge(self.screen, self.JAUGE_POLLUTION_PATH, "pollution", lambda: self.data, self.resp.resp(self.ratio_objet["Jauge_pollution"][0], self.ratio_objet["Jauge_pollution"][1], self.ratio_objet["Jauge_pollution"][2], self.ratio_objet["Jauge_pollution"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.pollution)),
                    "Jauge_bio" : Jauge(self.screen, self.JAUGE_BIO_PATH, "biodiversite", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_bio"][0], self.ratio_objet["Jauge_bio"][1], self.ratio_objet["Jauge_bio"][2], self.ratio_objet["Jauge_bio"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.biodiversite)),
                    "Jauge_niv_ocean" : Jauge(self.screen, self.JAUGE_NIV_OCEAN_PATH, "eau", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_niv_ocean"][0], self.ratio_objet["Jauge_niv_ocean"][1], self.ratio_objet["Jauge_niv_ocean"][2], self.ratio_objet["Jauge_niv_ocean"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.eau)),
                    "Jauge_social" : Jauge(self.screen, self.JAUGE_SOCIAL_PATH, "stabilite", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_social"][0], self.ratio_objet["Jauge_social"][1], self.ratio_objet["Jauge_social"][2], self.ratio_objet["Jauge_social"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.stabilite)),
                    "Jauge_temp" : Jauge(self.screen, self.JAUGE_TEMP_PATH, "temperature", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_temp"][0], self.ratio_objet["Jauge_temp"][1], self.ratio_objet["Jauge_temp"][2], self.ratio_objet["Jauge_temp"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.temperature)),
                    "Jauge_nourriture" : Jauge(self.screen, self.JAUGE_NOURRITURE_PATH, "profit", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_nourriture"][0], self.ratio_objet["Jauge_nourriture"][1], self.ratio_objet["Jauge_nourriture"][2], self.ratio_objet["Jauge_nourriture"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.profit)),
                    "Jauge_total" : Jauge(self.screen, self.JAUGE_TOTAL_PATH, "destruction", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_total"][0], self.ratio_objet["Jauge_total"][1], self.ratio_objet["Jauge_total"][2], self.ratio_objet["Jauge_total"][3]), 7, 0.01, self.converte_data_into_frame(11, self.data.destruction), "0", nbr_frames = 11)
                },
            },
            1:{
                "Flamme" : {
                },
                "Poubelle" : {
                },
                "Croix" : {
                },
                "Usine" : {
                },
                "Jauge" : {
                    "Jauge_pollution" : Jauge(self.screen, self.JAUGE_POLLUTION_PATH, "pollution", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_pollution"][0], self.ratio_objet["Jauge_pollution"][1], self.ratio_objet["Jauge_pollution"][2], self.ratio_objet["Jauge_pollution"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.pollution)),
                    "Jauge_bio" : Jauge(self.screen, self.JAUGE_BIO_PATH, "biodiversite", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_bio"][0], self.ratio_objet["Jauge_bio"][1], self.ratio_objet["Jauge_bio"][2], self.ratio_objet["Jauge_bio"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.biodiversite)),
                    "Jauge_niv_ocean" : Jauge(self.screen, self.JAUGE_NIV_OCEAN_PATH, "eau", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_niv_ocean"][0], self.ratio_objet["Jauge_niv_ocean"][1], self.ratio_objet["Jauge_niv_ocean"][2], self.ratio_objet["Jauge_niv_ocean"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.eau)),
                    "Jauge_social" : Jauge(self.screen, self.JAUGE_SOCIAL_PATH, "stabilite", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_social"][0], self.ratio_objet["Jauge_social"][1], self.ratio_objet["Jauge_social"][2], self.ratio_objet["Jauge_social"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.stabilite)),
                    "Jauge_temp" : Jauge(self.screen, self.JAUGE_TEMP_PATH, "temperature", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_temp"][0], self.ratio_objet["Jauge_temp"][1], self.ratio_objet["Jauge_temp"][2], self.ratio_objet["Jauge_temp"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.temperature)),
                    "Jauge_nourriture" : Jauge(self.screen, self.JAUGE_NOURRITURE_PATH, "profit", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_nourriture"][0], self.ratio_objet["Jauge_nourriture"][1], self.ratio_objet["Jauge_nourriture"][2], self.ratio_objet["Jauge_nourriture"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.profit)),
                    "Jauge_total" : Jauge(self.screen, self.JAUGE_TOTAL_PATH, "destruction", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_total"][0], self.ratio_objet["Jauge_total"][1], self.ratio_objet["Jauge_total"][2], self.ratio_objet["Jauge_total"][3]), 7, 0.03, self.converte_data_into_frame(11, self.data.destruction), "0", nbr_frames = 11)
                },
            },
            2:{
                "Flamme" : {
                },
                "Poubelle" : {
                },
                "Croix" : {
                },
                "Usine" : {
                },
                "Jauge" : {
                    "Jauge_pollution" : Jauge(self.screen, self.JAUGE_POLLUTION_PATH, "pollution", lambda: self.data, self.resp.resp(self.ratio_objet["Jauge_pollution"][0], self.ratio_objet["Jauge_pollution"][1], self.ratio_objet["Jauge_pollution"][2], self.ratio_objet["Jauge_pollution"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.pollution)),
                    "Jauge_bio" : Jauge(self.screen, self.JAUGE_BIO_PATH, "biodiversite", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_bio"][0], self.ratio_objet["Jauge_bio"][1], self.ratio_objet["Jauge_bio"][2], self.ratio_objet["Jauge_bio"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.biodiversite)),
                    "Jauge_niv_ocean" : Jauge(self.screen, self.JAUGE_NIV_OCEAN_PATH, "eau", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_niv_ocean"][0], self.ratio_objet["Jauge_niv_ocean"][1], self.ratio_objet["Jauge_niv_ocean"][2], self.ratio_objet["Jauge_niv_ocean"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.eau)),
                    "Jauge_social" : Jauge(self.screen, self.JAUGE_SOCIAL_PATH, "stabilite", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_social"][0], self.ratio_objet["Jauge_social"][1], self.ratio_objet["Jauge_social"][2], self.ratio_objet["Jauge_social"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.stabilite)),
                    "Jauge_temp" : Jauge(self.screen, self.JAUGE_TEMP_PATH, "temperature", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_temp"][0], self.ratio_objet["Jauge_temp"][1], self.ratio_objet["Jauge_temp"][2], self.ratio_objet["Jauge_temp"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.temperature)),
                    "Jauge_nourriture" : Jauge(self.screen, self.JAUGE_NOURRITURE_PATH, "profit", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_nourriture"][0], self.ratio_objet["Jauge_nourriture"][1], self.ratio_objet["Jauge_nourriture"][2], self.ratio_objet["Jauge_nourriture"][3]), 7, 0.01, self.converte_data_into_frame(7, self.data.profit)),
                    "Jauge_total" : Jauge(self.screen, self.JAUGE_TOTAL_PATH, "destruction", lambda : self.data, self.resp.resp(self.ratio_objet["Jauge_total"][0], self.ratio_objet["Jauge_total"][1], self.ratio_objet["Jauge_total"][2], self.ratio_objet["Jauge_total"][3]), 7, 0.01, self.converte_data_into_frame(11, self.data.destruction), "0", nbr_frames = 11)
                },
            },
        }

        self.flamme = Flamme(self.screen, self.grille, self.data, self.dico_UI_anim, self.dico_UI_interact, lambda: self.plan, self.notification) # On utilise lambda car le plan change dynamiquement
        self.condamne = Condamne(self.screen, self.grille, self.data, self.dico_UI_anim, lambda: self.plan,) # On utilise lambda car le plan change dynamiquement
        self.pollue = Pollue(self.screen, self.grille, self.data, self.dico_UI_anim, self.dico_UI_interact, lambda: self.plan, self.notification) # On utilise lambda car le plan change dynamiquement
        self.usine = Usine(self.screen, self.grille, self.data, self.dico_UI_anim, lambda: self.plan) # On utilise lambda car le plan change dynamiquement

        self.meteo = Meteo(self.screen, self.grille.zone_x, self.grille.zone_y, self.grille.zone_L, self.grille.zone_l, lambda: self.plan, self.data, self.grille, self.flamme, self.notification, self.dico_UI_anim, self.dico_UI_interact) # On utilise lambda car le plan change dynamiquement

        self.pouvoir_actif = None
        self.pouvoirs = {
                "incendie": Pouvoir(self.screen,
                    "incendie",
                    self.dico_UI_interact[0]["Bouton"]["Bouton_Feu"],
                    self.data,
                    self.grille,
                    lambda l, c: self.flamme.propagation_feu(l, c, self.flamme.puissance_feu(), spawn_anim = True, origine_joueur = True),
                    self.notification,
                    cursor_sprite_prefix=os.path.join(self.BASE_DIR, "sprite\sprite_bouton_feu\sprite_logo_feu_"),
                    cursor_frame_count=2,
                    cooldown = 7,
                    frame_delay = 105,
                ),

                "usine": Pouvoir(self.screen,
                    "usine",
                    self.dico_UI_interact[0]["Bouton"]["Bouton_Usine"],
                    self.data,
                    self.grille,
                    lambda l, c: self.usine.ajout_usine(l, c),
                    self.notification,
                    cursor_sprite_prefix=os.path.join(self.BASE_DIR, "sprite\sprite_bouton_usine\sprite_logo_usine_"),
                    cursor_frame_count=3,
                    cooldown = 15,
                    frame_delay = 115,
                ),
                "guerre": Pouvoir(self.screen,
                    "guerre",
                    self.dico_UI_interact[0]["Bouton"]["Bouton_Guerre"],
                    self.data,
                    self.grille,
                    lambda : self.data.utiliser_pouvoir("guerre"),
                    self.notification,
                    cooldown = 30,
                    cible_grille=False
                ),
                "canicule": Pouvoir(self.screen,
                    "canicule",
                    self.dico_UI_interact[0]["Bouton"]["Bouton_Canicule"],
                    self.data,
                    self.grille,
                    lambda : self.data.utiliser_pouvoir("canicule"),
                    self.notification,
                    cooldown = 20,
                    cible_grille=False
                ),
                "Maree Noire": Pouvoir(self.screen,
                    "Maree Noire",
                    self.dico_UI_interact[0]["Bouton"]["Bouton_Maree_Noire"],
                    self.data,
                    self.grille,
                    lambda l, c: self.pollue.propagation_pollue(l, c, self.pollue.puissance_pollue(), spawn_anim = True),
                    self.notification,
                    cursor_sprite_prefix=os.path.join(self.BASE_DIR, "sprite\sprite_bouton_maree_noire\sprite_logo_maree_noire_"),
                    cursor_frame_count=1,
                    cooldown = 8,
                    frame_delay = 105,
                ),
                "desinformation": Pouvoir(self.screen,
                    "desinformation",
                    self.dico_UI_interact[0]["Bouton"]["Bouton_Desinformation"],
                    self.data,
                    self.grille,
                    lambda : self.data.utiliser_pouvoir("desinformation"),
                    self.notification,
                    cooldown = 45,
                    cible_grille=False
                ),
            }
        self.pouvoir_actif = None

    def converte_data_into_frame(self, nbr_frame, valeur_reel):
        valeur_reel = max(0, min(100, valeur_reel))
        return round((valeur_reel / 100) * (nbr_frame - 1))

    def exit(self):
        '''Gère la fermeture de la fenêtre'''
        # On récupère tous les évènements pour vérifier si il y a un événement de type : pygame.QUIT
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Ceci arrête la boucle principal

        if self.dico_UI_pause[1]["Bouton_Quitter"].mouse_is_click():
            self.running = False

        if self.dico_UI_pause[1]["Bouton_Menu_Principal"].mouse_is_click():
            self.return_main_menu = True
            self.running = False
    
    def play_music(self, fichier:str, volume:float = 0.7):
        '''
        Cette fonction importe et lance la musique en boucle
        '''
        if self.current_music == fichier:
            return  # La musique est déjà en train de jouer

        MUSIC_PATH = os.path.join(self.BASE_DIR, fichier)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

        self.current_music = fichier

    def couper_son(self):
        '''
        Cette méthode gère l'arrêt de tous bruitage dans les settings en cliquant sur le png correspondant
        '''
        if self.setting_UI[1]["Couper_Son"].mouse_is_click():  # On vérifie si le png de bruitage est bien cliqué
            self.son_actif = (self.son_actif + 1) % 2  # On change l'indice de sprite (le modulo permet de rester entre 0 et 1)

            IMG_PATH = os.path.join(self.BASE_DIR, "sprite", f"{self.son_off_on[self.son_actif]}")
            self.setting_UI[1]["Couper_Son"].img_base = pygame.image.load(IMG_PATH).convert_alpha()  # On modifie le sprite dans la classe

            if self.son_actif == 1:  # Ici si le son est coupé on réduit le volume pour tout les objets admettant des bruitages
                for boutons in self.dico_UI_interact.values():
                    for bouton in boutons.values():
                        for b in bouton.values():
                            b.volume = 0

                for pngs in self.setting_UI.values():
                    for png in pngs.values():
                        png.volume = 0

                for boutons in self.dico_UI_pause.values():
                    for bouton in boutons.values():
                        if isinstance(bouton, UI_Bouton):
                            bouton.volume = 0

                for boutons in self.dico_UI_anim.values():
                    for bouton in boutons.values():
                        for b in bouton.values():
                            b.volume = 0

            else: # Si le son est réactivé, on restaure les paramètres initiaux des objets concernant les bruitages
                for boutons in self.dico_UI_interact.values():
                    for bouton in boutons.values():
                        for b in bouton.values():
                            b.volume = 0.02

                for pngs in self.setting_UI.values():
                    for png in pngs.values():
                        png.volume = 0.03

                for boutons in self.dico_UI_pause.values():
                    for bouton in boutons.values():
                        if isinstance(bouton, UI_Bouton):
                            bouton.volume = 0.02

                for boutons in self.dico_UI_anim.values():
                    for bouton in boutons.values():
                        for b in bouton.values():
                            b.volume = 0.02

    def couper_musique(self):
        '''
        Cette méthode gère l'arrêt de la musique dans les settings en cliquant sur le png correspondant
        '''
        if self.setting_UI[1]["Couper_Music"].mouse_is_click(): # On vérifie si le png de la musique
            self.music_actif = (self.music_actif + 1) % 2 # On change l'indice de sprite (le modulo permet de rester entre 0 et 1)

            IMG_PATH = os.path.join(self.BASE_DIR, "sprite", f"{self.music_off_on[self.music_actif]}")
            self.setting_UI[1]["Couper_Music"].img_base = pygame.image.load(IMG_PATH).convert_alpha()  # On modifie le sprite dans la classe

            if self.music_actif == 1: # Ici si la musique est coupé on met en pause la musique
                pygame.mixer.music.pause()
            else: # Si la musique est réactivée, on reprend la musique
                pygame.mixer.music.unpause()

    def stats(self):
        '''
        Cette méthode permet de gérer l'affichage des stats de performance et de test
        '''
        if self.keys[pygame.K_F1]:
            self.screen.blit(self.font.render(f"FPS : {self.fps}", True, (0,0,0)), (0,0)) # Nombre FPS
            self.screen.blit(self.font.render(f"Timer : {self.temps_ecoule}", True, (0,0,0)), (0,25)) # Timer
            self.screen.blit(self.font.render(f"Num de plan : {self.plan}", True, (0,0,0)), (0,50)) # Numéro plan
            self.screen.blit(self.font.render(f"Taux de pollution : {self.data.pollution}", True, (0,0,0)), (0,75)) # Taux de Pollution
            self.screen.blit(self.font.render(f"Niveau de température : {self.data.temperature}", True, (0,0,0)), (0,100)) # Niveau de température
            self.screen.blit(self.font.render(f"Taux d'eau : {self.data.eau}", True, (0,0,0)), (0,125)) # Taux d'eau
            self.screen.blit(self.font.render(f"Taux de biodiversité : {self.data.biodiversite}", True, (0,0,0)), (0,150)) # Taux de biodiversité
            self.screen.blit(self.font.render(f"Taux de stabilité : {self.data.stabilite}", True, (0,0,0)), (0,175)) # Taux de stabilité
            self.screen.blit(self.font.render(f"Taux de profit : {self.data.profit}", True, (0,0,0)), (0,200)) # Taux de profit
            self.screen.blit(self.font.render(f"Taux de d'augmentation de profit : {self.data.augmentation_profit}", True, (0,0,0)), (0,225)) # Taux de d'augmentation de profit
            self.screen.blit(self.font.render(f"Taux de destruction : {self.data.destruction}", True, (0,0,0)), (0,250)) # Taux de destruction
            self.screen.blit(self.font.render(f"Incendies declares : {self.data.incendie_declaree}", True, (0,0,0)), (0,275)) # Nombre d'incendies déclarés
            self.screen.blit(self.font.render(f"Cases polluees : {self.data.case_polluees}", True, (0,0,0)), (0,300)) # Nombre d'incendies déclarés
            self.screen.blit(self.font.render(f"Arbres brûles : {self.data.arbre_brules}", True, (0,0,0)), (0,325)) # Nombre d'incendies déclarés
            self.screen.blit(self.font.render(f"Usines creees : {self.data.usine_creee}", True, (0,0,0)), (0,350)) # Nombre d'incendies déclarés
            self.screen.blit(self.font.render(f"Desinformation creee : {self.data.desinformation_creee}", True, (0,0,0)), (0,375)) # Nombre d'incendies déclarés
            self.screen.blit(self.font.render(f"Guerres declarees : {self.data.guerre_declaree}", True, (0,0,0)), (0,400)) # Nombre d'incendies déclarés

    def modif_chrono(self):
        texte = str(round(self.chrono, 1)).zfill(5)
        
        for plan in [0, 1]:
            self.dico_UI[plan]["Texte_temps_chrono"].text = texte

    def modif_jauge(self):
        for plan in [0, 1]:
            for jauge in self.dico_UI_anim[plan]["Jauge"].values():
                valeur = getattr(self.data, jauge.nom_data)
                jauge.set_frame(
                    self.converte_data_into_frame(jauge.nbr_frames, valeur)
                )

    def update_cases_brulees(self):
        plan = self.plan

        for key, case in list(self.dico_UI_interact[plan]["CaseBrulee"].items()):
            if case.update(self.meteo):
                del self.dico_UI_interact[plan]["CaseBrulee"][key]

    def save_score(self):

        # Temps survécu
        score["temps"] = round(self.chrono, 3)

        # Stats monde
        score["incendie_declaree"] = self.data.incendie_declaree
        score["case_polluees"] = self.data.case_polluees
        score["arbre_brules"] = self.data.arbre_brules
        score["usine_creee"] = self.data.usine_creee
        score["desinformation_creee"] = self.data.desinformation_creee
        score["guerre_declaree"] = self.data.guerre_declaree

    def run(self):

        self.grille.crea_cases()
        self.return_main_menu = False

        while self.running:

            dt = self.clock.tick(120) / 1000
            self.keys = pygame.key.get_pressed()
            self.fps = int(self.clock.get_fps())

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            if self.plan == -1:

                self.start_game.run()

                if self.start_game.start():
                    self.plan = 0

                if self.start_game.retour():
                    self.running = False

            elif self.plan == 0:

                if self.music_actif == 0:  # musique autorisée
                    self.play_music("sound\music6.mp3")

                self.temps_ecoule += dt
                self.chrono += dt

                self.flamme.update_propagation_feu()
                self.flamme.update_extinction(self.meteo)
                self.pollue.update_propagation_pollue()
                self.pollue.update_extinction(self.meteo)
                self.update_cases_brulees()

                self.data.update_world(dt)

                if self.data.destruction >= 100:
                    self.save_score()
                    self.end_game = EndGame(self.screen)
                    self.end_game.run()
                    self.return_main_menu = True
                    self.running = False
                    
                current_time = pygame.time.get_ticks() / 1000

                for pouvoir in self.pouvoirs.values():
                    result = pouvoir.update(
                        self.dico_UI_interact[0]["Case"],
                        current_time
                    )

                    if result == "activate":
                        if self.pouvoir_actif:
                            self.pouvoir_actif.actif = False

                        self.pouvoir_actif = pouvoir
                        pouvoir.actif = True

                    elif result is True:
                        self.pouvoir_actif = None

                self.notification.update()
                self.modif_jauge()
                self.modif_chrono()
                if self.keys[pygame.K_ESCAPE]:
                    self.plan = 1  # Ceci arrête la boucle principal

            elif self.plan == 1:

                if self.dico_UI_pause[1]["Bouton_Continuer"].mouse_is_click():
                    self.plan = 0

                if self.dico_UI_pause[1]["Bouton_Quitter"].mouse_is_click():
                    self.return_main_menu = False
                    self.running = False

                if self.dico_UI_pause[1]["Bouton_Menu_Principal"].mouse_is_click():
                    self.return_main_menu = True
                    self.running = False

                if self.dico_UI_pause[1]["Bouton_Option"].mouse_is_click():
                    self.plan = 2

            if self.plan == 2:
                self.couper_musique()
                self.couper_son()

            if self.plan in (2,3) and (self.keys[pygame.K_ESCAPE] or self.dico_UI_pause[2]["Retour1"].mouse_is_click()):
                self.plan = 1
                self.sous_plan = 0

            if self.dico_UI_pause[2]["Son"].mouse_is_click():
                self.sous_plan = 1

            self.draw()

        return "hub" if self.return_main_menu else "quit"

    def draw(self):

        self.screen.fill((201, 254, 255))
        if self.plan == -1:

            self.start_game.draw()
            pygame.display.flip()
            return

        # Interfaces
        if self.plan == 0:
            for interfaces in self.dico_UI[0].values():
                interfaces.update()

        else:
            for interfaces in self.dico_UI[0].values():
                interfaces.create()


        # Grille
        if self.plan == 0:
            for case in self.dico_UI_interact[0]["Case"].values():
                case.update()

            for case_brulee in self.dico_UI_interact[0]["CaseBrulee"].values():
                case_brulee.img.update()

        elif self.plan in [1,2,3]:
            for case in self.dico_UI_interact[0]["Case"].values():
                case.create()

            for case_brulee in self.dico_UI_interact[0]["CaseBrulee"].values():
                case_brulee.img.create()

        # Boutons jeu (pas interactifs en pause)
        if self.plan == 0:
            for bouton in self.dico_UI_interact[0]["Bouton"].values():
                bouton.update()
        else:
            for bouton in self.dico_UI_interact[0]["Bouton"].values():
                bouton.create()

        # Jauges
        for anims in self.dico_UI_anim[0].values():
            for anim in anims.values():
                if self.plan == 0:
                    anim.update()
                else:
                    anim.create()

        # Infos jauges (UNIQUEMENT en jeu actif)
        if self.plan == 0:
            for jauge in self.dico_UI_anim[0]["Jauge"].values():
                if jauge.show_info:
                    jauge.info.update()
                    jauge.texte_info.update()
                    jauge.texte_stats_info.update()

        # Animations monde (SEULEMENT en jeu actif)
        if self.plan == 0:
            self.flamme.anim_feu()
            self.pollue.anim_pollue()
            self.condamne.anim_condamne()
            self.usine.anim_usine()

        # Animations principales
        if self.plan == 0:
            self.flamme.animation.update()
            self.usine.animation.update()
            self.pollue.animation.update()
            self.meteo.animation.update()
            self.meteo.update()

        # Pouvoirs (pas de hover en pause)
        for pouvoir in self.pouvoirs.values():
            pouvoir.draw_cooldown(self.screen)

        self.notification.draw()

        self.flamme.animation.draw()
        self.pollue.animation.draw()
        self.usine.animation.draw()
        self.meteo.animation.draw()

        if self.plan == 0:
            if self.pouvoir_actif:
                self.pouvoir_actif.draw_cursor(self.screen)

            for pouvoir in self.pouvoirs.values():
                pouvoir.hover_info()
                pouvoir.draw_info()

        if self.plan in [1,2,3]:

            # Overlay grisé
            self.screen.blit(self.ecran_noir, (0, 0))

            # Boutons pause (les seuls interactifs)
            for objet in self.dico_UI_pause[self.plan].values():
                objet.update()

            for setting in self.setting_UI[self.sous_plan].values(): # Si on est dans les settings, on update les objets paramètriques
                setting.update()

        # Stats en dernier
        self.stats()

        pygame.display.flip()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
    Long = screen_taille.current_w # On récupère la longueur de l'écran
    larg = screen_taille.current_h # On récupère la hauteur de l'écran

    BASE_DIR = os.path.dirname(__file__)
    ICON_PATH = os.path.join(BASE_DIR, "sprite", "icon.png")
    icon = pygame.image.load(ICON_PATH)

    screen = pygame.display.set_mode((Long, larg), pygame.FULLSCREEN) # On initialise l'écran avec les dimensions préalablement récupérer
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre

    game = Game(screen)
    game.run()