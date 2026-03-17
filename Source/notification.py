# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEWELINE COLLIN--MONTRON

import pygame
import os


# Classe qui gère l'affichage des notifications à l'écran
class Notification_gestion:

    # Initialisation du système de notification
    def __init__(self, screen, rect_ui, color=(255, 255, 255), font_size_ratio=0.19, diff_y=15, volume_sound = 0.2):

        # Surface principale du jeu
        self.screen = screen

        # Rectangle UI dans lequel le texte sera affiché
        self.rect_ui = rect_ui

        # Couleur du texte
        self.color = color

        # Ratio permettant de calculer la taille de la police selon la taille du rectangle
        self.font_size_ratio = font_size_ratio

        # Décalage vertical pour le texte
        self.diff_y = diff_y

        # Chemin du dossier du script
        self.BASE_DIR = os.path.dirname(__file__)

        # Chemin de la police utilisée pour les notifications
        self.FONT_PATH = os.path.join(self.BASE_DIR, "font", "retro_notif.ttf")

        # Chargement du son joué lorsqu'une notification apparaît
        self.NOTIF_SONG_PATH = os.path.join(self.BASE_DIR, "sound", "notif.wav")
        self.notif_sound = pygame.mixer.Sound(self.NOTIF_SONG_PATH)
        self.notif_sound.set_volume(volume_sound)

        # Création de la police UNE SEULE FOIS (optimisation)
        rect = self.rect_ui.rect
        font_size = int(rect.height * self.font_size_ratio)
        self.font = pygame.font.Font(self.FONT_PATH, font_size)

        # Liste des messages (file de notifications)
        self.file = []

        # Message actuellement actif
        self.active_message = ""

        # Texte actuellement affiché (effet machine à écrire)
        self.current_display = ""

        # Index du caractère en train d'être écrit
        self.char_index = 0

        # Vitesse d'écriture (ms entre chaque caractère)
        self.typing_speed = 10

        # Temps du dernier caractère écrit
        self.last_char_time = pygame.time.get_ticks()

        # Indique si l'effet machine à écrire est actif
        self.is_typing = False

        # Message affiché quand il n'y a aucune notification
        self.default_message = "Aucunes Notifications ici ..."

        # Indique si le message par défaut doit être affiché
        self.show_default = True

        # Liste des surfaces texte déjà rendues
        self.rendered_lines = []

        # Indique si la mise en page doit être recalculée
        self.layout_dirty = False

        # Initialisation avec le message par défaut
        self.active_message = self.default_message
        self.current_display = self.default_message
        self.char_index = len(self.default_message)
        self.is_typing = False
        self.layout_dirty = True

    # Ajoute une nouvelle notification
    def ajouter(self, message):
        """Ajoute une nouvelle notification et remplace l'ancienne."""

        # Nouveau message actif
        self.active_message = message

        # On vide le texte affiché pour recommencer l'effet typing
        self.current_display = ""

        # Réinitialisation de l'index
        self.char_index = 0

        # Activation de l'effet machine à écrire
        self.is_typing = True

        # Demande de recalcul de la mise en page
        self.layout_dirty = True

        # On désactive le message par défaut
        self.show_default = False

        # Lecture du son de notification
        self.notif_sound.play()

    # Mise à jour du système de notification
    def update(self):
        """Met à jour le texte à afficher."""

        # Gestion de l'effet machine à écrire
        if self.is_typing:

            now = pygame.time.get_ticks()

            # Vérifie si le temps entre deux caractères est écoulé
            if now - self.last_char_time > self.typing_speed:

                self.last_char_time = now

                # Ajout du caractère suivant
                if self.char_index < len(self.active_message):

                    self.current_display += self.active_message[self.char_index]
                    self.char_index += 1

                    # Demande de recalcul du layout
                    self.layout_dirty = True

                else:
                    # Fin de l'effet typing
                    self.is_typing = False

                    # On affiche le message complet
                    self.current_display = self.active_message

        # Recalcul de la mise en page uniquement si nécessaire
        if self.layout_dirty:
            self._update_text_layout()
            self.layout_dirty = False

    # Calcul de la mise en page du texte
    def _update_text_layout(self):
        """Met en page le texte pour qu’il tienne dans le rectangle."""

        rect = self.rect_ui.rect

        # Largeur maximale autorisée pour une ligne
        max_width = rect.width * 0.9

        # Réinitialisation des lignes
        self.rendered_lines = []

        # Découpage du texte par paragraphes
        paragraphs = self.current_display.split("\n")

        # Traitement de chaque paragraphe
        for paragraph in paragraphs:

            words = paragraph.split(" ")
            current_line = ""

            # Construction des lignes mot par mot
            for word in words:

                test_line = current_line + word + " "

                # Vérifie si la ligne rentre dans la largeur maximale
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line

                else:
                    # On ajoute la ligne actuelle
                    self.rendered_lines.append(self.font.render(current_line, True, self.color))

                    # On commence une nouvelle ligne
                    current_line = word + " "

            # Ajout de la dernière ligne du paragraphe
            if current_line:
                self.rendered_lines.append(self.font.render(current_line, True, self.color))

    # Affichage des notifications à l'écran
    def draw(self):
        """Affiche le texte à l'écran."""

        # Si aucune ligne n'existe, on ne dessine rien
        if not self.rendered_lines:
            return

        rect = self.rect_ui.rect

        # Hauteur d'une ligne de texte
        line_height = self.font.get_height()

        # Hauteur totale du bloc de texte
        total_height = len(self.rendered_lines) * line_height

        # Position verticale de départ pour centrer le texte
        start_y = rect.centery - total_height // 2

        # Affichage de chaque ligne
        for i, surf in enumerate(self.rendered_lines):

            txt_rect = surf.get_rect(center=(rect.centerx, start_y + i * line_height + self.diff_y))

            # Dessin du texte à l'écran
            self.screen.blit(surf, txt_rect)