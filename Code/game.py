import pygame
from pygame.locals import QUIT
from random import randint, random
from PIL import Image
import os
from ui_tools import *
from jauge import *
from data import *

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
        }

        # Gestion des types de cases
        self.CASES_E_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_eau", "sprite_eau_")
        self.CASES_H_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_herbe", "sprite_herbe_")
        self.CASES_Fo_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_foret", "sprite_foret_")
        self.CASES_Fe_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_feu", "sprite_feu_")
        self.CASES_P_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_pollue", "sprite_pollue_")
        self.CASES_In_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_condamne", "sprite_condamne_")
        self.type_cases = {
            (0,0,255) : [f"{self.CASES_E_PATH}{i}.png" for i in range(4)],
            (0,255,0) : [f"{self.CASES_H_PATH}{i}.png" for i in range(4)],
            (0,50,0) : [f"{self.CASES_Fo_PATH}{i}.png" for i in range(4)],
            "Case ETDB" : [f"{self.CASES_Fe_PATH}{i}.png" for i in range(5)],
            "Case pollue" : [f"{self.CASES_P_PATH}{i}.png" for i in range(3)],
            "Case brulee" : "",
            "Terre inutilisable": [f"{self.CASES_In_PATH}{i}.png" for i in range(7)],
        }
        
        self.data = Data()

        # Variable affichage
        # Num plan : {0:grille, 1:?}
        self.plan = 0

        # Gestion du nombre de cases
        self.lignes = 19
        self.colonnes = 30
        self.marge = 3.5  # marge entre les cases
        self.rect_zone = self.resp(
            self.ratio_objet["Rect_bouton"][0],
            self.ratio_objet["Rect_bouton"][1],
            self.ratio_objet["Rect_bouton"][2],
            self.ratio_objet["Rect_bouton"][3]
        )
        self.zone_x, self.zone_y, self.zone_L, self.zone_l = self.rect_zone
        self.case_Long = (self.zone_L - (self.colonnes + 1) * self.marge) / self.colonnes
        self.case_larg = (self.zone_l - (self.lignes + 1) * self.marge) / self.lignes

        self.grille = [["terre" for i in range(self.colonnes)] for j in range(self.lignes)]

        self.file_propagation = []  # [(ligne, colonne, puissance)]
        self.last_fire_update = pygame.time.get_ticks()
        self.fire_delay = 1200  # ms entre chaque vague

        self.RAIN_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_effet_pluie", "sprite_pluie_")
        self.sprite_pluie = [pygame.image.load(f"{self.RAIN_PATH}{str(i).zfill(2)}.png").convert() for i in range(23)] # Importation des 23 frames
        self.sprite_pluie = [pygame.transform.scale(elt, (self.zone_L, self.zone_l)) for elt in self.sprite_pluie] # Convertion des frames pour la grille
        self.last_rain_update = pygame.time.get_ticks()
        self.pluie_frame = 0        

        # Gestion des éléments graphiques non intéractif
        self.dico_UI = {
            0:{
                "Rect_bouton" : UI_screen(self.screen, (88, 41, 0), (255,255,255), self.rect_zone, taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_jauge" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp(self.ratio_objet["Rect_jauge"][0], self.ratio_objet["Rect_jauge"][1], self.ratio_objet["Rect_jauge"][2], self.ratio_objet["Rect_jauge"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_stats" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp(self.ratio_objet["Rect_stats"][0], self.ratio_objet["Rect_stats"][1], self.ratio_objet["Rect_stats"][2], self.ratio_objet["Rect_stats"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_notif" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp(self.ratio_objet["Rect_notif"][0], self.ratio_objet["Rect_notif"][1], self.ratio_objet["Rect_notif"][2], self.ratio_objet["Rect_notif"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Rect_power" : UI_screen(self.screen, (0, 100, 127), (255,255,255), self.resp(self.ratio_objet["Rect_power"][0], self.ratio_objet["Rect_power"][1], self.ratio_objet["Rect_power"][2], self.ratio_objet["Rect_power"][3]), taille_contour = 6, border_radius = 12, pulse = True),
                "Texte_temps_chrono" : Texte(self.screen, self.resp_text(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][1]), self.resp_font(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][2]), (0,0,0), f"{self.temps_ecoule}", font_type = "font/pixellari.ttf")
            },
        }

        # Gestion des éléments intéractifs
        self.dico_UI_interact = {
            0:{
                
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
                    "Jauge_pollution" : Jauge(self.screen, self.JAUGE_POLLUTION_PATH, "pollution", self.resp(self.ratio_objet["Jauge_pollution"][0], self.ratio_objet["Jauge_pollution"][1], self.ratio_objet["Jauge_pollution"][2], self.ratio_objet["Jauge_pollution"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.pollution)),
                    "Jauge_bio" : Jauge(self.screen, self.JAUGE_BIO_PATH, "biodiversite", self.resp(self.ratio_objet["Jauge_bio"][0], self.ratio_objet["Jauge_bio"][1], self.ratio_objet["Jauge_bio"][2], self.ratio_objet["Jauge_bio"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.biodiversite)),
                    "Jauge_niv_ocean" : Jauge(self.screen, self.JAUGE_NIV_OCEAN_PATH, "eau", self.resp(self.ratio_objet["Jauge_niv_ocean"][0], self.ratio_objet["Jauge_niv_ocean"][1], self.ratio_objet["Jauge_niv_ocean"][2], self.ratio_objet["Jauge_niv_ocean"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.eau)),
                    "Jauge_social" : Jauge(self.screen, self.JAUGE_SOCIAL_PATH, "stabilite", self.resp(self.ratio_objet["Jauge_social"][0], self.ratio_objet["Jauge_social"][1], self.ratio_objet["Jauge_social"][2], self.ratio_objet["Jauge_social"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.stabilite)),
                    "Jauge_temp" : Jauge(self.screen, self.JAUGE_TEMP_PATH, "temperature", self.resp(self.ratio_objet["Jauge_temp"][0], self.ratio_objet["Jauge_temp"][1], self.ratio_objet["Jauge_temp"][2], self.ratio_objet["Jauge_temp"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.temperature)),
                    "Jauge_nourriture" : Jauge(self.screen, self.JAUGE_NOURRITURE_PATH, "profit", self.resp(self.ratio_objet["Jauge_nourriture"][0], self.ratio_objet["Jauge_nourriture"][1], self.ratio_objet["Jauge_nourriture"][2], self.ratio_objet["Jauge_nourriture"][3]), 7, 0.03, self.converte_data_into_frame(7, self.data.profit)),
                    "Jauge_total" : Jauge(self.screen, self.JAUGE_TOTAL_PATH, "destruction", self.resp(self.ratio_objet["Jauge_total"][0], self.ratio_objet["Jauge_total"][1], self.ratio_objet["Jauge_total"][2], self.ratio_objet["Jauge_total"][3]), 7, 0.03, self.converte_data_into_frame(11, self.data.destruction), "0", nbr_frames = 11)
                },
            }
        }

    def converte_data_into_frame(self, nbr_frame, valeur_reel):
        valeur_reel = max(0, min(100, valeur_reel))
        return round((valeur_reel / 100) * (nbr_frame - 1))


    def resp(self, ratio_x:float, ratio_y:float, ratio_long:float, ratio_larg:float):
        '''Méthode qui gère la responsive des surfaces comme les boutons, les interfaces ou les champs'''
        # On convertit tout les éléments par rapport à un ratio et à la taille de l'écran
        x = self.Long * ratio_x
        y = self.larg * ratio_y
        L = self.Long * ratio_long
        l = self.larg * ratio_larg
        return (x, y, L, l)
    
    def placement_grille(self, ligne:int, colonne:int):
        x = self.zone_x + self.marge + ligne * (self.case_Long + self.marge)
        y = self.zone_y + self.marge +  colonne * (self.case_larg + self.marge)
        return x, y
    
    def crea_cases(self):
        # Création des cases
        index = 0
        for lignes in range(self.lignes):
            for colonnes in range(self.colonnes):
                x, y = self.placement_grille(colonnes, lignes)
                color = self.color_pixel_map("sprite/map.png", colonnes, lignes)
                self.dico_UI_interact[0][index] = UI_PNG(self.screen, self.type_cases[color][randint(0,3)], (x, y, self.case_Long, self.case_larg), 5, 0.03)
                self.grille[lignes][colonnes] = color
                index += 1

    def pluie(self):
        now = pygame.time.get_ticks()
        rain_delay = 50 # ms

        if now - self.last_rain_update >= rain_delay:
            self.pluie_frame = (self.pluie_frame + 1) % len(self.sprite_pluie)
            self.last_rain_update = now

        image = self.sprite_pluie[self.pluie_frame]
        image.set_alpha(155)  # Change l'opacité ici

        self.screen.blit(image, (self.zone_x, self.zone_y))
            

    def ajout_feu(self, ligne, colonne):
        x, y = self.placement_grille(colonne, ligne)

        flamme = UI_PNG(
            self.screen,
            self.type_cases["Case ETDB"][0],
            (x, y, self.case_Long, self.case_larg),
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
                flamme.frame = (flamme.frame + 1) % len(self.type_cases["Case ETDB"])
                flamme.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                flamme.IMG_PATH = self.type_cases["Case ETDB"][flamme.frame]
                flamme.img_base = pygame.image.load(
                    flamme.IMG_PATH
                ).convert_alpha()

    def ajout_condamne(self, ligne, colonne):
        x, y = self.placement_grille(colonne, ligne)

        croix = UI_PNG(
            self.screen,
            self.type_cases["Terre inutilisable"][0],
            (x, y, self.case_Long, self.case_larg),
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
                croix.frame = (croix.frame + 1) % len(self.type_cases["Terre inutilisable"])
                croix.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                croix.IMG_PATH = self.type_cases["Terre inutilisable"][croix.frame]
                croix.img_base = pygame.image.load(
                    croix.IMG_PATH
                ).convert_alpha()

    def ajout_pollue(self, ligne, colonne):
        x, y = self.placement_grille(colonne, ligne)

        poubelle = UI_PNG(
            self.screen,
            self.type_cases["Case pollue"][0],
            (x, y, self.case_Long, self.case_larg),
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
                poubelle.frame = (poubelle.frame + 1) % len(self.type_cases["Case pollue"])
                poubelle.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                poubelle.IMG_PATH = self.type_cases["Case pollue"][poubelle.frame]
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

        if not (0 <= ligne < self.lignes and 0 <= colonne < self.colonnes):
            return

        if puissance <= 0:
            return

        if self.grille[ligne][colonne] in [(0,0,255), "feu"]:
            return

        self.grille[ligne][colonne] = "feu"
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
    
    def resp_text(self, ratio_x:float, ratio_y:float):
        '''
        Méthode qui gère la responsive des positions des textes à partir d'un ratio x et y
        '''
        return (self.Long * ratio_x, self.larg * ratio_y)
    
    def resp_font(self, ratio_long:float, ratio_font:float):
        '''
        Méthode qui gère la responsive des tailles de polices d'écriture en fonction de la 
        longueur d'une surface
        '''
        return int(self.Long * ratio_long * ratio_font)
    
    def color_pixel_map(self, fichier:str, x:int, y:int):
        IMG_PATH = os.path.join(self.BASE_DIR, fichier)
        img = Image.open(IMG_PATH).convert("RGBA")  # RGBA recommandé
        pixels = img.load()

        # Lire un pixel
        r, g, b, a = pixels[x, y]
        return r,g,b

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
            self.screen.blit(self.font.render(f"Taux de destruction : {self.data.destruction}", True, (0,0,0)), (0,225)) # Taux de destruction

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
        self.crea_cases()
        self.propagation_feu(6, 4, self.puissance_feu())
        while self.running:
            diff_entre_frame = self.clock.tick(60) / 1000
            self.keys = pygame.key.get_pressed()

            self.temps_ecoule += diff_entre_frame
            self.fps = int(self.clock.get_fps())

            self.data.update_world(diff_entre_frame)
            self.update_propagation_feu()
            self.modif_jauge()
            self.modif_chrono()

            self.draw()
            self.exit()
        pygame.quit() # Puis on quitte proprement le jeu

    def draw(self):
        '''
        Cette méthode gère tout les affichages d'objets à l'écran ainsi que le rafraichissement de celui-ci
        '''
        self.screen.fill((71, 169, 215))  # Si on est dans le plan secret alors on affiche un arrière plan noir 
        
        for interfaces in self.dico_UI[self.plan].values():
            interfaces.update()  

        for cases in self.dico_UI_interact[self.plan].values():
            cases.update()  

        # Dessiner toutes les jauges
        for anims in self.dico_UI_anim[self.plan].values():
            for anim in anims.values():
                anim.update()

        # Puis dessiner les tooltips EN DERNIER
        for jauge in self.dico_UI_anim[self.plan]["Jauge"].values():
            if jauge.show_info:
                jauge.info.update()

        self.anim_feu() 
        self.anim_condamne() 
        self.anim_pollue()
        self.pluie()

        self.stats()  # On gère l'affichage des stats

        # Rafraîchissement de l'écran
        pygame.display.flip()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    hub = Game()
    hub.run()