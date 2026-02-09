import pygame
import os
from pygame.locals import QUIT
from random import randint
from ui_tools import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

class Hub:
    '''Classe qui gère le Hub du Jeu'''
    def __init__(self):

        # Gestion de l'écran
        self.screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
        self.Long = self.screen_taille.current_w # On récupère la longueur de l'écran
        self.larg = self.screen_taille.current_h # On récupère la hauteur de l'écran

        self.screen = pygame.display.set_mode((self.Long, self.larg)) # On initialise l'écran avec les dimensions préalablement récupérer
        pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre
        BASE_DIR = os.path.dirname(__file__)

        # Gestion du temps
        self.start_time = pygame.time.get_ticks()  # Temps de départ après l'initialisation de pygame
        self.clock = pygame.time.Clock() # Initialisation de l'horloge interne du jeu

        # Gestion du texte et importation de la police
        FONT_PATH = os.path.join(BASE_DIR, "font", "font_retro.ttf")
        self.font = pygame.font.Font(FONT_PATH, 20)

        # Gestion des ratios de chaques objets graphiques pour la responsive
        self.ratio_objet = {
            # Plan 0
            "Jouer" : (0.375, 0.68, 0.25, 0.15, 0.28),
            "Option" : (0.15, 0.71, 0.20, 0.10, 0.22),
            "Quitter" : (0.65, 0.71, 0.20, 0.10, 0.218),
            "Credit" : (0.02, 0.93, 0.07, 0.05, 0.215),
            "Aide" : (0.94, 0.02, 0.05, 0.08, 0.7),
            "Logo_jeu" : (0.305, 0.02, 0.37, 0.37),

            # Plan 1
            "Retour1" : (0.73, 0.22, 0.12, 0.07, 0.215),
            "Settings" : (0.125, 0.19, 0.75, 0.65),
            "Settings_select" : (0.14, 0.21, 0.20, 0.61),
            "Settings_modif" : (0.36, 0.39, 0.5, 0.43),
            "Son" : (0.165, 0.27, 0.15, 0.07, 0.215),
            "Ecran" : (0.165, 0.39, 0.15, 0.07, 0.215),
            "Secret" : (0.165, 0.5, 0.15, 0.07, 0.215),
            "Couper_Son": (0.4, 0.5, 0.1, 0.2),
            "Couper_Music": (0.55, 0.5, 0.1, 0.2),
            "Text_setting" : (0.37, 0.25, 0.1775),
            "Champ_secret" : (0.38, 0.43, 0.455, 0.1),

            # Plan 2
            "Retour2" : (0.71, 0.22, 0.12, 0.07, 0.215),
            "Rect_Credit" : (0.15, 0.19, 0.7, 0.6),
            "Text_credit" : (0.37, 0.23, 0.205),

            # Plan 3
            "Retour3" : (0.562, 0.08, 0.12, 0.07, 0.215),
            "Rect_Aide" : (0.3, 0.05, 0.4, 0.9),
            "Rect_Aide_Bloc" : (0.335, 0.22, 0.33, 0.70),
            "Text_aide" : (0.35, 0.07, 0.22),
            "Text_bloc_aide" : (0.35, 0.3, 0.06),

            # Plan 4
            "Text_secret" : (0.2, 0.5, 0.23),
        }

        # Active et désactive la boucle de jeu
        self.running = True

        # Variable affichage
        # num plan : {0:menu, 1:option, 2:credit, 3:aide, 4:secret}
        self.plan = 0
        self.sous_plan = 0

        # Importation des sprites complémentaires
        WALL_PATH = os.path.join(BASE_DIR, "sprite", "wallpaper5_v2", "wall2_")
        self.background = [pygame.image.load(f"{WALL_PATH}{i}.png").convert() for i in range(7)] # Importation des 7 frames
        self.background = [pygame.transform.scale(elt, (self.Long, self.larg)) for elt in self.background] # Convertion des frames pour l'écran
        LOGO_PATH = os.path.join(BASE_DIR, "sprite", "logo_jeu1.png")
        self.logo = pygame.image.load(LOGO_PATH).convert_alpha() # Importation du logo
        self.logo = pygame.transform.scale(self.logo, (self.Long * self.ratio_objet["Logo_jeu"][2], self.Long * self.ratio_objet["Logo_jeu"][3]) )# Convertion du logo

        # Gestion des bruitages et de la musique
        self.son_off_on = ["son_on_off/son_on.png", "son_on_off/son_off.png"]
        #self.flag_son = True # Permet de ne pas lancer le son en boucle et de vérifier si il est bien lancé
        self.son_actif = 0 # A comme rôle un indice dans le tableau self.son_off_on

        self.music_off_on = ["music_on_off/music_on.png", "music_on_off/music_off.png"]
        #self.flag_music = True # Pareil que pour les sons
        self.music_actif = 0 # A comme rôle un indice dans le tableau self.music_off_on
        self.current_music = None

        # Gestion de l'animation de l'arrière plan
        self.frame = 0 # A comme rôle un indice dans self.background
        self.last_frame_change = pygame.time.get_ticks() # Permet de changer de frames à intervales régulier
        
        # Gestion des éléments intéractifs
        self.dico_UI_interact = {
            0:{
                "Jouer" : UI_Bouton(self.screen, (58, 137, 35), (190, 245, 116), self.resp_font(self.ratio_objet["Jouer"][2], self.ratio_objet["Jouer"][4]), self.resp(self.ratio_objet["Jouer"][0], self.ratio_objet["Jouer"][1], self.ratio_objet["Jouer"][2], self.ratio_objet["Jouer"][3]), "JOUER", 4, 12, 16, 0.05),
                "Option": UI_Bouton(self.screen, (158, 253, 56), (190, 245, 116), self.resp_font(self.ratio_objet["Option"][2], self.ratio_objet["Option"][4]), self.resp(self.ratio_objet["Option"][0], self.ratio_objet["Option"][1], self.ratio_objet["Option"][2], self.ratio_objet["Option"][3]), "OPTION", 4, 12, 16, 0.05),
                "Quitter": UI_Bouton(self.screen, (158, 253, 56), (190, 245, 116), self.resp_font(self.ratio_objet["Quitter"][2], self.ratio_objet["Quitter"][4]), self.resp(self.ratio_objet["Quitter"][0], self.ratio_objet["Quitter"][1], self.ratio_objet["Quitter"][2], self.ratio_objet["Quitter"][3]), "QUITTER", 4, 12, 16, 0.05),
                "Credit": UI_Bouton(self.screen, (212, 115, 212), (0,0,0), self.resp_font(self.ratio_objet["Credit"][2], self.ratio_objet["Credit"][4]), self.resp(self.ratio_objet["Credit"][0], self.ratio_objet["Credit"][1], self.ratio_objet["Credit"][2], self.ratio_objet["Credit"][3]), "CREDIT", 5, 12, 16, 0.05),
                "Aide": UI_Bouton(self.screen, (255, 215, 0), (0,0,0), self.resp_font(self.ratio_objet["Aide"][2], self.ratio_objet["Aide"][4]), self.resp(self.ratio_objet["Aide"][0], self.ratio_objet["Aide"][1], self.ratio_objet["Aide"][2], self.ratio_objet["Aide"][3]), "?", 5, 12, 16, 0.05)
            },
            1:{
                "Retour1": UI_Bouton(self.screen, (4, 139, 154), (0,0,0), self.resp_font(self.ratio_objet["Retour1"][2], self.ratio_objet["Retour1"][4]), self.resp(self.ratio_objet["Retour1"][0], self.ratio_objet["Retour1"][1], self.ratio_objet["Retour1"][2], self.ratio_objet["Retour1"][3]), "RETOUR", 5, 12, 16, 0.05),
                "Son": UI_Bouton(self.screen, (23, 167, 232), (0,0,0), self.resp_font(self.ratio_objet["Son"][2], self.ratio_objet["Son"][4]), self.resp(self.ratio_objet["Son"][0], self.ratio_objet["Son"][1], self.ratio_objet["Son"][2], self.ratio_objet["Son"][3]), "SON", 5, 12, 16, 0.05),
                "Ecran": UI_Bouton(self.screen, (23, 167, 232), (0,0,0), self.resp_font(self.ratio_objet["Ecran"][2], self.ratio_objet["Ecran"][4]), self.resp(self.ratio_objet["Ecran"][0], self.ratio_objet["Ecran"][1], self.ratio_objet["Ecran"][2], self.ratio_objet["Ecran"][3]), "ECRAN", 5, 12, 16, 0.05),
                "Secret": UI_Bouton(self.screen, (23, 167, 232), (0,0,0), self.resp_font(self.ratio_objet["Secret"][2], self.ratio_objet["Secret"][4]), self.resp(self.ratio_objet["Secret"][0], self.ratio_objet["Secret"][1], self.ratio_objet["Secret"][2], self.ratio_objet["Secret"][3]), "<SECRET>", 5, 12, 16, 0.05),
            },
            2:{
                "Retour2": UI_Bouton(self.screen, (163,204,92), (0,0,0), self.resp_font(self.ratio_objet["Retour2"][2], self.ratio_objet["Retour2"][4]), self.resp(self.ratio_objet["Retour2"][0], self.ratio_objet["Retour2"][1], self.ratio_objet["Retour2"][2], self.ratio_objet["Retour2"][3]), "RETOUR", 5, 12, 16, 0.05),
            },
            3:{
                "Retour3": UI_Bouton(self.screen, (227,159,30), (0,0,0), self.resp_font(self.ratio_objet["Retour3"][2], self.ratio_objet["Retour3"][4]), self.resp(self.ratio_objet["Retour3"][0], self.ratio_objet["Retour3"][1], self.ratio_objet["Retour3"][2], self.ratio_objet["Retour3"][3]), "RETOUR", 5, 12, 16, 0.05),
            },
            4:{
            },
        }

        # Gestion des éléments graphiques non intéractif
        self.dico_UI = {
            0:{
            },
            1:{
            "rect_settings" : UI_screen(self.screen, (16,52,166), (255,255,255), self.resp(self.ratio_objet["Settings"][0], self.ratio_objet["Settings"][1], self.ratio_objet["Settings"][2], self.ratio_objet["Settings"][3]), taille_contour = 6, border_radius = 12),
            "rect_settings_select" : UI_screen(self.screen, (237,189,178), (0,0,0), self.resp(self.ratio_objet["Settings_select"][0], self.ratio_objet["Settings_select"][1], self.ratio_objet["Settings_select"][2], self.ratio_objet["Settings_select"][3]), taille_contour = 4, border_radius = 12),
            "rect_settings_modif" : UI_screen(self.screen, (237,189,178), (0,0,0), self.resp(self.ratio_objet["Settings_modif"][0], self.ratio_objet["Settings_modif"][1], self.ratio_objet["Settings_modif"][2], self.ratio_objet["Settings_modif"][3]), taille_contour = 4, border_radius = 12),
            "Text_setting" : Texte(self.screen, self.resp_text(self.ratio_objet["Text_setting"][0], self.ratio_objet["Text_setting"][1]), self.resp_font(self.ratio_objet["Text_setting"][0], self.ratio_objet["Text_setting"][2]), (255,255,255), "SETTINGS", font_type = "font/font_retro.ttf")
            },
            2:{
            "rect_credit" : UI_screen(self.screen, (87,250,233), (250,87,103), self.resp(self.ratio_objet["Rect_Credit"][0], self.ratio_objet["Rect_Credit"][1], self.ratio_objet["Rect_Credit"][2], self.ratio_objet["Rect_Credit"][3]), taille_contour = 6, border_radius = 12),
            "Text_credit" : Texte(self.screen, self.resp_text(self.ratio_objet["Text_credit"][0], self.ratio_objet["Text_credit"][1]), self.resp_font(self.ratio_objet["Text_credit"][0], self.ratio_objet["Text_credit"][2]), (255,255,255), "CREDIT", font_type = "font/font_retro.ttf"),
            },
            3:{
            "rect_aide" : UI_screen(self.screen, (235,199,21), (21,57,235), self.resp(self.ratio_objet["Rect_Aide"][0], self.ratio_objet["Rect_Aide"][1], self.ratio_objet["Rect_Aide"][2], self.ratio_objet["Rect_Aide"][3]), taille_contour = 6, border_radius = 12),
            "rect_aide_bloc" : UI_screen(self.screen, (237, 169, 33), (237, 169, 33), self.resp(self.ratio_objet["Rect_Aide_Bloc"][0], self.ratio_objet["Settings"][1], self.ratio_objet["Rect_Aide_Bloc"][2], self.ratio_objet["Rect_Aide_Bloc"][3]), taille_contour= 5, border_radius = 12),
            "Text_aide" : Texte(self.screen, self.resp_text(self.ratio_objet["Text_aide"][0], self.ratio_objet["Text_aide"][1]), self.resp_font(self.ratio_objet["Text_aide"][0], self.ratio_objet["Text_aide"][2]), (255,255,255), "AIDE", font_type = "font/font_retro.ttf"),
            "Text_bloc_aide" : Texte(self.screen, self.resp_text(self.ratio_objet["Text_bloc_aide"][0], self.ratio_objet["Text_bloc_aide"][1]), self.resp_font(self.ratio_objet["Text_bloc_aide"][0], self.ratio_objet["Text_bloc_aide"][2]), (255,255,255), "Voici un texte", font_type = "font/font_retro.ttf"),
            },
            4:{
            "Texte_secret" : Texte(self.screen, self.resp_text(self.ratio_objet["Text_secret"][0], self.ratio_objet["Text_secret"][1]), self.resp_font(self.ratio_objet["Text_secret"][0], self.ratio_objet["Text_secret"][2]), (24, 255, 3), "Tu ne devrais pas etre ici...", font_type = "font/font_retro.ttf")
            },
        }

        # Gestion des sprites ou surfaces des sous-plans
        self.setting_UI = {
            0:{
            },
            1:{
            "Couper_Son": UI_PNG(self.screen, self.son_off_on[self.son_actif], self.resp(self.ratio_objet["Couper_Son"][0], self.ratio_objet["Couper_Son"][1], self.ratio_objet["Couper_Son"][2], self.ratio_objet["Couper_Son"][3]), 15, 0.05),
            "Couper_Music": UI_PNG(self.screen, self.music_off_on[self.music_actif], self.resp(self.ratio_objet["Couper_Music"][0], self.ratio_objet["Couper_Music"][1], self.ratio_objet["Couper_Music"][2], self.ratio_objet["Couper_Music"][3]), 15, 0.05),
            },
            2:{
            },
            3:{
            "Secret": InputText(self.screen, self.resp(self.ratio_objet["Champ_secret"][0], self.ratio_objet["Champ_secret"][1], self.ratio_objet["Champ_secret"][2], self.ratio_objet["Champ_secret"][3]))
            },
            4:{
            },
        }
        
        # Variable de démarrage de partie
        self.play_game = False

    def exit(self):
        '''Gère la fermeture de la fenêtre'''
        # On récupère tous les évènements pour vérifier si il y a un événement de type : pygame.QUIT
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (self.dico_UI_interact[0]["Quitter"].mouse_is_click() and self.plan == 0):
                    self.running = False  # Ceci arrête la boucle principal

    def is_play(self):
        '''
        Cette fonction renvoit un booleen qui déclenche une partie
        '''
        if self.dico_UI_interact[0]["Jouer"].mouse_is_click():  # On vérifie si le bouton "Jouer" est cliqué
            self.running = False
            self.play_game = True
            return True
        else:
            return False

    def play_music(self, fichier:str, volume:float = 0.7):
        '''
        Cette fonction importe et lance la musique en boucle
        '''
        if self.current_music == fichier:
            return  # La musique est déjà en train de jouer

        pygame.mixer.music.stop()
        pygame.mixer.music.load(fichier)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

        self.current_music = fichier

    def move_plan(self):
        '''
        Cette fonction gère les changements de plans grâce aux boutons
        '''
        if self.dico_UI_interact[0]["Option"].mouse_is_click():
            self.plan = 1

        if self.dico_UI_interact[0]["Credit"].mouse_is_click():
            self.plan = 2

        if self.setting_UI[3]["Secret"].get_last_message().upper() == "HAPPY MEAL" and self.sous_plan == 3:
            self.plan = 4

        if self.dico_UI_interact[0]["Aide"].mouse_is_click():
            self.plan = 3

        if self.plan in (1,2,3,4) and (self.keys[pygame.K_ESCAPE] or self.dico_UI_interact[1]["Retour1"].mouse_is_click() or self.dico_UI_interact[2]["Retour2"].mouse_is_click() or self.dico_UI_interact[3]["Retour3"].mouse_is_click()):
            self.plan = 0
            self.sous_plan = 0

        if self.dico_UI_interact[1]["Son"].mouse_is_click():
            self.sous_plan = 1

        if self.dico_UI_interact[1]["Ecran"].mouse_is_click():
            self.sous_plan = 2

        if self.dico_UI_interact[1]["Secret"].mouse_is_click():
            self.sous_plan = 3

    def resp(self, ratio_x:float, ratio_y:float, ratio_long:float, ratio_larg:float):
        '''Méthode qui gère la responsive des surfaces comme les boutons, les interfaces ou les champs'''
        # On convertit tout les éléments par rapport à un ratio et à la taille de l'écran
        x = self.Long * ratio_x
        y = self.larg * ratio_y
        L = self.Long * ratio_long
        l = self.larg * ratio_larg
        return (x, y, L, l)

    def resp_font(self, ratio_long:float, ratio_font:float):
        '''
        Méthode qui gère la responsive des tailles de polices d'écriture en fonction de la 
        longueur d'une surface
        '''
        return int(self.Long * ratio_long * ratio_font)

    def resp_text(self, ratio_x:float, ratio_y:float):
        '''
        Méthode qui gère la responsive des positions des textes à partir d'un ratio x et y
        '''
        return (self.Long * ratio_x, self.larg * ratio_y)

    def couper_son(self):
        '''
        Cette méthode gère l'arrêt de tous bruitage dans les settings en cliquant sur le png correspondant
        '''
        if self.setting_UI[1]["Couper_Son"].mouse_is_click():  # On vérifie si le png de bruitage est bien cliqué
            self.son_actif = (self.son_actif + 1) % 2  # On change l'indice de sprite (le modulo permet de rester entre 0 et 1)

            self.setting_UI[1]["Couper_Son"].img_base = pygame.image.load(f"sprite/{self.son_off_on[self.son_actif]}").convert_alpha()  # On modifie le sprite dans la classe

            if self.son_actif == 1:  # Ici si le son est coupé on réduit le volume pour tout les objets admettant des bruitages
                for boutons in self.dico_UI_interact.values():
                    for bouton in boutons.values():
                        bouton.volume = 0
                for pngs in self.setting_UI.values():
                    for png in pngs.values():
                        png.volume = 0
            else: # Si le son est réactivé, on restaure les paramètres initiaux des objets concernant les bruitages
                for boutons in self.dico_UI_interact.values():
                    for bouton in boutons.values():
                        bouton.volume = 0.05
                for pngs in self.setting_UI.values():
                    for png in pngs.values():
                        png.volume = 0.05

    def couper_musique(self):
        '''
        Cette méthode gère l'arrêt de la musique dans les settings en cliquant sur le png correspondant
        '''
        if self.setting_UI[1]["Couper_Music"].mouse_is_click(): # On vérifie si le png de la musique
            self.music_actif = (self.music_actif + 1) % 2 # On change l'indice de sprite (le modulo permet de rester entre 0 et 1)

            self.setting_UI[1]["Couper_Music"].img_base = pygame.image.load(f"sprite/{self.music_off_on[self.music_actif]}").convert_alpha()  # On modifie le sprite dans la classe

            if self.music_actif == 1: # Ici si la musique est coupé on met en pause la musique
                pygame.mixer.music.pause()
            else: # Si la musique est réactivée, on reprend la musique
                pygame.mixer.music.unpause()

    def changement_frame(self):
        '''
        Cette ùéthode premet de gèrer le changement de frames de l'arrière plan du menu
        '''
        time_delay = 1000  # On initialise un delai entre chaques changements de frames (1000ms soit 1s)
        flag_frame = pygame.time.get_ticks()
        if flag_frame - self.last_frame_change >= time_delay: # On vérifie si 1s c'est bien écoulée
            self.frame = (self.frame + randint(2, 4)) % len(self.background) # On change l'indice de frame aléatoirement (le modulo permet d'avoir des indices compris entre 0 et le nombre de frames
            self.last_frame_change = flag_frame

    def stats(self):
        '''
        Cette méthode permet de gérer l'affichage des stats de performance et de test
        '''
        if self.keys[pygame.K_F1]:
            txt = self.font.render(f"FPS : {self.fps}", True, (255,255,255))  # FPS
            self.screen.blit(txt, (0,0))
            txt = self.font.render(f"Timer : {self.temps_ecoule}", True, (255,255,255))  # Temps écoulé
            self.screen.blit(txt, (0,25))
            txt = self.font.render(f"Num de plan : {self.plan}", True, (255,255,255))  # Numéro plan
            self.screen.blit(txt, (0,50))
            txt = self.font.render(f"Num de sous plan : {self.sous_plan}", True, (255,255,255))  # Numéro sous-plan
            self.screen.blit(txt, (0,75))

    def run(self):
        '''
        Cette méthode enclenche la boucle principale du menu en appelant toutes les méthodes utiles à 
        son fonctionnement
        '''
        while self.running:
            self.keys = pygame.key.get_pressed()  # On récupère les touches enclenchées
            self.clock.tick(60)  # On paramètre le tick soit les fps max de la boucle (ici 60fps)
            self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000  # On récupère le temps réel
            self.fps = int(self.clock.get_fps())  # On récupère les fps en temps réel
            if self.music_actif == 0:  # musique autorisée
                if self.plan == 4:
                    self.play_music("sound/whoofs.wav")
                else:
                    self.play_music("sound/music2.mp3")
            self.draw()  # On affiche les éléments graphiques
            self.is_play()  # On vérifie si une partie est lancée
            self.move_plan()  # On gère les changements de plans
            if self.plan == 1:
                self.couper_son()  # On gère l'arrêt des bruitages
                self.couper_musique()  # On gère l'arrêt de la musique
            self.exit()  # On test si une condition d'arrêt est déclenchée

        pygame.mixer.music.stop()  # Si le programme s'arrête on stop la musique
        if not self.play_game:
            pygame.quit() # On quitte proprement le jeu si aucune partie n'est déclenchée

    def draw(self):
        '''
        Cette méthode gère tout les affichages d'objets à l'écran ainsi que le rafraichissement de celui-ci
        '''
        if self.plan == 4:  
            self.screen.fill((0,0,0))  # Si on est dans le plan secret alors on affiche un arrière plan noir
            
        else:  # Sinon on affiche le logo du jeu et l'arrière plan
            self.screen.blit(self.background[self.frame], (0,0))
            self.screen.blit(self.logo, (self.Long * self.ratio_objet["Logo_jeu"][0], self.larg * self.ratio_objet["Logo_jeu"][1]))    
            self.changement_frame()  # Ici on gère le changment de frames de l'arrière plan
            
            
        for interfaces in self.dico_UI[self.plan].values():  # On update les objets non interactifs
            interfaces.update()

        for boutons in self.dico_UI_interact[self.plan].values(): # On update les objets interactifs
            boutons.update()

        if self.plan == 1:
            for setting in self.setting_UI[self.sous_plan].values(): # Si on est dans les settings, on update les objets paramètriques
                setting.update()

        self.stats()  # On gère l'affichage des stats

        # Rafraîchissement de l'écran
        pygame.display.flip()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    hub = Hub()
    hub.run()