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

        self.screen = screen
        self.Long, self.larg = screen.get_size()
        self.BASE_DIR = os.path.dirname(__file__)

        self.resp = Resp_tools(self.Long, self.larg)

        FONT_PATH = os.path.join(self.BASE_DIR, "font", "font_retro.ttf")
        self.font = pygame.font.Font(FONT_PATH, 20)

        self.start_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
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
            "Rect_Fond": UI_screen(self.screen, (110, 219, 219), (110, 219, 219), self.resp.resp(*self.ratio_objet["Rect_Fond"]), pulse=False),

            "Rect_Info_Pouvoir": UI_screen(self.screen, (88, 41, 0), (255, 255, 255), self.resp.resp(*self.ratio_objet["Rect_Info_Pouvoir"]), taille_contour=6, border_radius=12),

            "Rect_Info_Start": UI_screen(self.screen, (0, 86, 27), (255, 255, 255), self.resp.resp(*self.ratio_objet["Rect_Info_Start"]), taille_contour=6, border_radius=12),

            "Rect_Regle": UI_screen(self.screen, (212, 255, 255), (0, 184, 184), self.resp.resp(*self.ratio_objet["Rect_Regle"]), taille_contour=6, border_radius=12, pulse=False),
        }

        self.dico_UI_interact = {
            "Bouton_Retour": UI_Bouton(self.screen, (0, 123, 184), (0, 66, 97), self.resp.resp_font(self.ratio_objet["Bouton_Retour"][2], self.ratio_objet["Bouton_Retour"][4]), self.resp.resp(*self.ratio_objet["Bouton_Retour"][:4]), "RETOUR", 4, 12, 16, 0.05),
            "Bouton_Start": UI_Bouton(self.screen, (0, 123, 184), (0, 66, 97), self.resp.resp_font(self.ratio_objet["Bouton_Start"][2], self.ratio_objet["Bouton_Start"][4]), self.resp.resp(*self.ratio_objet["Bouton_Start"][:4]), "START", 4, 12, 16, 0.05),
        }

        self.notification = Notification_gestion(self.screen, self.dico_UI["Rect_Regle"], (0, 0, 0), font_size_ratio = 0.09, diff_y = 25)

        phrase = PHRASES_AIDE_START[0]
        self.notification.ajouter(phrase)

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.dico_UI_interact["Bouton_Retour"].mouse_is_click():
            self.running = False

    def stats(self):
        if pygame.key.get_pressed()[pygame.K_F1]:
            txt = self.font.render(f"FPS : {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.screen.blit(txt, (10, 10))

    def draw(self):
        self.screen.fill((0, 0, 0))

        for interfaces in self.dico_UI.values():
            interfaces.update()

        for objet in self.dico_UI_interact.values():
            objet.update()

        self.notification.update()
        self.notification.draw()

        self.stats()

        pygame.display.update()  # plus léger que flip()

    def run(self):
        while self.running:
            self.clock.tick(60)  # 🔥 60 FPS stable (menu inutile en 120)

            self.exit()
            self.draw()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
    Long = screen_taille.current_w # On récupère la longueur de l'écran
    larg = screen_taille.current_h # On récupère la hauteur de l'écran

    screen = pygame.display.set_mode((Long, larg)) # On initialise l'écran avec les dimensions préalablement récupérer
    pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre

    start_game = StartGame(screen)
    start_game.run()