import pygame
from pygame.locals import QUIT
from random import randint
from PIL import Image
import os
from ui_tools import *

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
        self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000 # Temps écoulé en secondes

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
            "Texte_temps_chrono": (0.782, 0.06, 0.06),
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
        self.nbr_eau = 0
        self.nbr_herbe = 0
        self.nbr_foret = 0

        # Variable affichage
        # Num plan : {0:grille, 1:?}
        self.plan = 0

        # Gestion du nombre de cases
        self.lignes = 19
        self.colonnes = 30
        self.marge = 4  # marge entre les cases
        self.rect_zone = self.resp(
            self.ratio_objet["Rect_bouton"][0],
            self.ratio_objet["Rect_bouton"][1],
            self.ratio_objet["Rect_bouton"][2],
            self.ratio_objet["Rect_bouton"][3]
        )
        self.zone_x, self.zone_y, self.zone_L, self.zone_l = self.rect_zone
        self.case_Long = (self.zone_L - (self.colonnes + 1) * self.marge) / self.colonnes
        self.case_larg = (self.zone_l - (self.lignes + 1) * self.marge) / self.lignes
        

        # Gestion des éléments graphiques non intéractif
        self.dico_UI = {
            0:{
                "Rect_bouton" : UI_screen(self.screen, (88, 41, 0), (255,255,255), self.rect_zone, taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_jauge" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp(self.ratio_objet["Rect_jauge"][0], self.ratio_objet["Rect_jauge"][1], self.ratio_objet["Rect_jauge"][2], self.ratio_objet["Rect_jauge"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Rect_stats" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp(self.ratio_objet["Rect_stats"][0], self.ratio_objet["Rect_stats"][1], self.ratio_objet["Rect_stats"][2], self.ratio_objet["Rect_stats"][3]), taille_contour = 6, border_radius = 12, pulse = False),
                "Texte_temps_chrono" : Texte(self.screen, self.resp_text(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][1]), self.resp_font(self.ratio_objet["Texte_temps_chrono"][0], self.ratio_objet["Texte_temps_chrono"][2]), (0,0,0), f"Temps de {self.temps_ecoule}", font_type = "font/pixellari.ttf")
            },
        }

        # Gestion des éléments intéractifs
        self.dico_UI_interact = {
            0:{
                
            },
        }

        # Gestion des éléments en animations
        self.dico_UI_anim = {
            0:{
                "Flamme" : {
                },
                "Croix" : {
                },
                "Poubelle" : {
                },
            }
        }

        

    def resp(self, ratio_x:float, ratio_y:float, ratio_long:float, ratio_larg:float):
        '''Méthode qui gère la responsive des surfaces comme les boutons, les interfaces ou les champs'''
        # On convertit tout les éléments par rapport à un ratio et à la taille de l'écran
        x = self.Long * ratio_x
        y = self.larg * ratio_y
        L = self.Long * ratio_long
        l = self.larg * ratio_larg
        return (x, y, L, l)
    
    def placement_grille(self, colonne:int, ligne:int):
        x = self.zone_x + self.marge + ligne * (self.case_Long + self.marge)
        y = self.zone_y + self.marge +  colonne * (self.case_larg + self.marge)
        return x, y
    
    def crea_cases(self):
        # Création des cases
        index = 0
        for lignes in range(self.lignes):
            for colonnes in range(self.colonnes):
                x, y = self.placement_grille(lignes, colonnes)
                color = self.color_pixel_map("sprite/map.png", colonnes, lignes)
                self.dico_UI_interact[0][index] = UI_PNG(self.screen, self.type_cases[color][randint(0,3)], (x, y, self.case_Long, self.case_larg), 5, 0.03)
                index += 1

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
            self.screen.blit(self.font.render(f"FPS : {self.fps}", True, (0,0,0)), (0,0)) # Numéro plan
            self.screen.blit(self.font.render(f"Timer : {self.temps_ecoule}", True, (0,0,0)), (0,25)) # Numéro plan
            self.screen.blit(self.font.render(f"Num de plan : {self.plan}", True, (0,0,0)), (0,50)) # Numéro plan
            self.screen.blit(self.font.render(f"Nbr cases eau : {self.nbr_eau}", True, (0,0,0)), (0,75)) # Numéro plan
            self.screen.blit(self.font.render(f"Nbr cases herbe : {self.nbr_herbe}", True, (0,0,0)), (0,100)) # Numéro plan
            self.screen.blit(self.font.render(f"Nbr cases forêt : {self.nbr_foret}", True, (0,0,0)), (0,125)) # Numéro plan

    def run(self):
        '''
        Cette méthode enclenche la boucle principale du menu en appelant toutes les méthodes utiles à 
        son fonctionnement
        '''
        self.crea_cases()
        self.ajout_feu(2,2)
        self.ajout_feu(6,7)
        self.ajout_condamne(8,7)
        self.ajout_condamne(10,7)
        while self.running:
            self.keys = pygame.key.get_pressed()  # On récupère les touches enclenchées
            self.clock.tick(60)  # On paramètre le tick soit les fps max de la boucle (ici 60fps)
            self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000  # On récupère le temps réel
            self.fps = int(self.clock.get_fps())  # On récupère les fps en temps réel
            self.draw()  # On affiche les éléments graphiques
            self.exit()  # On test si une condition d'arrêt est déclenchée
    
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

        for anims in self.dico_UI_anim[self.plan].values():
            for anim in anims.values():
                anim.update()  

        self.anim_feu() 
        self.anim_condamne() 

        self.stats()  # On gère l'affichage des stats

        # Rafraîchissement de l'écran
        pygame.display.flip()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    hub = Game()
    hub.run()