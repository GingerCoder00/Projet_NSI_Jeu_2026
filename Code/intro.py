
import pygame
import os

pygame.init()
pygame.mixer.init()
pygame.font.init()

class Intro:
    '''Cete classe gère l'intro'''
    def __init__(self, logo:str):

        self.screen_taille = pygame.display.Info()
        self.Long = self.screen_taille.current_w
        self.larg = self.screen_taille.current_h

        self.screen = pygame.display.set_mode((self.Long, self.larg))
        pygame.display.set_caption("Let's Smash Up The Earth")

        self.start_time = pygame.time.get_ticks()  # temps de départ
        self.clock = pygame.time.Clock()
        
        BASE_DIR = os.path.dirname(__file__)
        LOGO_PATH = os.path.join(BASE_DIR, "sprite", logo)

        self.logo = pygame.image.load(LOGO_PATH).convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (int(self.Long * 0.80), int(self.Long * 0.80)))
        self.logo_rect = self.logo.get_rect(center = (self.Long//2, self.larg //2))

        self.opacite_logo = 0
        self.logo.set_alpha(self.opacite_logo)

        MUSIC1_PATH = os.path.join(BASE_DIR, "sound", "intro.wav")
        MUSIC2_PATH = os.path.join(BASE_DIR, "sound", "intro2.wav")
        self.sound_intro = pygame.mixer.Sound(MUSIC1_PATH)
        self.sound_intro.set_volume(0.6)
        self.sound_intro2 = pygame.mixer.Sound(MUSIC2_PATH)
        self.sound_intro2.set_volume(0.05)
        self.flag_intro = False
        self.flag_intro2 = True

        self.font = pygame.font.Font(None, 30)

        # Active et désactive la boucle de jeu
        self.running = True

    def play_sound(self):
        if not self.flag_intro:
            self.sound_intro.play()
            self.flag_intro = True
            self.flag_intro2 = False

        if not self.flag_intro2:
            self.sound_intro2.play()
            self.flag_intro2 = True

    def animation(self):
        if 2 <= self.temps_ecoule <= 4:
            self.opacite_logo += (255/(self.fps+1))

        elif  4 < self.temps_ecoule <= 6:
            self.opacite_logo = 255

        elif 6 < self.temps_ecoule <= 8:
            self.opacite_logo -= (255/(self.fps+1))

        self.logo.set_alpha(self.opacite_logo)
    
    def stat(self):
        if self.keys[pygame.K_F1]:
            txt = self.font.render(f"FPS : {self.fps}", True, (255,255,255))
            self.screen.blit(txt, (5,0))
            txt = self.font.render(f"Timer : {self.temps_ecoule}", True, (255,255,255))
            self.screen.blit(txt, (5,25))

    def exit(self):
        '''Gère la fermeture de la fenêtre'''
        for event in pygame.event.get():
                if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                    self.running = False
    
    def run(self):
        while self.running:
            self.keys = pygame.key.get_pressed()
            self.clock.tick(60)
            self.temps_ecoule = (pygame.time.get_ticks() - self.start_time)/1000
            self.fps = int(self.clock.get_fps())

            self.exit()
            self.screen.fill((0, 0, 0))
            if self.opacite_logo > 180:
                self.play_sound()
            self.animation()
            self.stat()
            self.screen.blit(self.logo, self.logo_rect)
            
            # Rafraîchissement de l'écran
            pygame.display.flip()

            if self.temps_ecoule >= 8:
                self.running = False

if __name__ == "__main__":
    intro = Intro("logo5.png")
    intro.run()