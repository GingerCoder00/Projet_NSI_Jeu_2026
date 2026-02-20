import pygame
import os

class Pouvoir:
    def __init__(self, nom, bouton, data, grille, callback_action,
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

        self.actif = False

        # -------- Cooldown --------
        self.cooldown = cooldown
        self.last_use = -cooldown
        self.ready = True

        # -------- Animation curseur --------
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

    # ---------------------------------------------------
    # Récupération automatique du coût depuis Data
    # ---------------------------------------------------

    def get_cout(self):
        if self.nom in self.data.pouvoirs:
            return self.data.pouvoirs[self.nom]["cout"]
        return 0

    def assez_argent(self):
        return self.data.profit >= self.get_cout()

    # ---------------------------------------------------

    def is_ready(self, current_time):
        return (current_time - self.last_use) >= self.cooldown

    # ---------------------------------------------------

    def update(self, cases, current_time):

        self.ready = self.is_ready(current_time)

        if not self.assez_argent():
            self.actif = False
            return False

        # Activation bouton
        if self.bouton.mouse_is_click() and self.ready:

            # 🎯 Cas pouvoir global (pas de case)
            if not self.cible_grille:

                if self.data.utiliser_pouvoir(self.nom):
                    self.callback_action()
                    self.last_use = current_time

                return True

            # 🎯 Cas pouvoir avec cible
            self.actif = True

        if not self.actif:
            return False

        for index, case in cases.items():
            if case.mouse_is_click():

                ligne = index // self.grille.colonnes
                colonne = index % self.grille.colonnes

                if self.data.utiliser_pouvoir(self.nom, ligne, colonne):
                    self.callback_action(ligne, colonne)
                    self.last_use = current_time

                self.actif = False
                return True

        return False

    # ---------------------------------------------------

    def draw_cursor(self, screen):

        # ❌ Si pas assez d'argent → pas de logo
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

    # ---------------------------------------------------

    def draw_cooldown(self, screen):

        rect = self.bouton.rect

        # 🟣 Cas 1 : Pas assez d'argent → bouton grisé
        if not self.assez_argent():
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill((80, 80, 80, 180))
            screen.blit(surface, (rect.x, rect.y))
            return

        # 🔵 Cas 2 : Cooldown actif
        if not self.ready:
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 150))
            screen.blit(surface, (rect.x, rect.y))

            remaining = round(self.cooldown - (pygame.time.get_ticks()/1000 - self.last_use), 1)

            font = pygame.font.Font(None, 28)
            txt = font.render(str(max(0, remaining)), True, (255,255,255))
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)