# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
import os

# Initialisation de Pygame et de ses modules audio et police
pygame.init()
pygame.mixer.init()
pygame.font.init()

class Intro:
    '''Cette classe gère l'introduction du jeu avec logo et musique'''

    def __init__(self, logo:str, screen):
        # Récupération des dimensions de l'écran
        self.Long, self.larg = screen.get_size()
        self.screen = screen

        # Temps de départ et horloge pour le framerate
        self.start_time = pygame.time.get_ticks()  # timestamp de départ
        self.clock = pygame.time.Clock()
        
        # Détermination du chemin du logo
        BASE_DIR = os.path.dirname(__file__)
        LOGO_PATH = os.path.join(BASE_DIR, "sprite", logo)

        # Chargement et mise à l'échelle du logo
        self.logo = pygame.image.load(LOGO_PATH).convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (int(self.Long * 0.80), int(self.Long * 0.80)))
        self.logo_rect = self.logo.get_rect(center = (self.Long//2, self.larg //2))

        # Initialisation de l'opacité pour effet fade-in/fade-out
        self.opacite_logo = 0
        self.logo.set_alpha(self.opacite_logo)

        # Chargement de la musique d'intro
        MUSIC1_PATH = os.path.join(BASE_DIR, "sound", "intro.wav")
        MUSIC2_PATH = os.path.join(BASE_DIR, "sound", "intro2.wav")
        self.sound_intro = pygame.mixer.Sound(MUSIC1_PATH)
        self.sound_intro.set_volume(0.6)
        self.sound_intro2 = pygame.mixer.Sound(MUSIC2_PATH)
        self.sound_intro2.set_volume(0.05)

        # Flags pour contrôler quand jouer la musique
        self.flag_intro = False
        self.flag_intro2 = True

        # Police pour afficher FPS et timer si nécessaire
        self.font = pygame.font.Font(None, 30)

        # Booléen pour activer/désactiver la boucle d'intro
        self.running = True

    def play_sound(self):
        """Joue les sons d'intro selon les flags"""
        if not self.flag_intro:
            self.sound_intro.play()
            self.flag_intro = True
            self.flag_intro2 = False

        if not self.flag_intro2:
            self.sound_intro2.play()
            self.flag_intro2 = True

    def animation(self):
        """Gère l'effet fade-in et fade-out du logo selon le temps écoulé"""
        if 2 <= self.temps_ecoule <= 4:
            # Augmente l'opacité progressivement (fade-in)
            self.opacite_logo += (255/(self.fps+1))

        elif 4 < self.temps_ecoule <= 6:
            # Maintient l'opacité à 100%
            self.opacite_logo = 255

        elif 6 < self.temps_ecoule <= 8:
            # Diminue progressivement l'opacité (fade-out)
            self.opacite_logo -= (255/(self.fps+1))

        self.logo.set_alpha(self.opacite_logo)
    
    def stat(self):
        """Affiche FPS et temps écoulé si la touche F1 est pressée"""
        if self.keys[pygame.K_F1]:
            txt = self.font.render(f"FPS : {self.fps}", True, (255,255,255))
            self.screen.blit(txt, (5,0))
            txt = self.font.render(f"Timer : {self.temps_ecoule}", True, (255,255,255))
            self.screen.blit(txt, (5,25))

    def exit(self):
        '''Gère la fermeture de la fenêtre ou appui sur ESC'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.running = False
    
    def run(self):
        """Boucle principale de l'intro"""
        while self.running:
            # Récupération des touches pressées
            self.keys = pygame.key.get_pressed()
            self.clock.tick(120)  # Limitation du framerate à 120 FPS
            self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000
            self.fps = int(self.clock.get_fps())

            # Gestion des événements de fermeture
            self.exit()

            # Fond noir
            self.screen.fill((0, 0, 0))

            # Jouer le son quand le logo est suffisamment visible
            if self.opacite_logo > 180:
                self.play_sound()

            # Mise à jour de l'animation du logo
            self.animation()

            # Affichage des stats si nécessaire
            self.stat()

            # Affichage du logo
            self.screen.blit(self.logo, self.logo_rect)
            
            # Rafraîchissement de l'écran
            pygame.display.flip()

            # Fin de l'intro après 8 secondes
            if self.temps_ecoule >= 8:
                self.running = False

# Partie exécutable si le fichier est lancé directement
if __name__ == "__main__":
    # Récupère la taille de l'écran
    screen_taille = pygame.display.Info()
    Long = screen_taille.current_w
    larg = screen_taille.current_h

    # Création de la fenêtre
    screen = pygame.display.set_mode((Long, larg))
    pygame.display.set_caption("Let's Break Down The Earth") # Titre de la fenêtre

    # Création de l'objet Intro et lancement de l'intro
    intro = Intro("logo5.png", screen)
    intro.run()
