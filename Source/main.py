# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from intro import Intro
from hub import Hub
from game import Game
import os


if __name__ == "__main__":

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    screen_info = pygame.display.Info()
    Long = screen_info.current_w
    larg = screen_info.current_h

    screen = pygame.display.set_mode((Long, larg), pygame.FULLSCREEN)

    BASE_DIR = os.path.dirname(__file__)
    ICON_PATH = os.path.join(BASE_DIR, "sprite", "icon.png")
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Let's Break Down The Earth")

    LOGO_PATH = os.path.join(BASE_DIR, "sprite", "logo5.png")

    current_scene = "hub"
    running = True
    Intro(LOGO_PATH, screen).run()

    while running:

        if current_scene == "hub":
            hub = Hub(screen)
            result = hub.run()

            if result == "game":
                current_scene = "game"
            else:
                running = False

        elif current_scene == "game":
            game = Game(screen)
            result = game.run()

            if result == "hub":
                current_scene = "hub"
            else:
                running = False

    pygame.quit()