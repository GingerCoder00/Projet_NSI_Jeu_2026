import pygame
from random import randint, random
from PIL import Image
import os
from ui_tools import *
from jauge import *
from data import *
from meteo import *
from resp_tools import *
from grille import *
from dico_info_game import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

class Game:
    '''Classe qui gère le Hub du Jeu'''
    def __init__(self):
        self.screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
        self.Long = self.screen_taille.current_w # On récupère la longueur de l'écran
        self.larg = self.screen_taille.current_h # On récupère la hauteur de l'écran

        self.BASE_DIR = os.path.dirname(__file__)

        self.screen = pygame.display.set_mode((self.Long, self.larg)) # On initialise l'écran avec les dimensions préalablement récupérer
        pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre

        # Gestion du temps
        self.start_time = pygame.time.get_ticks()  # Temps de départ après l'initialisation de pygame
        self.clock = pygame.time.Clock() # Initialisation de l'horloge interne du jeu
        self.temps_ecoule = 0

        # Gestion du texte et importation de la police
        FONT_PATH = os.path.join(self.BASE_DIR, "font", "sans_sherif.otf")
        self.font = pygame.font.Font(FONT_PATH, 20)

        # Active et désactive la boucle de jeu
        self.running = True

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
            "Bouton_Feu": (0.45, 0.83, 0.055, 0.08)
        }

        self.dico_info = Dico_info_Game()

        self.fire_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case ETDB"]]

        # Variable affichage
        # Num plan : {0:grille, 1:?}
        self.plan = 0

        self.file_propagation = []  # [(ligne, colonne, puissance)]
        self.last_fire_update = pygame.time.get_ticks()
        self.fire_delay = 1200  # ms entre chaque vague
       
        self.BOUTON_FEU_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_bouton_feu", "sprite_bouton_feu_0.png")
        self.bouton_active = False

        self.data = Data()

        # Gestion des éléments intéractifs
        self.dico_UI_interact = {
            0:{
                "Case" : {

                },
                "Bouton" : {
                    "Bouton_Feu" : UI_PNG(self.screen, self.BOUTON_FEU_PATH, self.resp.resp(self.ratio_objet["Bouton_Feu"][0], self.ratio_objet["Bouton_Feu"][1], self.ratio_objet["Bouton_Feu"][2], self.ratio_objet["Bouton_Feu"][3]), 12, 0.03) 
                },
            },
        }

        self.grille = Grille(self.screen, 19, 30, 3.5, self.resp.resp(self.ratio_objet["Rect_bouton"][0], self.ratio_objet["Rect_bouton"][1], self.ratio_objet["Rect_bouton"][2], self.ratio_objet["Rect_bouton"][3]), self.dico_UI_interact)
        self.meteo = Meteo(self.screen, self.grille.zone_x, self.grille.zone_y, self.grille.zone_L, self.grille.zone_l)

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
        }

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
                "Croix" : {
                },
                "Poubelle" : {
                },
                "Jauge" : {
                    "Jauge_pollution" : Jauge(self.screen, self.JAUGE_POLLUTION_PATH, "pollution", self.resp.resp(self.ratio_objet["Jauge_pollution"][0], self.ratio_objet["Jauge_pollution"][1], self.ratio_objet["Jauge_pollution"][2], self.ratio_objet["Jauge_pollution"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.pollution)),
                    "Jauge_bio" : Jauge(self.screen, self.JAUGE_BIO_PATH, "biodiversite", self.resp.resp(self.ratio_objet["Jauge_bio"][0], self.ratio_objet["Jauge_bio"][1], self.ratio_objet["Jauge_bio"][2], self.ratio_objet["Jauge_bio"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.biodiversite)),
                    "Jauge_niv_ocean" : Jauge(self.screen, self.JAUGE_NIV_OCEAN_PATH, "eau", self.resp.resp(self.ratio_objet["Jauge_niv_ocean"][0], self.ratio_objet["Jauge_niv_ocean"][1], self.ratio_objet["Jauge_niv_ocean"][2], self.ratio_objet["Jauge_niv_ocean"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.eau)),
                    "Jauge_social" : Jauge(self.screen, self.JAUGE_SOCIAL_PATH, "stabilite", self.resp.resp(self.ratio_objet["Jauge_social"][0], self.ratio_objet["Jauge_social"][1], self.ratio_objet["Jauge_social"][2], self.ratio_objet["Jauge_social"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.stabilite)),
                    "Jauge_temp" : Jauge(self.screen, self.JAUGE_TEMP_PATH, "temperature", self.resp.resp(self.ratio_objet["Jauge_temp"][0], self.ratio_objet["Jauge_temp"][1], self.ratio_objet["Jauge_temp"][2], self.ratio_objet["Jauge_temp"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.temperature)),
                    "Jauge_nourriture" : Jauge(self.screen, self.JAUGE_NOURRITURE_PATH, "profit", self.resp.resp(self.ratio_objet["Jauge_nourriture"][0], self.ratio_objet["Jauge_nourriture"][1], self.ratio_objet["Jauge_nourriture"][2], self.ratio_objet["Jauge_nourriture"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.profit)),
                    "Jauge_total" : Jauge(self.screen, self.JAUGE_TOTAL_PATH, "destruction", self.resp.resp(self.ratio_objet["Jauge_total"][0], self.ratio_objet["Jauge_total"][1], self.ratio_objet["Jauge_total"][2], self.ratio_objet["Jauge_total"][3]), 7, 0.03, self.converte_data_into_frame(11, self.data.destruction), "0", nbr_frames = 11)
                },
            }
        }

    def converte_data_into_frame(self, nbr_frame, valeur_reel):
        valeur_reel = max(0, min(100, valeur_reel))
        return round((valeur_reel / 100) * (nbr_frame - 1))

    def ajout_feu(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        flamme = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Case ETDB"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            5, 0
        )

        flamme.frame = 0
        flamme.last_update = pygame.time.get_ticks()

        self.dico_UI_anim[0]["Flamme"][len(self.dico_UI_anim[0]["Flamme"])] = flamme

    def anim_feu(self):
        FRAME_DELAY = 120  # ms
        now = pygame.time.get_ticks()

        for flamme in self.dico_UI_anim[self.plan]["Flamme"].values():
            if now - flamme.last_update >= FRAME_DELAY:
                flamme.frame = (flamme.frame + 1) % len(self.dico_info.type_cases["Case ETDB"])
                flamme.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                flamme.img_base = self.fire_frames[flamme.frame]

    def ajout_condamne(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        croix = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Terre inutilisable"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            5, 0
        )

        croix.frame = 0
        croix.last_update = pygame.time.get_ticks()

        self.dico_UI_anim[0]["Croix"][len(self.dico_UI_anim[0]["Croix"])] = croix

    def anim_condamne(self):
        FRAME_DELAY = 120  # ms
        now = pygame.time.get_ticks()

        for croix in self.dico_UI_anim[self.plan]["Croix"].values():
            if now - croix.last_update >= FRAME_DELAY:
                croix.frame = (croix.frame + 1) % len(self.dico_info.type_cases["Terre inutilisable"])
                croix.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                croix.IMG_PATH = self.dico_info.type_cases["Terre inutilisable"][croix.frame]
                croix.img_base = pygame.image.load(
                    croix.IMG_PATH
                ).convert_alpha()

    def ajout_pollue(self, ligne, colonne):
        x, y = self.placement_grille(colonne, ligne)

        poubelle = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Case pollue"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            5, 0
        )

        poubelle.frame = 0
        poubelle.last_update = pygame.time.get_ticks()

        self.dico_UI_anim[0]["Poubelle"][len(self.dico_UI_anim[0]["Poubelle"])] = poubelle

    def anim_pollue(self):
        FRAME_DELAY = 120  # ms
        now = pygame.time.get_ticks()

        for poubelle in self.dico_UI_anim[self.plan]["Poubelle"].values():
            if now - poubelle.last_update >= FRAME_DELAY:
                poubelle.frame = (poubelle.frame + 1) % len(self.dico_info.type_cases["Case pollue"])
                poubelle.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                poubelle.IMG_PATH = self.dico_info.type_cases["Case pollue"][poubelle.frame]
                poubelle.img_base = pygame.image.load(
                    poubelle.IMG_PATH
                ).convert_alpha()

    def proba_propagation(self):
        """
        Retourne une probabilité entre 0 et 1
        dépendante de la température
        """

        # Base minimale
        base = 0.15  

        # Influence température (0 → 100)
        influence = self.data.temperature / 150  

        # Limite max
        return min(0.85, base + influence)
    
    def puissance_feu(self):
        '''
        Détermine la profondeur de propagation
        '''
        return 4 + int(self.data.temperature / 25)

    def propagation_feu(self, ligne, colonne, puissance):

        if not (0 <= ligne < self.grille.lignes and 0 <= colonne < self.grille.colonnes):
            return

        if puissance <= 0:
            return

        if self.grille.grille[ligne][colonne] in [(0,0,255), "feu"]:
            return

        self.grille.grille[ligne][colonne] = "feu"
        self.ajout_feu(ligne, colonne)

        proba = self.proba_propagation()

        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        for dl, dc in directions:
            if random() < proba:
                self.file_propagation.append(
                    (ligne + dl, colonne + dc, puissance - 1)
                )

    def update_propagation_feu(self):
        now = pygame.time.get_ticks()

        if now - self.last_fire_update < self.fire_delay:
            return

        self.last_fire_update = now

        # On prend une vague complète
        vague = self.file_propagation.copy()
        self.file_propagation.clear()

        for ligne, colonne, puissance in vague:
            self.propagation_feu(ligne, colonne, puissance)

    def resp_cases(self, ratio_x:float, ratio_y:float, ratio_long:float, ratio_larg:float):
        '''Méthode qui gère la responsive des cases sur la grille'''
        # On convertit tout les éléments par rapport à un ratio et à la taille de la zone des cases
        x = self.ratio_objet["Rect_bouton"][0] * ratio_x
        y = self.ratio_objet["Rect_bouton"][1] * ratio_y
        L = self.ratio_objet["Rect_bouton"][0] * ratio_long
        l = self.ratio_objet["Rect_bouton"][1] * ratio_larg
        return (x, y, L, l)

    def exit(self):
        '''Gère la fermeture de la fenêtre'''
        # On récupère tous les évènements pour vérifier si il y a un événement de type : pygame.QUIT
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Ceci arrête la boucle principal

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False  # Ceci arrête la boucle principal
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
            self.screen.blit(self.font.render(f"Taux de d'augmentation de profit : {self.data.augmentation_profil}", True, (0,0,0)), (0,225)) # Taux de d'augmentation de profit
            self.screen.blit(self.font.render(f"Taux de destruction : {self.data.destruction}", True, (0,0,0)), (0,250)) # Taux de destruction

    def modif_chrono(self):
        self.dico_UI[0]["Texte_temps_chrono"].text = str(round(self.temps_ecoule, 1))

    def modif_jauge(self):
        for jauge in self.dico_UI_anim[0]["Jauge"].values():

            # On récupère la valeur correspondante dans Data
            valeur = getattr(self.data, jauge.nom_data)

            # On convertit en frame
            jauge.set_frame(self.converte_data_into_frame(jauge.nbr_frames, valeur))

    def run(self):
        '''
        Cette méthode enclenche la boucle principale du menu en appelant toutes les méthodes utiles à 
        son fonctionnement
        '''
        self.grille.crea_cases()
        while self.running:
            diff_entre_frame = self.clock.tick(60) / 1000
            self.keys = pygame.key.get_pressed()

            self.temps_ecoule += diff_entre_frame
            self.fps = int(self.clock.get_fps())

            self.data.update_world(diff_entre_frame)
            self.handle_event_bouton_feu()
            self.update_propagation_feu()
            self.modif_jauge()
            self.modif_chrono()

            self.draw()
            self.exit()
        pygame.quit() # Puis on quitte proprement le jeu

    def handle_event_bouton_feu(self):
        # Activation / désactivation du bouton
        if self.dico_UI_interact[self.plan]["Bouton"]["Bouton_Feu"].mouse_is_click():
            self.bouton_active = True

        # Si le bouton n'est pas actif, on arrête
        if not self.bouton_active:
            return

        # Si bouton actif → on attend un clic sur une case
        for index, cases in self.dico_UI_interact[self.plan]["Case"].items():
            if cases.mouse_is_click() and self.data.utiliser_pouvoir("incendie"):
                ligne = index // self.grille.colonnes
                colonne = index % self.grille.colonnes
                self.propagation_feu(ligne, colonne, self.puissance_feu())
                # Désactivation immédiate après 1 clic
                self.bouton_active = False

    def draw(self):
        '''
        Cette méthode gère tout les affichages d'objets à l'écran ainsi que le rafraichissement de celui-ci
        '''
        self.screen.fill((71, 169, 215))  # Si on est dans le plan secret alors on affiche un arrière plan noir 
        
        for interfaces in self.dico_UI[self.plan].values():
            interfaces.update()  

        for cases in self.dico_UI_interact[self.plan]["Case"].values():
            cases.update() 

        for objet in self.dico_UI_interact[self.plan]["Bouton"].values():
            objet.update()  

        # Dessiner toutes les jauges
        for anims in self.dico_UI_anim[self.plan].values():
            for anim in anims.values():
                anim.update()

        # Puis dessiner les infos
        for jauge in self.dico_UI_anim[self.plan]["Jauge"].values():
            if jauge.show_info:
                jauge.info.update()
                jauge.texte_info.update()

        self.anim_feu() 
        self.anim_condamne() 
        self.anim_pollue()
        self.meteo.pluie()
        self.stats()  # On gère l'affichage des stats

        # Rafraîchissement de l'écran
        pygame.display.flip()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    hub = Game()
    hub.run()