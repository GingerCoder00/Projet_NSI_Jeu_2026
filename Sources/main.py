# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from intro import Intro
from hub import Hub
from game import Game
import os


# Point d'entrée du programme
if __name__ == "__main__":

    # Initialisation des modules pygame
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    # Récupération de la résolution de l'écran
    screen_info = pygame.display.Info()
    Long = screen_info.current_w
    larg = screen_info.current_h

    # Création de la fenêtre du jeu en plein écran
    screen = pygame.display.set_mode((Long, larg), pygame.FULLSCREEN)

    # Chemin de base du projet
    BASE_DIR = os.path.dirname(__file__)

    # Chargement de l'icône de la fenêtre
    ICON_PATH = os.path.join(BASE_DIR, "sprite", "icon.png")
    icon = pygame.image.load(ICON_PATH)

    # Application de l'icône à la fenêtre
    pygame.display.set_icon(icon)

    # Titre de la fenêtre
    pygame.display.set_caption("Let's Break Down The Earth")

    # Chemin du logo affiché dans l'introduction
    LOGO_PATH = os.path.join(BASE_DIR, "sprite", "logo5.png")

    # Scène actuelle du jeu
    current_scene = "hub"

    # Variable contrôlant la boucle principale
    running = True

    # Lancement de l'écran d'introduction
    Intro(LOGO_PATH, screen).run()

    # Boucle principale du jeu
    while running:

        # Scène du hub (menu principal)
        if current_scene == "hub":

            # Création de la scène hub
            hub = Hub(screen)

            # Exécution du hub
            result = hub.run()

            # Si le joueur lance une partie
            if result == "game":
                current_scene = "game"

            # Sinon on quitte le jeu
            else:
                running = False


        # Scène du jeu principal
        elif current_scene == "game":

            # Création de la scène de jeu
            game = Game(screen)

            # Lancement de la partie
            result = game.run()
            # Retour au hub si demandé
            if result == "hub":
                current_scene = "hub"

            # Sinon on ferme le jeu
            else:
                running = False

    # Fermeture propre de pygame
    pygame.quit()