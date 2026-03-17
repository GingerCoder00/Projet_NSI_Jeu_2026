# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
import os
from random import randint, random, shuffle
from phrases_notif import PHRASES_METEO
from animation import Animation
from dico_info_game import *
import math

class Meteo:

    def __init__(self, screen, zone_grille_x, zone_grille_y, zone_largeur, zone_hauteur, plan_ref, data, grille, flamme, notification, dico_UI_anim, dico_UI_interact):

        self.screen = screen
        self.plan_ref = plan_ref
        self.data = data
        self.grille = grille
        self.flamme = flamme
        self.notif = notification
        self.animation = Animation(screen, plan_ref, dico_UI_anim, grille)
        self.dico_UI_interact = dico_UI_interact
        self.dico_info = Dico_info_Game()

        self.zone_x = zone_grille_x
        self.zone_y = zone_grille_y
        self.zone_L = zone_largeur
        self.zone_l = zone_hauteur

        self.start_time = pygame.time.get_ticks()
        self.last_frame = pygame.time.get_ticks()
        self.last_event = pygame.time.get_ticks()

        self.BASE_DIR = os.path.dirname(__file__)

        # PLUIE SPRITES
        self.RAIN_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_effet_pluie", "sprite_pluie_")
        self.sprite_pluie = [pygame.transform.scale(elt, (self.zone_L, self.zone_l)) for elt in [pygame.image.load(f"{self.RAIN_PATH}{str(i).zfill(2)}.png").convert() for i in range(23)]]
        self.pluie_frame = 0

        # SOLEIL SPRITES
        self.SUN_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_effet_canicule", "sprite_effet_canicule_")
        self.sprite_sun = [pygame.transform.scale(elt, (self.zone_L, self.zone_l)) for elt in [pygame.image.load(f"{self.SUN_PATH}{i}.png").convert() for i in range(1)]]

        # GEL SPRITES
        self.GEL_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_effet_gel", "sprite_effet_gel_")
        self.sprite_gel = [pygame.transform.scale(elt, (self.zone_L, self.zone_l)) for elt in [pygame.image.load(f"{self.GEL_PATH}{i}.png").convert() for i in range(1)]]

        # ECLAIR SPRITES
        self.sprite_eclair = [os.path.join(self.BASE_DIR, "sprite", "sprite_eclair", f"sprite_eclair_{i}.png") for i in range(4)]

        self.flash_surface = pygame.Surface((self.zone_L, self.zone_l))
        self.flash_surface.fill((255,255,255))  

        # METEORITE SPRITES
        self.sprite_meteorite = [os.path.join(self.BASE_DIR, "sprite", "sprite_meteorite", f"sprite_meteorite_{str(i).zfill(2)}.png") for i in range(18)]
        self.meteorite_spawn = False
        self.flag_flash = False
        self.meteorite_anim_id = None

        # TORNADE SPRITES
        self.sprite_tornade = [os.path.join(self.BASE_DIR, "sprite", "sprite_tornade", f"sprite_tornade_{str(i).zfill(2)}.png") for i in range(6)]
        self.tornade_spawn = False

        # Tornade mouvement
        self.tornade_move_delay = 250  # ms entre chaque case
        
        # Animation tornade
        self.tornade_frames = [pygame.transform.scale(elt, (self.grille.case_Long * 5, self.grille.case_larg * 5)) for elt in [pygame.image.load(i).convert_alpha() for i in self.sprite_tornade]]
        self.tornade_last_frame = 0
        self.tornade_frame_delay = 80

        self.reforestation_done = False
        self.inondation_done = False
        self.secheresse_done = False

        # IMAGES EPIDEMIE 
        self.EPIDEMIE_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_emoji2", "sprite_emoji2_")
        self.sprite_epidemie = [pygame.image.load(f"{self.EPIDEMIE_PATH}{i}.png").convert_alpha() for i in range(4)]

        # IMAGES ECOLOGISTE 
        self.ECO_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_emoji", "sprite_emoji_")
        self.sprite_eco = [pygame.image.load(f"{self.ECO_PATH}{i}.png").convert_alpha() for i in range(4)]

        # Particules
        self.image_particles = []
        self.spawn_timer = 0
        self.spawn_delay = 300
        self.particle_lifetime = 4000

        # Gestion des événements
        self.epidemie_active = True  # True si tu veux déclencher l'épidémie
        self.intervention_ecologiste_active = True  # True si tu veux déclencher l'intervention écolo

        # ÉTATS
        self.current_event = None
        self.event_duration = 9500

        self.pluie_active = False
        self.canicule_active = False
        self.gel_active = False
        self.orage_active = False
        self.tornade_active = False
        self.inondation_active = False
        self.reforestation_active = False
        self.intervention_ecologiste_active = False
        self.secheresse_ciblee_active = False
        self.epidemie_active = False
        self.meteorite_active = False
        self.nuage_active = False

        # Orage visuel
        self.flash_alpha = 0

        self.events = [
                ["pluie", 0.4, PHRASES_METEO[0]],
                ["canicule", 0.4, PHRASES_METEO[1]],
                ["gel", 0.4, PHRASES_METEO[2]],
                ["orage", 0.5, PHRASES_METEO[3]],
                ["tornade", 0.5, PHRASES_METEO[4]],
                ["inondation", 0.4, PHRASES_METEO[5]],
                ["reforestation", 0.6, PHRASES_METEO[6]],
                ["intervention ecologiste", 0.4, PHRASES_METEO[7]],
                ["sécheresse ciblée", 0.6, PHRASES_METEO[8]],
                ["epidemie", 0.4, PHRASES_METEO[9]],
                ["météorite", 0.15, PHRASES_METEO[10]],
                [None, 1]
            ]
        
        # Coefficients par événement : +1 = augmente la probabilité, -1 = la diminue
        self.event_coeffs = {
            "epidemie": {"pollution": 0.01, "biodiversite": -0.005},   # pollution → épidémie
            "intervention ecologiste": {"pollution": -0.01, "biodiversite": 0.01}, # pollution → intervention
            "canicule": {"temperature": 0.02, "eau": -0.01},
            "inondation": {"eau": 0.02},
            "sécheresse ciblée": {"eau": -0.02},
            "reforestation": {"biodiversite": 0.01},
            "pluie": {"eau": 0.01},
            "gel": {"temperature": -0.02},
            "orage": {"temperature": 0.01, "eau": 0.01},
            "tornade": {"stabilite": -0.01},
            "météorite": {}  # événement rare, reste fixe
        }

        self.event_effects = {
            "pluie": {"eau": 6, "biodiversite": 5, "pollution": -4},
            "canicule": {"temperature": 5, "eau": -6, "biodiversite": -3},
            "gel": {"temperature": -5, "eau": -4, "biodiversite": -3},
            "orage": {"stabilite": -5},
            "tornade": {"stabilite": -5, "temperature": -2, "destruction": -3},
            "inondation": {"temperature": -1.5, "stabilite": -2, "eau": 3},
            "reforestation": {"biodiversite": 3, "stabilite": 2, "augmentation_profit": -3},
            "intervention ecologiste": {"biodiversite": 8, "profit": -5, "augmentation_profit": -10.5},
            "sécheresse ciblée": {"eau": -5},
            "epidemie": {"pollution": 3, "eau": -2, "profit": -8.5, "augmentation_profit": -5},
            "météorite": {"stabilite": -8, "destruction": -5, "pollution": -4, "profit": -10}
        }
        
    def calculer_prob_event(self, event_name):
        # Récupérer la proba de base
        base_prob = next((elt[1] for elt in self.events if elt[0] == event_name), 0)
        
        # Ajuster selon les jauges
        coeffs = self.event_coeffs.get(event_name, {})
        modif = 0
        for jauge, coef in coeffs.items():
            valeur = getattr(self, jauge)
            modif += coef * valeur  # valeur de la jauge * coefficient

        prob_finale = max(0, min(1, base_prob + modif))
        return prob_finale
    
    def appliquer_effets(self):
        if self.current_event in self.event_effects:
            effets = self.event_effects[self.current_event]
            for jauge, valeur in effets.items():
                if hasattr(self, jauge):
                    setattr(self, jauge, getattr(self, jauge) + valeur)

    def update_event(self):
        now = pygame.time.get_ticks()

        # On ne fait rien si l'événement actuel n'est pas encore terminé
        # ou s'il y a déjà une tornade ou une météorite en cours
        if now - self.last_event <= self.event_duration or self.tornade_active or self.meteorite_active:
            return

        # On note le moment où l'on déclenche un nouvel événement
        self.last_event = now

        # On choisit un événement au hasard dans la liste
        index_event = randint(0, len(self.events) - 1)
        self.current_event = self.events[index_event][0]

        # Vérifier si l'événement se déclenche selon sa probabilité
        if random() >= self.events[index_event][1]:
            # L'événement ne se déclenche pas
            self.current_event = None
            return

        # On met à jour l'état de chaque événement (vrai si c'est l'événement actuel, sinon faux)
        self.pluie_active = (self.current_event == "pluie")
        self.canicule_active = (self.current_event == "canicule")
        self.gel_active = (self.current_event == "gel")
        self.orage_active = (self.current_event == "orage")
        self.tornade_active = (self.current_event == "tornade")
        self.inondation_active = (self.current_event == "inondation")
        self.reforestation_active = (self.current_event == "reforestation")
        self.intervention_ecologiste_active = (self.current_event == "intervention ecologiste")
        self.secheresse_ciblee_active = (self.current_event == "sécheresse ciblée")
        self.epidemie_active = (self.current_event == "epidemie")
        self.meteorite_active = (self.current_event == "météorite")

        # Réinitialiser les flags et compteurs pour certains événements
        if not self.tornade_active:
            self.tornade_spawn = False
        if self.inondation_active:
            self.inondation_done = False
        if self.reforestation_active:
            self.reforestation_done = False
        if self.secheresse_ciblee_active:
            self.secheresse_done = False
        if not self.meteorite_active:
            self.meteorite_spawn = False
        if self.meteorite_active:
            self.flag_flash = False

        # Afficher la phrase de notification si elle existe
        try:
            phrase = self.events[index_event][2]
            self.notif.ajouter(phrase)
        except:
            pass

        # Affichage dans la console pour suivre les événements
        print(f"Evénement actif : {self.current_event} à {round((now - self.start_time) / 1000, 2)} secondes")

    def pluie(self):

        if not self.pluie_active:
            return

        now = pygame.time.get_ticks()
        rain_delay = 30

        if now - self.last_frame >= rain_delay:
            self.pluie_frame = (self.pluie_frame + 1) % len(self.sprite_pluie)
            self.last_frame = now

        image = self.sprite_pluie[self.pluie_frame]
        image.set_alpha(120)
        self.screen.blit(image, (self.zone_x, self.zone_y))

    def canicule(self):

        if not self.canicule_active:
            return

        image = self.sprite_sun[0]
        image.set_alpha(120)
        self.screen.blit(image, (self.zone_x, self.zone_y))

    def orage(self):

        if not self.orage_active:
            return

        # Flash visuel
        if random() < 0.038:
            self.flash_alpha = 150

            # Chance de déclencher un feu
            if random() < 0.35:
                ligne = randint(0, self.grille.lignes - 1)
                colonne = randint(0, self.grille.colonnes - 1)

                if not self.grille.grille[ligne][colonne] == (0,0,255):
                    self.animation.ajouter_animation(self.sprite_eclair, self.animation.scale(6, ligne, colonne, from_top = 0.4)[1], self.animation.scale(6, ligne, colonne, from_top = 0.4)[0], frame_delay = 90)
                    self.flamme.propagation_feu(ligne, colonne, puissance = 3, spawn_anim=False)

        if self.flash_alpha > 0:
            self.flash_surface.set_alpha(self.flash_alpha)
            self.screen.blit(self.flash_surface, (self.zone_x, self.zone_y))
            self.flash_alpha -= 10

    def gel(self):

        if not self.gel_active:
            return

        image = self.sprite_gel[0]
        image.set_alpha(120)
        self.screen.blit(image, (self.zone_x, self.zone_y))

    def tornade(self):

        if not self.tornade_active:
            self.tornade_spawn = False
            return

        now = pygame.time.get_ticks()

        # SPAWN UNE SEULE FOIS
        if not self.tornade_spawn:

            self.tornade_ligne = randint(2, self.grille.lignes - 3)

            if random() < 0.5:
                self.tornade_direction = 1
                self.tornade_colonne = 0
            else:
                self.tornade_direction = -1
                self.tornade_colonne = self.grille.colonnes - 1

            self.tornade_last_move = now
            self.tornade_frame_index = 0
            self.tornade_spawn = True

        # Animation
        if now - self.tornade_last_frame > self.tornade_frame_delay:
            self.tornade_frame_index = (self.tornade_frame_index + 1) % len(self.tornade_frames)
            self.tornade_last_frame = now

        # Déplacement
        if now - self.tornade_last_move > self.tornade_move_delay:

            self.tornade_colonne += self.tornade_direction
            self.tornade_last_move = now

            if self.tornade_colonne < 0 or self.tornade_colonne >= self.grille.colonnes:
                self.tornade_active = False
                self.tornade_spawn = False
                return

        # Impact 5x5
        for i in range(-2, 3):
            for j in range(-2, 3):

                ligne = self.tornade_ligne + i
                colonne = self.tornade_colonne + j

                if 0 <= ligne < self.grille.lignes and 0 <= colonne < self.grille.colonnes:
                    if self.grille.grille[ligne][colonne] == "usine":
                        self.flamme.detruire_usine(ligne, colonne)

        # Affichage
        x, y = self.grille.placement_grille(self.tornade_colonne - 2, self.tornade_ligne - 4)
        self.screen.blit(self.tornade_frames[self.tornade_frame_index], (x, y))

    def meteorite(self):

        if not self.meteorite_active:
            return

        # SPAWN UNE SEULE FOIS
        if not self.meteorite_spawn:

            max_attempts = 50
            attempts = 0

            while attempts < max_attempts:
                self.meteorite_ligne = randint(2, self.grille.lignes - 3)
                self.meteorite_colonne = randint(2, self.grille.colonnes - 3)

                if self.grille.grille[self.meteorite_ligne][self.meteorite_colonne] != (0,0,255):
                    break

                attempts += 1

            self.meteorite_anim_id = self.animation.ajouter_animation(self.sprite_meteorite, self.animation.scale(9, self.meteorite_ligne, self.meteorite_colonne, from_top=0.4)[1], self.animation.scale(9, self.meteorite_ligne, self.meteorite_colonne, from_top=0.4)[0], frame_delay=90)

            self.meteorite_spawn = True
            self.flag_flash = False

        # Si animation supprimée → stop
        if self.meteorite_anim_id not in self.animation.animations:
            self.meteorite_active = False
            self.meteorite_spawn = False
            return

        anim = self.animation.animations[self.meteorite_anim_id]
        current_frame = anim.frame_index

        # IMPACT FRAME 8
        if current_frame >= 8 and not self.flag_flash:

            self.flash_alpha = 200
            self.flag_flash = True

            for i in range(-2, 3):
                for j in range(-2, 3):

                    ligne = self.meteorite_ligne + i
                    colonne = self.meteorite_colonne + j

                    if 0 <= ligne < self.grille.lignes and 0 <= colonne < self.grille.colonnes:
                        self.flamme.propagation_feu(ligne, colonne, puissance = 2, spawn_anim=False)

        # FLASH
        if self.flash_alpha > 0:
            self.flash_surface.set_alpha(self.flash_alpha)
            self.screen.blit(self.flash_surface, (self.zone_x, self.zone_y))

            self.flash_alpha -= 15

    def reforestation_naturelle(self):
        if not self.reforestation_active or self.reforestation_done:
            return

        # Récupérer toutes les cases herbe adjacentes à une forêt
        candidates = []

        for ligne in range(self.grille.lignes):
            for colonne in range(self.grille.colonnes):
                if self.grille.grille[ligne][colonne] == (0,255,0):
                    voisins = [(ligne-1, colonne), (ligne+1, colonne), (ligne, colonne-1), (ligne, colonne+1)]
                    for vl, vc in voisins:
                        if 0 <= vl < self.grille.lignes and 0 <= vc < self.grille.colonnes:
                            if self.grille.grille[vl][vc] == (0,50,0):  # forêt
                                candidates.append((ligne, colonne))
                                break

        if not candidates:
            return

        shuffle(candidates)
        cases_a_changer = candidates[:randint(4,8)]

        for ligne, colonne in cases_a_changer:
            case_id = ligne * self.grille.colonnes + colonne
            case_obj = self.dico_UI_interact[0]["Case"].get(case_id)
            if case_obj:
                sprites = self.dico_info.type_cases[(0,50,0)]
                case_obj.img_base = pygame.image.load(sprites[randint(0, (len(sprites)) - 1)]).convert_alpha()
                self.grille.grille[ligne][colonne] = (0,50,0)

        self.reforestation_done = True  # Marquer comme fait pour cet événement

    def inondation(self):

        if not self.inondation_active or self.inondation_done:
            return

        # Récupérer toutes les cases herbe adjacentes à la mer
        candidates = []

        for ligne in range(self.grille.lignes):
            for colonne in range(self.grille.colonnes):
                if self.grille.grille[ligne][colonne] in [(0,255,0), (0,50,0), "usine"]:
                    voisins = [(ligne-1, colonne), (ligne+1, colonne), (ligne, colonne-1), (ligne, colonne+1)]
                    for vl, vc in voisins:
                        if 0 <= vl < self.grille.lignes and 0 <= vc < self.grille.colonnes:
                            if self.grille.grille[vl][vc] == (0,0,255):  # eau
                                candidates.append((ligne, colonne))
                                break

        if not candidates:
            return

        shuffle(candidates)
        cases_a_changer = candidates[:randint(4,8)]

        for ligne, colonne in cases_a_changer:
            case_id = ligne * self.grille.colonnes + colonne
            case_obj = self.dico_UI_interact[0]["Case"].get(case_id)
            if case_obj:
                if self.grille.grille[ligne][colonne] == "usine":
                    self.flamme.detruire_usine(ligne, colonne)
                sprites = self.dico_info.type_cases[(0,0,255)]
                case_obj.img_base = pygame.image.load(sprites[randint(0, (len(sprites)) - 1)]).convert_alpha()
                self.grille.grille[ligne][colonne] = (0,0,255)

        self.inondation_done = True  # Marquer comme fait pour cet événement

    def secheresse_naturelle(self):

        if not self.secheresse_ciblee_active or self.secheresse_done:
            return

        # Récupérer toutes les cases herbe adjacentes à une forêt
        candidates = []

        for ligne in range(self.grille.lignes):
            for colonne in range(self.grille.colonnes):
                if self.grille.grille[ligne][colonne] == (0,0,255):
                    voisins = [(ligne-1, colonne), (ligne+1, colonne), (ligne, colonne-1), (ligne, colonne+1)]
                    for vl, vc in voisins:
                        if 0 <= vl < self.grille.lignes and 0 <= vc < self.grille.colonnes:
                            if self.grille.grille[vl][vc] in [(0,50,0), (0,255,0)]:  # forêt et herbe
                                candidates.append((ligne, colonne))
                                break

        if not candidates:
            return

        shuffle(candidates)
        cases_a_changer = candidates[:randint(4,8)]

        for ligne, colonne in cases_a_changer:
            case_id = ligne * self.grille.colonnes + colonne
            case_obj = self.dico_UI_interact[0]["Case"].get(case_id)
            if case_obj:
                sprites = self.dico_info.type_cases[(0,255,0)]
                case_obj.img_base = pygame.image.load(sprites[randint(0, (len(sprites)) - 1)]).convert_alpha()
                self.grille.grille[ligne][colonne] = (0,255,0)

        self.secheresse_done = True  # Marquer comme fait pour cet événement

    def epidemie(self):

        if not self.epidemie_active:
            return
        
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = now

            # Créer une particule épidémie
            base_image = self.sprite_epidemie[randint(0, len(self.sprite_epidemie) - 1)]
            ligne = randint(0, self.grille.lignes - 1)
            colonne = randint(0, self.grille.colonnes - 1)
            x, y = self.grille.placement_grille(colonne, ligne)
            scale = random() * 0.8 + 0.4
            image = pygame.transform.smoothscale(base_image, (int(base_image.get_width() * scale), int(base_image.get_height() * scale)))
            image.set_alpha(randint(100, 170))
            self.image_particles.append({
                "type": "epidemie",
                "image": image,
                "x": x + self.grille.case_Long // 2,
                "y": y + self.grille.case_larg // 2,
                "angle_offset": random() * math.pi,
                "birth": now
            })

        # Affichage des particules épidémie
        for particle in self.image_particles[:]:
            if particle["type"] != "epidemie":
                continue
            age = now - particle["birth"]
            angle = 15 * math.sin(now * 0.003 + particle["angle_offset"])
            rotated = pygame.transform.rotate(particle["image"], angle)
            rect = rotated.get_rect(center=(particle["x"], particle["y"]))
            self.screen.blit(rotated, rect)
            if age > self.particle_lifetime:
                self.image_particles.remove(particle)

    def intervention_ecologiste(self):

        if not self.intervention_ecologiste_active:
            return

        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = now

            # Créer une particule intervention écolo
            base_image = self.sprite_eco[randint(0, len(self.sprite_eco) - 1)]
            ligne = randint(0, self.grille.lignes - 1)
            colonne = randint(0, self.grille.colonnes - 1)
            x, y = self.grille.placement_grille(colonne, ligne)
            scale = random() * 0.8 + 0.4
            image = pygame.transform.smoothscale(base_image, (int(base_image.get_width() * scale), int(base_image.get_height() * scale)))
            image.set_alpha(randint(100, 170))
            self.image_particles.append({
                "type": "ecolo",
                "image": image,
                "x": x + self.grille.case_Long // 2,
                "y": y + self.grille.case_larg // 2,
                "angle_offset": random() * math.pi,
                "birth": now
            })

        # Affichage des particules écolo
        for particle in self.image_particles[:]:
            if particle["type"] != "ecolo":
                continue
            age = now - particle["birth"]
            angle = 15 * math.sin(now * 0.003 + particle["angle_offset"])
            rotated = pygame.transform.rotate(particle["image"], angle)
            rect = rotated.get_rect(center=(particle["x"], particle["y"]))
            self.screen.blit(rotated, rect)
            if age > self.particle_lifetime:
                self.image_particles.remove(particle)

    def update(self):
        self.update_event()

        self.appliquer_effets()  # <-- applique les jauges

        self.pluie()
        self.canicule()
        self.gel()
        self.orage()
        self.tornade()
        self.meteorite()
        self.reforestation_naturelle()
        self.inondation()
        self.secheresse_naturelle()
        self.intervention_ecologiste()
        self.epidemie()