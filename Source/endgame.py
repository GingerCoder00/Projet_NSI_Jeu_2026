# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from random import randint
import os
from resp_tools import *
from save import score
from ui_tools import Texte, UI_screen
from notification import *
from phrases_notif import PHRASES_FIN_DE_JEU

pygame.init()
pygame.mixer.init()

class EndGame:
    '''Cette classe permet de gérer l'écran de fin de jeu'''

    def __init__(self, screen):

        self.screen = screen

        self.width, self.height = self.screen.get_size()

        self.BASE_DIR = os.path.dirname(__file__)
        self.resp = Resp_tools(self.width, self.height)

        # On importe les médias une fois au début

        self.MUSIC_END_PATH = os.path.join(self.BASE_DIR, "sound", "music_end.wav")
        pygame.mixer.music.load(self.MUSIC_END_PATH)
        pygame.mixer.music.set_volume(0.7)

        self.GLITCH_SFX_PATH1 = os.path.join(self.BASE_DIR, "sound", "glitch1.mp3")
        self.flag_glitch1 = False
        self.glitch1 = pygame.mixer.Sound(self.GLITCH_SFX_PATH1)
        self.glitch1.set_volume(0.05)

        self.CLAP_SFX_PATH = os.path.join(self.BASE_DIR, "sound", "clap1.mp3")
        self.flag_clap = False
        self.clap = pygame.mixer.Sound(self.CLAP_SFX_PATH)
        self.clap.set_volume(0.14)

        self.EXPLOSION_SFX_PATH = [os.path.join(self.BASE_DIR, "sound", f"explosion{i}.wav") for i in range(5)]

        self.WALL_PATH = os.path.join(self.BASE_DIR, "sprite", "wallpaper_hub", "sprite_wallpaper_hub_0.png")
        self.EXPLOSION_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_explosion2", "sprite_explosion3_")
        
        self.flag_music = False

        # Importation du fichier qui sauvegarde les meilleurs scores
        self.score_path = os.path.join(self.BASE_DIR, "best_score.txt")

        self.rect_notif_fin = UI_screen(self.screen, (0,0,0), (0,0,0), (0,0, self.width, self.height), pulse = False)  # Création d'un zone de notif

        self.notification = Notification_gestion(self.screen, self.rect_notif_fin, (255, 255, 255), font_size_ratio = 0.08, diff_y = 25, volume_sound = 0) # Création du gestionnaire de Notification

        # Dictionnaire sauvegardant les ratios de tous les objets graphique présent dans le EndGame
        self.ratio_objet = {
            "spawn_zone" : (0.2, 0.2, 0.6, 0.8),
            "Texte_Temps" : (0.135, 0.07, 0.5),
            "Texte_Incendie" : (0.15, 0.3, 0.15),
            "Texte_Polluee" : (0.15, 0.4, 0.15),
            "Texte_Brulee" : (0.15, 0.5, 0.15),
            "Texte_Usine" : (0.15, 0.6, 0.15),
            "Texte_Desinformation" : (0.15, 0.7, 0.15),
            "Texte_Guerre" : (0.15, 0.8, 0.15),
            "Best_Temps": (0.78, 0.13, 0.08),
            "Best_Incendie": (0.7, 0.29, 0.08),
            "Best_Polluee": (0.7, 0.39, 0.08),
            "Best_Brulee": (0.7, 0.49, 0.08),
            "Best_Usine": (0.7, 0.59, 0.08),
            "Best_Desinformation": (0.7, 0.69, 0.08),
            "Best_Guerre": (0.7, 0.79, 0.08),
        }

        # On remplira ce dico pour stocker les insatnce de UI_PNG qui permettront d'afficher chaque stats de la partie
        self.dico_stats = {}

        # On créé une zone de spawn pour les explosions de la terre
        self.spawn_zone = self.resp.resp(self.ratio_objet["spawn_zone"][0], self.ratio_objet["spawn_zone"][1], self.ratio_objet["spawn_zone"][2], self.ratio_objet["spawn_zone"][3])
        
        # Arrière-plan
        self.bg_image = pygame.image.load(self.WALL_PATH).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        # Liste d'explosions
        self.explosions = []

        self.flag_explosion = False

        # Préparer les explosions
        self.explosion_sprites_path = self.EXPLOSION_PATH
        self.explosion_frames = 23

        # Charger toutes les frames pour les réutiliser
        self.explosion_images = [pygame.image.load(f"{self.explosion_sprites_path}{str(i).zfill(2)}.png").convert_alpha() for i in range(self.explosion_frames)]

        # Horloge pour gérer les spawn
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0
        self.spawn_interval = 0.3  # Secondes entre les explosions

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

        self.stats_timer = 0
        self.glitch_active = False
        self.glitch_timer = 0
        self.notif_started = False

        self.micro_glitch_timer = 0
        self.micro_glitch_interval = 0.1  # Intervalle moyen entre glitchs
        self.micro_glitch_duration = 0.05  # Durée d'un micro-glitch
        self.micro_glitch_active = False

        self.phrase_index = 0
        self.phrase_timer = 0
        self.phrase_duration = 4 # Durée d'une phrase
        self.sequence_started = False
        self.sequence_finished = False

    def create_stat_ui(self):
        '''
        Cette méthode permet de créer les instances d'affichage des stats de la partie
        '''

        mapping = {
            "temps": ("Texte_Temps", "Best_Temps"),
            "incendie_declaree": ("Texte_Incendie", "Best_Incendie"),
            "case_polluees": ("Texte_Polluee", "Best_Polluee"),
            "arbre_brules": ("Texte_Brulee", "Best_Brulee"),
            "usine_creee": ("Texte_Usine", "Best_Usine"),
            "desinformation_creee": ("Texte_Desinformation", "Best_Desinformation"),
            "guerre_declaree": ("Texte_Guerre", "Best_Guerre"),
        }

        dico_name = {
            "temps": "temps",
            "incendie_declaree": "incendies déclarés",
            "case_polluees": "cases polluées",
            "arbre_brules": "arbres brûlés",
            "usine_creee": "usines créées",
            "desinformation_creee": "désinformations divulguées",
            "guerre_declaree": "guerres déclarées",
        }

        index = 0

        for key, value in score.items():

            if key not in mapping:
                continue

            text_ratio, best_ratio = mapping[key]

            # Positionnement et création des texte de stats
            position = self.resp.resp_text(self.ratio_objet[text_ratio][0], self.ratio_objet[text_ratio][1])

            size = self.resp.resp_font(self.ratio_objet[text_ratio][0], self.ratio_objet[text_ratio][2])

            self.dico_stats[index] = {"text": Texte(self.screen, position, size, (255,255,255), f"{dico_name[key].capitalize()} : {value}",font_type="font/retro_notif.ttf")}

            # Positionnement et création des texte "BEST SCORE"
            if key in self.new_records:

                best_position = self.resp.resp_text(self.ratio_objet[best_ratio][0], self.ratio_objet[best_ratio][1])

                best_size = self.resp.resp_font(self.ratio_objet[best_ratio][0], self.ratio_objet[best_ratio][2])

                self.dico_stats[index]["best"] = Texte(self.screen, best_position, best_size, [255,215,0], "BEST !", sin_effect=True, font_type="font/font_retro.ttf")

            index += 1

    def load_best_score_from_file(self):
        '''
        Cette méthode permet de lire et de stocker les informations présente dans le fichier texte best_score
        '''
        best_score_file = {}

        if not os.path.exists(self.score_path):  # On vérifie que le fichier existe pour ne pas créer de bug le cas échéant
            return None

        # Boncle de lecture du fichier texte
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
                        best_score_file[key] = 0  # Valeur par défaut en cas de problème

        return best_score_file
    
    def write_best_score_file(self):
        '''
        Cette méthode permet de mettre à jour le fichier texte avec les nouvelles meilleures stats si elles ont battus les précédentes
        '''
        # Boucle d'écriture du fichier texte
        with open(self.score_path, "w") as f: 
            for key, value in score.items():
                f.write(f"{key}={value}\n")

    def update_best_score_file(self):
        '''
        Cette méthode permet d'actualisé les meilleurs records si ils ont battus les précédents
        '''

        current_best = self.load_best_score_from_file()

        # Si aucun fichier alors par défault tout est un record
        if current_best is None:
            self.new_records = {k: True for k in score}
            self.write_best_score_file()
            return

        updated = False
        for key in score:

            old_value = current_best.get(key, 0)
            new_value = score[key]

            if key == "temps":  # Pour la stat de temps il faut faire une conparaison inverse en effet on cherche à avoir le plus petit temps possible pas le plus grand
                if new_value < old_value:
                    updated = True
                    self.new_records[key] = True
            elif new_value > old_value: # On test les anciennes et nouvelles valeurs
                updated = True
                self.new_records[key] = True

        if updated:  # On vérifie bien que le fichier a bien changé pour ne pas avoir à le modifier à chaque fois
            self.write_best_score_file()

    def spawn_explosion(self, count = 3):
        '''
        Cette méthode fait apparaître plusieurs explosions à un endroit aléatoire dans la zone prédéfie
        '''
        x_min, y_min, x_max, y_max = self.spawn_zone

        # On créé un nombre donné d'explosion à des coordonnées aléatoire dans la zone d'explosion
        for _ in range(count):
            x = randint(int(x_min), int(x_max))
            y = randint(int(y_min), int(y_max))

            explosion = {"pos": (x, y), "frame": 0, "finished": False, "frame_timer": 0, "frame_delay": 0.12} # On créer des informations sur les explosions pour pouvoir en gérer beaucoup
            self.explosions.append(explosion)

    def update(self, dt):
        ''' Cette méthode permet d'actualiser et de gérer les différents instant du plan ainsi que les effets visuels et auditifs'''

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

        if self.overlay_done and self.score_saved and not self.glitch_active:
            self.stats_timer += dt

            if self.stats_timer >= 7:
                self.glitch_active = True
        
        if self.glitch_active and not self.notif_started:
            self.glitch_timer += dt

            if self.glitch_timer >= 3.5:
                self.notif_started = True

        # Lancement de la séquence une seule fois
        if self.notif_started and not self.sequence_started:
            self.sequence_started = True
            self.phrase_index = 0
            self.phrase_timer = 0
            self.notification.ajouter(PHRASES_FIN_DE_JEU[self.phrase_index])


        # Gestion du timing des phrases
        if self.sequence_started and not self.sequence_finished:

            self.phrase_timer += dt

            if self.phrase_timer >= self.phrase_duration:
                self.phrase_timer = 0
                self.phrase_index += 1

                if self.phrase_index < len(PHRASES_FIN_DE_JEU):
                    self.notification.ajouter(PHRASES_FIN_DE_JEU[self.phrase_index])
                else:
                    self.sequence_finished = True

            # Micro-glitch aléatoire pendant les phrases
            self.micro_glitch_timer += dt
            if self.micro_glitch_timer >= self.micro_glitch_interval:
                self.micro_glitch_timer = 0
                # Tirage aléatoire pour savoir si on déclenche un glitch
                if randint(0, 2) == 1:  # 50% de chance
                    self.micro_glitch_active = True
                    self.micro_glitch_end = self.total_time + self.micro_glitch_duration

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
        if not self.flag_explosion:
            self.screen.blit(self.bg_image, (0, 0))

            for explosion in self.explosions:
                img = self.explosion_images[explosion["frame"]]
                rect = img.get_rect(center=explosion["pos"])
                if randint(1,300) == 1:
                    self.explosion = pygame.mixer.Sound(self.EXPLOSION_SFX_PATH[randint(0,2)])
                    if self.overlay_active:
                        self.explosion.set_volume(0.02) 
                    else:
                        self.explosion.set_volume(0.06) 
                    self.explosion.play()
                self.screen.blit(img, rect)

        # Overlay noir progressive
        if self.overlay_active:
            self.screen.blit(self.overlay, (0, 0))

            if self.overlay_done:
                if not self.flag_clap:
                    self.clap.play()
                    self.flag_clap = True
                for index in self.dico_stats:
                    self.dico_stats[index]["text"].update()

                    if "best" in self.dico_stats[index]:
                        self.dico_stats[index]["best"].update()

        if self.glitch_active and not self.notif_started:
            if not self.flag_glitch1:
                self.glitch1.play()
                self.flag_glitch1 = True
            for _ in range(85):
                x = randint(0, self.width)
                y = randint(0, self.height)
                w = randint(int(self.width * 0.02), int(self.width * 0.2))
                h = randint(int(self.height * 0.005), int(self.height * 0.05))
                color = (randint(150,255), randint(0,100), randint(0,100))
                pygame.draw.rect(self.screen, color, (x,y,w,h))

        if self.notif_started:
            self.flag_explosion = True
            if not self.flag_music:
                pygame.mixer.music.play(-1)
                self.flag_music = True
            self.rect_notif_fin.update()
            self.notification.update()
            self.notification.draw()

        # Micro-glitch pendant les phrases
        if self.micro_glitch_active:
            for _ in range(randint(5, 12)):  # nombre aléatoire de rectangles
                x = randint(0, self.width)
                y = randint(0, self.height)
                w = randint(int(self.width * 0.01), int(self.width * 0.15))
                h = randint(int(self.height * 0.003), int(self.height * 0.03))
                color = (randint(100,255), randint(100,255), randint(100,255))
                pygame.draw.rect(self.screen, color, (x, y, w, h))
            
            # Vérifier si le glitch doit s'arrêter
            if self.total_time >= getattr(self, 'micro_glitch_end', 0):
                self.micro_glitch_active = False

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # delta time en secondes
            self.update(dt)
            self.draw()

if __name__ == "__main__":  # Permet de démarrer le programme dans de bonnes conditions
    screen_taille = pygame.display.Info() # On récupère la taille de l'écran du système
    Long = screen_taille.current_w # On récupère la longueur de l'écran
    larg = screen_taille.current_h # On récupère la hauteur de l'écran

    screen = pygame.display.set_mode((Long, larg)) # On initialise l'écran avec les dimensions préalablement récupérer
    pygame.display.set_caption("Let's Break Down The Earth") # On donne un nom à la fenêtre

    end_game = EndGame(screen)
    end_game.run()
