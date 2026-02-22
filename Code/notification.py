import pygame
import os

pygame.mixer.init()

class Notification:
    def __init__(self, message, duree=4000):
        self.message = message
        self.duree = duree
        self.start_time = pygame.time.get_ticks()

    def expiree(self):
        return pygame.time.get_ticks() - self.start_time > self.duree

class Notification_gestion:
    def __init__(self, screen, rect_ui, resp_tools):

        self.screen = screen
        self.rect_ui = rect_ui
        self.resp = resp_tools
        self.BASE_DIR = os.path.dirname(__file__)

        self.NOTIF_SONG_PATH = os.path.join(self.BASE_DIR, "sound", "notif.wav")

        self.notif_sound = pygame.mixer.Sound(self.NOTIF_SONG_PATH)
        self.notif_sound.set_volume(0.2)

        self.file = []
        self.active_message = "< Aucune Notification ... >"

        # Machine à écrire
        self.current_display = ""
        self.char_index = 0
        self.typing_speed = 15
        self.last_char_time = pygame.time.get_ticks()
        self.is_typing = True

        self.BASE_DIR = os.path.dirname(__file__)

        self.FONT_PATH = os.path.join(self.BASE_DIR, "font", "font_retro2.ttf")

        self.font = None
        self.lines = []

    def ajouter(self, message):
        self.file.append(message)
        self.notif_sound.play()

    def update(self):

        if self.file:
            self.active_message = self.file.pop(0)
            self.current_display = ""
            self.char_index = 0
            self.is_typing = True

        # Machine à écrire
        if self.is_typing:
            now = pygame.time.get_ticks()

            if now - self.last_char_time > self.typing_speed:
                self.last_char_time = now

                if self.char_index < len(self.active_message):
                    self.current_display += self.active_message[self.char_index]
                    self.char_index += 1
                else:
                    self.is_typing = False

        self._update_text_layout()

    # Adaptation taille + retour ligne auto

    def _update_text_layout(self):

        rect = self.rect_ui.rect
        max_width = rect.width * 0.9
        max_height = rect.height * 0.8

        # Taille dynamique selon hauteur rectangle
        font_size = int(rect.height * 0.25)

        if font_size < 14:
            font_size = 14

        self.font = pygame.font.Font(self.FONT_PATH, font_size)

        words = self.current_display.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = self.font.render(test_line, True, (255,255,255))

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)
        self.lines = lines

    def draw(self):

        rect = self.rect_ui.rect

        total_height = len(self.lines) * self.font.get_height()
        start_y = rect.centery - total_height // 2

        for i, line in enumerate(self.lines):

            txt_surface = self.font.render(line, True, (255,255,255))
            txt_rect = txt_surface.get_rect(center=(rect.centerx, start_y + i * self.font.get_height()))

            self.screen.blit(txt_surface, txt_rect)