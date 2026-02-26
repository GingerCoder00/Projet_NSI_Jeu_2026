import pygame
import os
from random import randint, random
from phrases_notif import PHRASES_METEO
from animation import Animation

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

        # ECLAIR SPRITES
        self.sprite_eclair = [os.path.join(self.BASE_DIR, "sprite", "sprite_eclair", f"sprite_eclair_{i}.png") for i in range(4)]

        # METEORITE SPRITES
        self.sprite_meteorite = [os.path.join(self.BASE_DIR, "sprite", "sprite_meteorite", f"sprite_meteorite_{str(i).zfill(2)}.png") for i in range(18)]
        self.meteorite_spawn = False
        self.flag_flash = False
        self.meteorite_anim_id = None

        # TORNADE SPRITES
        self.sprite_tornade = [os.path.join(self.BASE_DIR, "sprite", "sprite_tornade", f"sprite_tornade_{str(i).zfill(2)}.png") for i in range(14)]
        self.tornade_spawn = False

        # Tornade mouvement
        self.tornade_move_delay = 250  # ms entre chaque case
        
        # Animation tornade
        self.tornade_frames = [pygame.transform.scale(elt, (self.grille.case_Long * 5, self.grille.case_larg * 5)) for elt in [pygame.image.load(i).convert_alpha() for i in self.sprite_tornade]]
        self.tornade_last_frame = 0
        self.tornade_frame_delay = 80

        # NUAGE SPRITES
        self.sprite_nuage = [os.path.join(self.BASE_DIR, "sprite", "sprite_nuage", f"sprite_nuage_{i}.png") for i in range(4)]

        # Nuage mouvement
        self.tornade_move_delay = 150  # ms entre chaque case

        # ÉTATS
        self.current_event = None
        self.event_duration = 6000

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
                #["pluie", 1, PHRASES_METEO[0]],
                #["canicule", 0.25, PHRASES_METEO[1]],
                #["gel", 0.4, PHRASES_METEO[2]],
                ["orage", 0.9, PHRASES_METEO[3]],
                ["tornade", 0.8, PHRASES_METEO[4]],
                #["inondation", 1, PHRASES_METEO[5]],
                #["reforestation", 1, PHRASES_METEO[6]],
                #["intervention ecologiste", 0.45, PHRASES_METEO[7]],
                #["sécheresse ciblée", 1, PHRASES_METEO[8]],
                #["epidemie", 0.35, PHRASES_METEO[9]],
                ["météorite", 0.5, PHRASES_METEO[10]],
                #[None, 1]
            ]

    def update_event(self):

        now = pygame.time.get_ticks()

        if now - self.last_event > self.event_duration and not self.tornade_active:

            self.last_event = now

            index_event = randint(0, 2)
            self.current_event = self.events[index_event][0]

            if random() < self.events[index_event][1]:

                self.pluie_active = self.current_event == "pluie"
                self.canicule_active = self.current_event == "canicule"
                self.gel_active = self.current_event == "gel"
                self.orage_active = self.current_event == "orage"

                if self.current_event == "tornade":
                    self.tornade_active = True
                else:
                    self.tornade_active = False

                self.inondation_active = self.current_event == "inondation"
                self.reforestation_active = self.current_event == "reforestation"
                self.intervention_ecologiste_active = self.current_event == "intervention ecologiste"
                self.secheresse_ciblee_active = self.current_event == "sécheresse ciblée"
                self.epidemie_active = self.current_event == "epidemie"

                if self.current_event == "météorite":
                    self.meteorite_active = True
                    self.meteorite_spawn = False
                else:
                    self.meteorite_active = False
            
                print(f"Evénement actif : {self.current_event} à {(now - self.start_time) / 1000}")

                try:
                    phrase = self.events[index_event][2]
                    self.notif.ajouter(phrase)
                except:
                    pass

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

        # Effets gameplay
        self.data.eau += 0.03
        self.data.biodiversite += 0.02

    def canicule(self):

        if not self.canicule_active:
            return

        image = self.sprite_sun[0]
        image.set_alpha(120)
        self.screen.blit(image, (self.zone_x, self.zone_y))

        self.data.eau -= 0.04
        self.data.biodiversite -= 0.02

    def orage(self):

        if not self.orage_active:
            return

        # Flash visuel
        if random() < 0.035:
            self.flash_alpha = 150

            # Chance de déclencher un feu
            if random() < 0.8:
                ligne = randint(0, self.grille.lignes - 1)
                colonne = randint(0, self.grille.colonnes - 1)

                if not self.grille.grille[ligne][colonne] == (0,0,255):
                    self.animation.ajouter_animation(self.sprite_eclair, self.animation.scale(6, ligne, colonne, from_top = 0.4)[1], self.animation.scale(6, ligne, colonne, from_top = 0.4)[0], frame_delay = 90)
                    self.flamme.propagation_feu(ligne, colonne, puissance = 3, spawn_anim=False)

        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((self.zone_L, self.zone_l))
            flash_surface.fill((255,255,255))
            flash_surface.set_alpha(self.flash_alpha)
            self.screen.blit(flash_surface, (self.zone_x, self.zone_y))
            self.flash_alpha -= 10

    def gel(self):

        if not self.gel_active:
            return

        # Ralentit propagation via malus
        pass

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

            self.meteorite_ligne = randint(2, self.grille.lignes - 3)
            self.meteorite_colonne = randint(2, self.grille.colonnes - 3)

            if self.grille.grille[self.meteorite_ligne][self.meteorite_colonne] != (0,0,255):

                self.meteorite_anim_id = self.animation.ajouter_animation(self.sprite_meteorite, self.animation.scale(9, self.meteorite_ligne, self.meteorite_colonne, from_top=0.4)[1], self.animation.scale(9, self.meteorite_ligne, self.meteorite_colonne, from_top=0.4)[0], frame_delay=90)

                self.meteorite_spawn = True
                self.flag_flash = False

        # Si animation supprimée → stop
        if self.meteorite_anim_id not in self.animation.animations:
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
                        self.flamme.propagation_feu(ligne, colonne, puissance=6, spawn_anim=False)

        # FLASH
        if self.flash_alpha > 0:

            flash_surface = pygame.Surface((self.zone_L, self.zone_l))
            flash_surface.fill((255,255,255))
            flash_surface.set_alpha(self.flash_alpha)

            self.screen.blit(flash_surface, (self.zone_x, self.zone_y))

            self.flash_alpha -= 15

    def reforestation_naturelle(self):

        if not self.reforestation_active:
            return

        cases_changees = 0
        objectif = randint(4, 8)

        for ligne in range(self.grille.lignes):
            for colonne in range(self.grille.colonnes):

                if cases_changees >= objectif:
                    return

                # Si c'est de l'herbe
                if self.grille.grille[ligne][colonne] == (0,255,0):

                    # Vérifie les 4 voisins
                    voisins = [(ligne-1, colonne), (ligne+1, colonne), (ligne, colonne-1), (ligne, colonne+1)]

                    for l, c in voisins:
                        if 0 <= l < self.grille.lignes and 0 <= c < self.grille.colonnes:
                            if self.grille.grille[l][c] == (0,50,0):

                                # Transformation
                                self.grille.grille[ligne][colonne] = (0,50,0)
                                cases_changees += 1
                                break

    def inondation(self):

        if not self.inondation_active:
            return

        cases_changees = 0
        objectif = randint(4, 8)

        for ligne in range(self.grille.lignes):
            for colonne in range(self.grille.colonnes):

                if cases_changees >= objectif:
                    return

                case = self.grille.grille[ligne][colonne]

                # Si herbe ou forêt
                if case == (0,255,0) or case == (0,50,0):

                    voisins = [(ligne-1, colonne), (ligne+1, colonne), (ligne, colonne-1), (ligne, colonne+1)]

                    for l, c in voisins:
                        if 0 <= l < self.grille.lignes and 0 <= c < self.grille.colonnes:
                            if self.grille.grille[l][c] == (0,0,255):

                                self.grille.grille[ligne][colonne] = (0,0,255)
                                cases_changees += 1
                                break

    def secheresse_naturelle(self):

        if not self.secheresse_ciblee_active:
            return

        cases_changees = 0
        objectif = randint(4, 8)

        for ligne in range(self.grille.lignes):
            for colonne in range(self.grille.colonnes):

                if cases_changees >= objectif:
                    return

                # Si c'est de l'eau
                if self.grille.grille[ligne][colonne] == (0,0,255):

                    # 4 voisins (adjacence simple)
                    voisins = [(ligne-1, colonne), (ligne+1, colonne), (ligne, colonne-1), (ligne, colonne+1)]

                    for l, c in voisins:
                        if 0 <= l < self.grille.lignes and 0 <= c < self.grille.colonnes:
                            if self.grille.grille[l][c] == (0,255,0):  # herbe

                                # Transformation eau → herbe
                                self.grille.grille[ligne][colonne] = (0,255,0)
                                cases_changees += 1
                                break

    def update(self):
        self.update_event()

        self.pluie()
        self.canicule()
        self.gel()
        self.orage()
        self.tornade()
        self.meteorite()
        self.reforestation_naturelle()
        self.inondation()
        self.secheresse_naturelle()