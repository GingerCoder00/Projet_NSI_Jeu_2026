
import pygame
from intro import Intro
from hub import Hub
from game import Game


class Jeu:
    def __init__(self):
        '''
        Démarrage du programme principal
        '''

        self.screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
        self.Long = self.screen_taille.current_w # On récupère la longueur de l'écran
        self.larg = self.screen_taille.current_h # On récupère la hauteur de l'écran

        self.screen = pygame.display.set_mode((self.Long, self.larg), pygame.FULLSCREEN) # On initialise l'écran avec les dimensions préalablement récupérer
        pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre

        intro = Intro("logo5.png", self.screen)
        hub = Hub(self.screen)
        game = Game(self.screen)

        intro.run()

        while True:
            hub = Hub(self.screen)
            game = Game(self.screen)
            hub.run()
            game.run()

if __name__ == "__main__":
    Jeu()