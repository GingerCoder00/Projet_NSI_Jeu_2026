# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from phrases_notif import PHRASES_DESINFORMATION, PHRASES_POUVOIR
from random import choice
from ui_tools import UI_screen, Texte
import os

class Pouvoir:
    def __init__(self, screen, nom, bouton, data, grille, callback_action, notif_manager, cursor_sprite_prefix=None, cursor_frame_count=1, cooldown=3, frame_delay=100, cible_grille=True):

        # Références principales du jeu
        self.screen = screen
        self.nom = nom                      # Nom du pouvoir
        self.bouton = bouton                # Bouton UI associé
        self.data = data                    # Données globales du jeu (profit, stats, etc.)
        self.grille = grille                # Grille du jeu
        self.callback_action = callback_action  # Fonction appelée lorsque le pouvoir est utilisé
        self.cible_grille = cible_grille    # Indique si le pouvoir nécessite de cliquer sur une case
        self.notif = notif_manager          # Gestionnaire de notifications

        # Etat du pouvoir
        self.actif = False                  # Indique si le pouvoir est actuellement activé

        # Gestion du cooldown
        self.cooldown = cooldown            # Temps de recharge du pouvoir
        self.last_use = -cooldown           # Temps de dernière utilisation
        self.ready = True                   # Indique si le pouvoir est prêt à être utilisé

        # Animation du curseur du pouvoir
        self.cursor_frames = []             # Liste des images d'animation du curseur
        self.cursor_frame_index = 0         # Frame actuelle
        self.cursor_last_update = pygame.time.get_ticks()
        self.frame_delay = frame_delay      # Temps entre deux frames

        # Chargement des sprites du curseur
        if cursor_sprite_prefix:
            for i in range(cursor_frame_count):
                path = f"{cursor_sprite_prefix}{i}.png"
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (60, 60))
                self.cursor_frames.append(img)

        # Informations UI du pouvoir (affichées au survol)

        self.Longueur, self.largeur = self.screen.get_size()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Ratios pour placer les textes dans la fenêtre d'information
        self.ratio_texte = {
            "Nom_Pouvoir" : (0.01, 0.02),
            "Cout_Pouvoir" : (0.01, 0.08),
            "Cooldown_Pouvoir" : (0.01, 0.14),
        }

        self.show_info = False

        # Chemins vers les ressources
        self.BASE_DIR = os.path.dirname(__file__)
        self.FONT_PATH = os.path.join(self.BASE_DIR, "font", "font_retro2.ttf")

        # Fenêtre d'information du pouvoir
        self.info = UI_screen(self.screen, (255, 119, 92), (117, 0, 0), (self.mouse_x - self.Longueur * 0.19, self.mouse_y - self.largeur * 0.19, self.Longueur * 0.19, self.largeur * 0.19), 7, 18)

        # Texte affichant le nom du pouvoir
        self.texte_nom = Texte(self.screen, (self.mouse_x + self.Longueur * self.ratio_texte["Nom_Pouvoir"][0], self.mouse_y + self.largeur * self.ratio_texte["Nom_Pouvoir"][1]), int(self.Longueur * 0.07 * 0.3), (255, 237, 237), f"{self.nom.capitalize()}", font_type=self.FONT_PATH)

        # Texte affichant le coût
        self.texte_cout = Texte(self.screen, (self.mouse_x + self.Longueur * self.ratio_texte["Cout_Pouvoir"][0], self.mouse_y + self.largeur * self.ratio_texte["Cout_Pouvoir"][1]), int(self.Longueur * 0.07 * 0.3), (255, 237, 237), f"Cout : {self.get_cout()}", font_type=self.FONT_PATH)

        # Texte affichant le cooldown
        self.texte_cooldown = Texte(self.screen, (self.mouse_x + self.Longueur * self.ratio_texte["Cooldown_Pouvoir"][0], self.mouse_y + self.largeur * self.ratio_texte["Cooldown_Pouvoir"][1]), int(self.Longueur * 0.07 * 0.3), (255, 237, 237), f"Cooldown : {self.cooldown}s", font_type=self.FONT_PATH)

    def get_cout(self):
        """Retourne le coût du pouvoir."""
        if self.nom in self.data.pouvoirs:
            return self.data.pouvoirs[self.nom]["cout"]
        return 0


    def assez_argent(self):
        """Vérifie si le joueur possède assez de profit pour utiliser le pouvoir."""
        return self.data.profit >= self.get_cout()


    def is_ready(self, current_time):
        """Vérifie si le cooldown est terminé."""
        return (current_time - self.last_use) >= self.cooldown


    def update(self, cases, current_time):
        """
        Fonction principale appelée à chaque frame.
        Gère l'activation et l'utilisation du pouvoir.
        """

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Vérifie si le cooldown est terminé
        self.ready = self.is_ready(current_time)

        # Si pas assez d'argent → notification
        if not self.assez_argent():
            if self.bouton.mouse_is_click():
                phrase = PHRASES_POUVOIR[3]
                self.notif.ajouter(phrase)
            return False

        # Si le bouton est cliqué et que le pouvoir est prêt
        if self.bouton.mouse_is_click() and self.ready:
            return "activate"

        # Pouvoir global (pas besoin de cliquer sur la grille)
        if self.actif and not self.cible_grille:

            if self.data.utiliser_pouvoir(self.nom):
                self.callback_action()
                self.last_use = current_time

                # Notifications spécifiques
                if self.nom == "desinformation":
                    self.notif.ajouter(choice(PHRASES_DESINFORMATION))
                    self.data.desinformation_creee += 1

                if self.nom == "guerre":
                    self.notif.ajouter(PHRASES_POUVOIR[8])
                    self.data.guerre_declaree += 1

                if self.nom == "canicule":
                    self.notif.ajouter(PHRASES_POUVOIR[9])

            self.actif = False
            return True

        # Pouvoir nécessitant une cible sur la grille
        if self.actif:

            for index, case in cases.items():

                if case.mouse_is_click():

                    ligne = index // self.grille.colonnes
                    colonne = index % self.grille.colonnes

                    if self.data.utiliser_pouvoir(self.nom, ligne, colonne):

                        # Exécution de l'action
                        self.callback_action(ligne, colonne)
                        self.last_use = current_time

                        # Notifications selon le pouvoir
                        if self.nom == "incendie":
                            self.notif.ajouter(PHRASES_POUVOIR[5])
                            self.data.incendie_declaree += 1

                        if self.nom == "usine":
                            self.notif.ajouter(PHRASES_POUVOIR[6])
                            self.data.usine_creee += 1

                        if self.nom == "Maree Noire":
                            self.notif.ajouter(PHRASES_POUVOIR[7])
                            self.data.case_polluees += 1

                    self.actif = False
                    return True

        return False


    def draw_cursor(self, screen):
        """Affiche l'animation du curseur du pouvoir."""

        if not self.actif or not self.cursor_frames or not self.assez_argent():
            return

        now = pygame.time.get_ticks()

        # Animation du curseur
        if now - self.cursor_last_update >= self.frame_delay:
            self.cursor_frame_index = (self.cursor_frame_index + 1) % len(self.cursor_frames)
            self.cursor_last_update = now

        img = self.cursor_frames[self.cursor_frame_index]

        mx, my = pygame.mouse.get_pos()
        rect = img.get_rect(center=(mx, my))

        screen.blit(img, rect)


    def draw_cooldown(self, screen):
        """Dessine le cooldown sur le bouton du pouvoir."""

        rect = self.bouton.rect

        # Pas assez d'argent
        if not self.assez_argent():
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill((80, 80, 80, 180))
            screen.blit(surface, (rect.x, rect.y))
            return

        # Cooldown actif
        if not self.ready:
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 150))
            screen.blit(surface, (rect.x, rect.y))

            remaining = round(self.cooldown - (pygame.time.get_ticks()/1000 - self.last_use), 1)

            font = pygame.font.Font(None, 28)
            txt = font.render(str(max(0, remaining)), True, (255,255,255))
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)


    def hover_info(self):
        """Affiche les informations du pouvoir lorsque la souris passe dessus."""

        if self.bouton.rect.collidepoint((self.mouse_x, self.mouse_y)):

            self.show_info = True

            # Position dynamique de la fenêtre
            self.info.x = min(self.mouse_x - self.Longueur * 0.19,
                              self.screen.get_width() - self.info.L)
            self.info.y = min(self.mouse_y - self.largeur * 0.19,
                              self.screen.get_height() - self.info.l)

            # Mise à jour des positions du texte
            self.texte_nom.x = self.info.x + self.Longueur * self.ratio_texte["Nom_Pouvoir"][0]
            self.texte_nom.y = self.info.y + self.largeur * self.ratio_texte["Nom_Pouvoir"][1]

            self.texte_cout.x = self.info.x + self.Longueur * self.ratio_texte["Cout_Pouvoir"][0]
            self.texte_cout.y = self.info.y + self.largeur * self.ratio_texte["Cout_Pouvoir"][1]

            self.texte_cooldown.x = self.info.x + self.Longueur * self.ratio_texte["Cooldown_Pouvoir"][0]
            self.texte_cooldown.y = self.info.y + self.largeur * self.ratio_texte["Cooldown_Pouvoir"][1]

        else:
            self.show_info = False


    def draw_info(self):
        """Dessine la fenêtre d'information du pouvoir."""

        if not self.show_info:
            return

        self.info.update()
        self.texte_nom.update()
        self.texte_cout.update()
        self.texte_cooldown.update()