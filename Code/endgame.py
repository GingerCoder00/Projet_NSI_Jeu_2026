import pygame
from random import randint
import os
from resp_tools import *
from save import score
import math

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
            "spawn_zone" : (0.2, 0.2, 0.6, 0.8)
        }

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

        # Police pour le chrono
        self.font = pygame.font.SysFont("arial", 80)
        self.best_font_base = pygame.font.SysFont("arial", 60)

        # Boutons ou actions
        self.running = True
        self.return_to_menu = False

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

        self.explosions = [e for e in self.explosions if not e["finished"]]

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
                y_offset = self.height // 2 - 150

                for key, value in score.items():

                    stat_text = f"{key} : {value}"
                    text_surface = self.font.render(stat_text, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(self.width // 2, y_offset))
                    self.screen.blit(text_surface, text_rect)

                    # Si record battu → afficher BEST SCORE !
                    if key in self.new_records:
                        pulse = 1 + 0.15 * math.sin(pygame.time.get_ticks() * 0.01)
                        size = int(60 * pulse)

                        best_font = pygame.font.SysFont("arial", size)
                        best_surface = best_font.render("BEST SCORE !", True, (255, 215, 0))
                        best_rect = best_surface.get_rect(center=(self.width // 2, y_offset + 40))
                        self.screen.blit(best_surface, best_rect)

                    y_offset += 100

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