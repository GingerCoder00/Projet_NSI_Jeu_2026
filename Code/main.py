
import pygame
from intro import Intro
from hub import Hub
from game import Game


class Jeu:
    def __init__(self):
        '''
        Démarrage du programme principal
        '''
        Intro("logo5.png").run()
        Hub().run()
        Game().run()

if __name__ == "__main__":
    Jeu() 