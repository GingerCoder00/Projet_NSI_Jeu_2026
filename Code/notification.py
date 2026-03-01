import pygame
import os

class Notification_gestion:
    def __init__(self, screen, rect_ui, color=(255, 255, 255), font_size_ratio=0.19, diff_y=15, volume_sound = 0.2):
        self.screen = screen
        self.rect_ui = rect_ui
        self.color = color
        self.font_size_ratio = font_size_ratio
        self.diff_y = diff_y

        self.BASE_DIR = os.path.dirname(__file__)
        self.FONT_PATH = os.path.join(self.BASE_DIR, "font", "retro_notif.ttf")

        self.NOTIF_SONG_PATH = os.path.join(self.BASE_DIR, "sound", "notif.wav")
        self.notif_sound = pygame.mixer.Sound(self.NOTIF_SONG_PATH)
        self.notif_sound.set_volume(volume_sound)

        # Police créée UNE SEULE FOIS
        rect = self.rect_ui.rect
        font_size = int(rect.height * self.font_size_ratio)
        self.font = pygame.font.Font(self.FONT_PATH, font_size)

        self.file = []
        self.active_message = ""  # Message en cours
        self.current_display = ""  # Texte affiché pour typing
        self.char_index = 0
        self.typing_speed = 20
        self.last_char_time = pygame.time.get_ticks()
        self.is_typing = False

        # Message par défaut
        self.default_message = "Aucunes Notifications ici ..."
        self.show_default = True  # On doit afficher le message par défaut au début

        # Pré-render
        self.rendered_lines = []
        self.layout_dirty = False

        # On initialise le message par défaut dès le départ
        self.active_message = self.default_message
        self.current_display = self.default_message
        self.char_index = len(self.default_message)
        self.is_typing = False
        self.layout_dirty = True

    def ajouter(self, message):
        """Ajoute une nouvelle notification et remplace l'ancienne."""
        self.active_message = message
        self.current_display = ""
        self.char_index = 0
        self.is_typing = True
        self.layout_dirty = True
        self.show_default = False  # On n'affichera plus le message par défaut
        self.notif_sound.play()

    def update(self):
        """Met à jour le texte à afficher."""
        # Machine à écrire
        if self.is_typing:
            now = pygame.time.get_ticks()
            if now - self.last_char_time > self.typing_speed:
                self.last_char_time = now
                if self.char_index < len(self.active_message):
                    self.current_display += self.active_message[self.char_index]
                    self.char_index += 1
                    self.layout_dirty = True
                else:
                    self.is_typing = False
                    # On garde le texte affiché tant qu'une nouvelle notif n'est pas ajoutée
                    self.current_display = self.active_message

        # Recalcul layout seulement si nécessaire
        if self.layout_dirty:
            self._update_text_layout()
            self.layout_dirty = False

    def _update_text_layout(self):
        """Met en page le texte pour qu’il tienne dans le rectangle."""
        rect = self.rect_ui.rect
        max_width = rect.width * 0.9

        words = self.current_display.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

        # Pré-render
        self.rendered_lines = [self.font.render(line, True, self.color) for line in lines]

    def draw(self):
        """Affiche le texte à l'écran."""
        if not self.rendered_lines:
            return

        rect = self.rect_ui.rect
        line_height = self.font.get_height()
        total_height = len(self.rendered_lines) * line_height
        start_y = rect.centery - total_height // 2

        for i, surf in enumerate(self.rendered_lines):
            txt_rect = surf.get_rect(center=(rect.centerx, start_y + i * line_height + self.diff_y))
            self.screen.blit(surf, txt_rect)