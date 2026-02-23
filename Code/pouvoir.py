import pygame
from phrases_notif import PHRASES_DESINFORMATION, PHRASES_POUVOIR
from random import choice

class Pouvoir:
    def __init__(self, nom, bouton, data, grille, callback_action,
                 notif_manager,
                 cursor_sprite_prefix=None,
                 cursor_frame_count=1,
                 cooldown=3,
                 frame_delay=100,
                 cible_grille=True):

        self.nom = nom
        self.bouton = bouton
        self.data = data
        self.grille = grille
        self.callback_action = callback_action
        self.cible_grille = cible_grille
        self.notif = notif_manager

        # Toujours présent mais contrôlé par Game
        self.actif = False

        # Cooldown
        self.cooldown = cooldown
        self.last_use = -cooldown
        self.ready = True

        # Animation curseur
        self.cursor_frames = []
        self.cursor_frame_index = 0
        self.cursor_last_update = pygame.time.get_ticks()
        self.frame_delay = frame_delay

        if cursor_sprite_prefix:
            for i in range(cursor_frame_count):
                path = f"{cursor_sprite_prefix}{i}.png"
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (60, 60))
                self.cursor_frames.append(img)

    def get_cout(self):
        if self.nom in self.data.pouvoirs:
            return self.data.pouvoirs[self.nom]["cout"]
        return 0

    def assez_argent(self):
        return self.data.profit >= self.get_cout()

    def is_ready(self, current_time):
        return (current_time - self.last_use) >= self.cooldown

    def update(self, cases, current_time):

        self.ready = self.is_ready(current_time)

        # Pas assez d'argent
        if not self.assez_argent():
            if self.bouton.mouse_is_click():
                phrase = PHRASES_POUVOIR[3]
                self.notif.ajouter(phrase)
            return False

        # Demande d'activation (au lieu d'activer direct)
        
        if self.bouton.mouse_is_click() and self.ready:
            return "activate"

        # Pouvoir global (pas de cible grille)
        
        if self.actif and not self.cible_grille:

            if self.data.utiliser_pouvoir(self.nom):
                self.callback_action()
                self.last_use = current_time

                if self.nom == "desinformation":
                    self.notif.ajouter(choice(PHRASES_DESINFORMATION))

                if self.nom == "guerre":
                    self.notif.ajouter(PHRASES_POUVOIR[8])

                if self.nom == "canicule":
                    self.notif.ajouter(PHRASES_POUVOIR[9])

            self.actif = False
            return True

        # Pouvoir avec cible grille

        if self.actif:

            for index, case in cases.items():
                if case.mouse_is_click():

                    ligne = index // self.grille.colonnes
                    colonne = index % self.grille.colonnes

                    if self.data.utiliser_pouvoir(self.nom, ligne, colonne):
                        self.callback_action(ligne, colonne)
                        self.last_use = current_time

                        if self.nom == "incendie":
                            self.notif.ajouter(PHRASES_POUVOIR[5])

                        if self.nom == "usine":
                            self.notif.ajouter(PHRASES_POUVOIR[6])

                        if self.nom == "maree_noire":
                            self.notif.ajouter(PHRASES_POUVOIR[7])

                    self.actif = False
                    return True

        return False

    def draw_cursor(self, screen):

        if not self.actif or not self.cursor_frames or not self.assez_argent():
            return

        now = pygame.time.get_ticks()

        if now - self.cursor_last_update >= self.frame_delay:
            self.cursor_frame_index = (self.cursor_frame_index + 1) % len(self.cursor_frames)
            self.cursor_last_update = now

        img = self.cursor_frames[self.cursor_frame_index]

        mx, my = pygame.mouse.get_pos()
        rect = img.get_rect(center=(mx, my))

        screen.blit(img, rect)

    def draw_cooldown(self, screen):

        rect = self.bouton.rect

        if not self.assez_argent():
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill((80, 80, 80, 180))
            screen.blit(surface, (rect.x, rect.y))
            return

        if not self.ready:
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 150))
            screen.blit(surface, (rect.x, rect.y))

            remaining = round(self.cooldown - (pygame.time.get_ticks()/1000 - self.last_use), 1)

            font = pygame.font.Font(None, 28)
            txt = font.render(str(max(0, remaining)), True, (255,255,255))
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)