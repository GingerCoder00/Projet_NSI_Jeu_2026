import pygame
from random import randint
import os
from resp_tools import *
from save import score
import math
from ui_tools import Texte

pygame.init()

class EndGame:
    """Classe pour gérer l'écran de fin du jeu."""

    def __init__(self, screen):

        self.screen = screen

        self.width, self.height = self.screen.get_size()

        self.BASE_DIR = os.path.dirname(__file__)
        self.resp = Resp_tools(self.width, self.height)

        self.score_path = os.path.join(self.BASE_DIR, "best_score.txt")

        self.WALL_PATH = os.path.join(self.BASE_DIR, "sprite", "wallpaper5_v2", "wall2_0.png")
        self.EXPLOSION_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_explosion2", "sprite_explosion3_")

        self.ratio_objet = {
            "spawn_zone" : (0.2, 0.2, 0.6, 0.8),
            "Texte_Temps" : (0.15, 0.15, 0.4),
            "Texte_Incendie" : (0.15, 0.3, 0.15),
            "Texte_Polluee" : (0.15, 0.4, 0.15),
            "Texte_Brulee" : (0.15, 0.5, 0.15),
            "Texte_Usine" : (0.15, 0.6, 0.15),
            "Texte_Desinformation" : (0.15, 0.7, 0.15),
            "Texte_Guerre" : (0.15, 0.8, 0.15),
            "Best_Temps": (0.6, 0.17, 0.08),
            "Best_Incendie": (0.6, 0.29, 0.08),
            "Best_Polluee": (0.6, 0.39, 0.08),
            "Best_Brulee": (0.6, 0.49, 0.08),
            "Best_Usine": (0.6, 0.59, 0.08),
            "Best_Desinformation": (0.6, 0.69, 0.08),
            "Best_Guerre": (0.6, 0.79, 0.08),
        }

        self.dico_stats = {}

        self.spawn_zone = self.resp.resp(self.ratio_objet["spawn_zone"][0], self.ratio_objet["spawn_zone"][1], self.ratio_objet["spawn_zone"][2], self.ratio_objet["spawn_zone"][3])
        
        # Arrière-plan
        self.bg_image = pygame.image.load(self.WALL_PATH).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        # Liste d'explosions
        self.explosions = []

        # Préparer les explosions
        self.explosion_sprites_path = self.EXPLOSION_PATH
        self.explosion_frames = 23

        # Charger toutes les frames pour les réutiliser
        self.explosion_images = [pygame.image.load(f"{self.explosion_sprites_path}{str(i).zfill(2)}.png").convert_alpha() for i in range(self.explosion_frames)]

        # Horloge pour gérer les spawn
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0
        self.spawn_interval = 0.3  # secondes entre les explosions

        # Timer global
        self.total_time = 0
        self.overlay_alpha = 0
        self.overlay_active = False
        self.overlay_done = False

        # Surface overlay noir
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.overlay_alpha)

        self.score_saved = False
        self.new_records = {}  # Pour savoir quelles stats ont battu un record

        # Boutons ou actions
        self.running = True
        self.return_to_menu = False

    def create_stat_ui(self):

        self.dico_stats = {}

        mapping = {
            "temps": ("Texte_Temps", "Best_Temps"),
            "incendie_declaree": ("Texte_Incendie", "Best_Incendie"),
            "case_polluees": ("Texte_Polluee", "Best_Polluee"),
            "arbre_brules": ("Texte_Brulee", "Best_Brulee"),
            "usine_creee": ("Texte_Usine", "Best_Usine"),
            "desinformation_creee": ("Texte_Desinformation", "Best_Desinformation"),
            "guerre_declaree": ("Texte_Guerre", "Best_Guerre"),
        }

        index = 0

        for key, value in score.items():

            if key not in mapping:
                continue

            text_ratio, best_ratio = mapping[key]

            # Position texte principal
            position = self.resp.resp_text(
                self.ratio_objet[text_ratio][0],
                self.ratio_objet[text_ratio][1]
            )

            size = self.resp.resp_font(
                self.ratio_objet[text_ratio][0],
                self.ratio_objet[text_ratio][2]
            )

            self.dico_stats[index] = {"text": Texte(self.screen, position, size, (255,255,255), f"{key.upper()} : {value}",font_type="font/font_retro.ttf")
            }

            # BEST SCORE responsive
            if key in self.new_records:

                best_position = self.resp.resp_text(
                    self.ratio_objet[best_ratio][0],
                    self.ratio_objet[best_ratio][1]
                )

                best_size = self.resp.resp_font(
                    self.ratio_objet[best_ratio][0],
                    self.ratio_objet[best_ratio][2]
                )

                self.dico_stats[index]["best"] = Texte(
                    self.screen,
                    best_position,
                    best_size,
                    [255,215,0],
                    "BEST !",
                    sin_effect=True,
                    font_type="font/font_retro.ttf"
                )

            index += 1

    def load_best_score_from_file(self):
        best_score_file = {}

        if not os.path.exists(self.score_path):
            return None

        with open(self.score_path, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=")

                    # Convertir en float si c'est un nombre décimal, sinon en int
                    try:
                        if "." in value:
                            best_score_file[key] = float(value)
                        else:
                            best_score_file[key] = int(value)
                    except ValueError:
                        best_score_file[key] = 0  # valeur par défaut en cas de problème

        return best_score_file
    
    def write_best_score_file(self):

        with open(self.score_path, "w") as f:
            for key, value in score.items():
                f.write(f"{key}={value}\n")

    def update_best_score_file(self):

        current_best = self.load_best_score_from_file()

        # Si aucun fichier → tout est record
        if current_best is None:
            self.new_records = {k: True for k in score}
            self.write_best_score_file()
            return

        updated = False
        self.new_records = {}

        for key in score:

            old_value = current_best.get(key, 0)
            new_value = score[key]

            if key == "temps":
                if new_value < old_value:
                    updated = True
                    self.new_records[key] = True
            elif new_value > old_value:
                updated = True
                self.new_records[key] = True

        if updated:
            self.write_best_score_file()

    def spawn_explosion(self, count = 3):
        """Fait apparaître plusieurs explosions à un endroit aléatoire dans la zone."""
        x_min, y_min, x_max, y_max = self.spawn_zone
        for _ in range(count):
            x = randint(int(x_min), int(x_max))
            y = randint(int(y_min), int(y_max))

            explosion = {
                "pos": (x, y),
                "frame": 0,
                "finished": False,
                "frame_timer": 0,  # Pour contrôler la vitesse d'animation
                "frame_delay": 0.12  # secondes entre chaque frame (plus lent)
            }
            self.explosions.append(explosion)

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.return_to_menu = True

    def update(self, dt):

        # Temps total écoulé
        self.total_time += dt

        # Activation overlay après 5 secondes
        if self.total_time >= 5:
            self.overlay_active = True
        
        if self.overlay_active:
            if self.overlay_alpha < 200:
                self.overlay_alpha += 60 * dt
                if self.overlay_alpha >= 200:
                    self.overlay_alpha = 200
                    self.overlay_done = True
                self.overlay.set_alpha(int(self.overlay_alpha))

        # Spawn automatique des explosions
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_explosion()
            self.spawn_timer = 0

        if self.overlay_done and not self.score_saved:
            self.update_best_score_file()
            self.create_stat_ui()
            self.score_saved = True

        # Update des explosions
        for explosion in self.explosions:
            explosion["frame_timer"] += dt
            if explosion["frame_timer"] >= explosion["frame_delay"]:
                explosion["frame_timer"] = 0
                if explosion["frame"] < self.explosion_frames - 1:
                    explosion["frame"] += 1
                else:
                    explosion["finished"] = True

        self.explosions = [elt for elt in self.explosions if not elt["finished"]]

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        for explosion in self.explosions:
            img = self.explosion_images[explosion["frame"]]
            rect = img.get_rect(center=explosion["pos"])
            self.screen.blit(img, rect)

        # Overlay noir progressive
        if self.overlay_active:
            self.screen.blit(self.overlay, (0, 0))

            if self.overlay_done:
                for index in self.dico_stats:
                    self.dico_stats[index]["text"].update()

                    if "best" in self.dico_stats[index]:
                        self.dico_stats[index]["best"].update()

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # delta time en secondes
            self.update(dt)
            self.draw()
            self.exit()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
    Long = screen_taille.current_w # On récupère la longueur de l'écran
    larg = screen_taille.current_h # On récupère la hauteur de l'écran

    screen = pygame.display.set_mode((Long, larg)) # On initialise l'écran avec les dimensions préalablement récupérer
    pygame.display.set_caption("Let's Smash Up The Earth") # On donne un nom à la fenêtre

    end_game = EndGame(screen)
    end_game.run()