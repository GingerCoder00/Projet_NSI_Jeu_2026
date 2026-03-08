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
    game = Game(screen)
    hub = Hub(screen)

    while running:

        if current_scene == "hub":
            result = hub.run()

            if result == "game":
                current_scene = "game"
            else:
                running = False

        elif current_scene == "game":
            result = game.run()

            if result == "hub":
                current_scene = "hub"
            else:
                running = False

    pygame.quit()