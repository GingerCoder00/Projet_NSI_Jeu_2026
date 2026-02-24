import pygame
import os
from ui_tools import *
from animation import *
from resp_tools import *
from notification import *
from phrases_notif import PHRASES_AIDE_START

pygame.init()
pygame.mixer.init()
pygame.font.init()

class StartGame:
    def __init__(self, screen):

        self.Long, self.larg = screen.get_size()

        self.BASE_DIR = os.path.dirname(__file__)

        self.screen = screen

        self.resp = Resp_tools(self.Long, self.larg)
        self.flag_texte_aide = False
        FONT_PATH = os.path.join(self.BASE_DIR, "font", "font_retro.ttf")
        self.font = pygame.font.Font(FONT_PATH, 20)

        # Gestion du temps
        self.start_time = pygame.time.get_ticks()  # Temps de départ après l'initialisation de pygame
        self.clock = pygame.time.Clock() # Initialisation de l'horloge interne du jeu

        # Active et désactive la boucle de jeu
        self.running = True

        self.ratio_objet = {
            "Rect_Fond": (0, 0, 1, 1),
            "Rect_Info_Pouvoir": (0.43, 0.05, 0.53, 0.9),
            "Rect_Info_Start": (0.04, 0.05, 0.35, 0.9),
            "Rect_Regle": (0.075, 0.1, 0.28, 0.45),
            "Bouton_Retour": (0.111, 0.79, 0.2, 0.1, 0.2),
            "Bouton_Start": (0.089, 0.61, 0.25, 0.15, 0.22),
        }

        self.dico_UI = {
            "Rect_Fond" : UI_screen(self.screen, (110, 219, 219), (110, 219, 219), self.resp.resp(self.ratio_objet["Rect_Fond"][0], self.ratio_objet["Rect_Fond"][1], self.ratio_objet["Rect_Fond"][2], self.ratio_objet["Rect_Fond"][3]), pulse = False),
            "Rect_Info_Pouvoir" : UI_screen(self.screen, (88, 41, 0), (255,255,255), self.resp.resp(self.ratio_objet["Rect_Info_Pouvoir"][0], self.ratio_objet["Rect_Info_Pouvoir"][1], self.ratio_objet["Rect_Info_Pouvoir"][2], self.ratio_objet["Rect_Info_Pouvoir"][3]), taille_contour = 6, border_radius = 12),
            "Rect_Info_Start" : UI_screen(self.screen, (0, 86, 27), (255,255,255), self.resp.resp(self.ratio_objet["Rect_Info_Start"][0], self.ratio_objet["Rect_Info_Start"][1], self.ratio_objet["Rect_Info_Start"][2], self.ratio_objet["Rect_Info_Start"][3]), taille_contour = 6, border_radius = 12),
            "Rect_Regle" : UI_screen(self.screen, (212, 255, 255), (0, 184, 184), self.resp.resp(self.ratio_objet["Rect_Regle"][0], self.ratio_objet["Rect_Regle"][1], self.ratio_objet["Rect_Regle"][2], self.ratio_objet["Rect_Regle"][3]), taille_contour = 6, border_radius = 12, pulse = False),
        }

        self.dico_UI_interact = {
            "Bouton_Retour" : UI_Bouton(self.screen, (0, 123, 184), (0, 66, 97), self.resp.resp_font(self.ratio_objet["Bouton_Retour"][2], self.ratio_objet["Bouton_Retour"][4]), self.resp.resp(self.ratio_objet["Bouton_Retour"][0], self.ratio_objet["Bouton_Retour"][1], self.ratio_objet["Bouton_Retour"][2], self.ratio_objet["Bouton_Retour"][3]), "RETOUR", 4, 12, 16, 0.05),
            "Bouton_Start" : UI_Bouton(self.screen, (0, 123, 184), (0, 66, 97), self.resp.resp_font(self.ratio_objet["Bouton_Start"][2], self.ratio_objet["Bouton_Start"][4]), self.resp.resp(self.ratio_objet["Bouton_Start"][0], self.ratio_objet["Bouton_Start"][1], self.ratio_objet["Bouton_Start"][2], self.ratio_objet["Bouton_Start"][3]), "START", 4, 12, 16, 0.05),
        }

        self.notification = Notification_gestion(self.screen, self.dico_UI["Rect_Regle"], self.resp, (0,0,0))

    def exit(self):
        '''Gère la fermeture de la fenêtre'''
        # On récupère tous les évènements pour vérifier si il y a un événement de type : pygame.QUIT
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Ceci arrête la boucle principal

        if self.dico_UI_interact["Bouton_Retour"].mouse_is_click():
            self.running = False

    def stats(self):
        '''
        Cette méthode permet de gérer l'affichage des stats de performance et de test
        '''
        if self.keys[pygame.K_F1]:
            txt = self.font.render(f"FPS : {self.fps}", True, (255,255,255))  # FPS
            self.screen.blit(txt, (0,0))
            txt = self.font.render(f"Timer : {self.temps_ecoule}", True, (255,255,255))  # Temps écoulé
            self.screen.blit(txt, (0,25))

    def texte_aide(self):
        if not self.flag_texte_aide:
            phrase = PHRASES_AIDE_START[0]
            self.notification.ajouter(phrase)
            self.flag_texte_aide = True
            
    def draw(self):
        '''
        Cette méthode gère tout les affichages d'objets à l'écran ainsi que le rafraichissement de celui-ci
        '''
        self.screen.fill((0,0,0))  # Si on est dans le plan secret alors on affiche un arrière plan noir 

        for interfaces in self.dico_UI.values():
            interfaces.update()

        for objet in self.dico_UI_interact.values():
            objet.update()

        self.notification.draw()
        self.stats()

        pygame.display.flip()

    def run(self):
        '''
        Cette méthode enclenche la boucle principale du menu en appelant toutes les méthodes utiles à 
        son fonctionnement
        '''
        while self.running:
            self.keys = pygame.key.get_pressed()
            self.clock.tick(60)
            self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000
            self.fps = int(self.clock.get_fps())

            self.texte_aide()
            self.notification.update()
            self.draw()
            self.exit()


if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
    Long = screen_taille.current_w # On récupère la longueur de l'écran
    larg = screen_taille.current_h # On récupère la hauteur de l'écran

    screen = pygame.display.set_mode((Long, larg)) # On initialise l'écran avec les dimensions préalablement récupérer
    pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre

    start_game = StartGame(screen)
    start_game.run()