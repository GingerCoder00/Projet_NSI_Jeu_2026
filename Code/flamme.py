import pygame
from ui_tools import UI_PNG
from random import random
from data import *
from grille import *
from dico_info_game import *
from animation import *
from random import randint
from case_brulee import CaseBrulee

class Flamme:
    def __init__(self, screen, grille, data, dico_UI_anim, dico_UI_interact, plan_ref):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.dico_UI_interact = dico_UI_interact
        self.plan_ref = plan_ref  # référence vers le plan du jeu
        self.animation = Animation(screen, plan_ref, dico_UI_anim, grille)
        self.BASE_DIR = os.path.dirname(__file__)

        self.dico_info = Dico_info_Game()
        self.fire_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case ETDB"]]

        self.file_propagation = []
        self.last_fire_update = pygame.time.get_ticks()
        self.fire_delay = 1200

        self.nbr_flammes_spawn = 0

        self.SOUND_EXPLOSION_PATH = [os.path.join(self.BASE_DIR, "sound", f"explosion{i}") for i in range(1,4)]
        self.SOUND_FIRE_PATH = [os.path.join(self.BASE_DIR, "sound", f"fire{i}") for i in range(1,4)]
        

    def ajout_feu(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        flamme = UI_PNG(self.screen, self.dico_info.type_cases["Case ETDB"][0], (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0)

        flamme.frame = 0
        flamme.last_update = pygame.time.get_ticks()
        flamme.vie = 100
        flamme.ligne = ligne
        flamme.colonne = colonne

        self.data.pollution += 0.5
        self.data.temperature += 0.8

        plan = self.plan_ref()
        self.dico_UI_anim[plan]["Flamme"][self.nbr_flammes_spawn] = flamme

        self.nbr_flammes_spawn += 1

    def anim_feu(self):
        frame_delay = 105  # ms
        now = pygame.time.get_ticks()

        for flamme in self.dico_UI_anim[self.plan_ref()]["Flamme"].values():
            if now - flamme.last_update >= frame_delay:
                flamme.frame = (flamme.frame + 1) % len(self.dico_info.type_cases["Case ETDB"])
                flamme.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                flamme.img_base = self.fire_frames[flamme.frame]

    def proba_propagation(self):
        """
        Retourne une probabilité entre 0 et 1
        dépendante de la température
        """
        # Base minimale
        base = 0.12  

        # Influence température (0 → 100)
        influence = self.data.temperature / 150  

        # Limite max
        return min(0.75, base + influence)
    
    def puissance_feu(self):
        '''
        Détermine la profondeur de propagation
        '''
        return 2 + int(self.data.temperature / 25)

    def propagation_feu(self, ligne, colonne, puissance, spawn_anim=False):
        
        if puissance <= 0:
            return
        
        case = self.grille.grille[ligne][colonne]

        # Si on tombe sur une usine
        if case == "usine":
            self.detruire_usine(ligne, colonne)
            return

        if self.grille.grille[ligne][colonne] in [(0,0,255), "feu", "pollue"]:
            return
        
        else:
            if spawn_anim:
                frames = [
                    os.path.join(self.BASE_DIR, "sprite", "sprite_feu", f"sprite_feu_spawn_{str(i).zfill(2)}.png")
                    for i in range(18)
                ]
                self.animation.ajouter_animation(
                    frames,
                    self.animation.scale(3, ligne, colonne)[1],
                    self.animation.scale(3, ligne, colonne)[0],
                    frame_delay=1
                )
                self.fire_sound = pygame.mixer.Sound(f"{self.SOUND_FIRE_PATH[randint(0,2)]}.wav")
                self.fire_sound.set_volume(0.05)
                self.fire_sound.play()
            self.grille.grille[ligne][colonne] = "feu"
            self.ajout_feu(ligne, colonne)

            proba = self.proba_propagation()

            # Haut
            if ligne > 0 and random() < proba:
                self.file_propagation.append((ligne - 1, colonne, puissance - 1))

            # Bas
            if ligne < self.grille.lignes - 1 and random() < proba:
                self.file_propagation.append((ligne + 1, colonne, puissance - 1))

            # Gauche
            if colonne > 0 and random() < proba:
                self.file_propagation.append((ligne, colonne - 1, puissance - 1))

            # Droite
            if colonne < self.grille.colonnes - 1 and random() < proba:
                self.file_propagation.append((ligne, colonne + 1, puissance - 1))


    def update_propagation_feu(self):
        now = pygame.time.get_ticks()

        if now - self.last_fire_update < self.fire_delay:
            return

        self.last_fire_update = now

        # On prend une vague complète
        vague = self.file_propagation.copy()
        self.file_propagation.clear()

        for ligne, colonne, puissance in vague:
            self.propagation_feu(ligne, colonne, puissance)

    def detruire_usine(self, ligne, colonne):

        plan = self.plan_ref()

        # Animation explosion
        frames = [
            os.path.join(self.BASE_DIR, "sprite", "sprite_usine",
                        f"sprite_usine_explosion_{i}.png")
            for i in range(9)
        ]

        self.animation.ajouter_animation(
            frames,
            self.animation.scale(5, ligne, colonne, from_top=0.45)[1],
            self.animation.scale(5, ligne, colonne, from_top=0.45)[0],
            frame_delay=70
        )

        # Son explosion
        explosion_sound = pygame.mixer.Sound(f"{self.SOUND_EXPLOSION_PATH[randint(0,2)]}.wav")
        explosion_sound.set_volume(0.11)
        explosion_sound.play()

        # Supprimer l’usine visuellement
        for key, usine in list(self.dico_UI_anim[plan]["Usine"].items()):
            if usine.ligne == ligne and usine.colonne == colonne:
                del self.dico_UI_anim[plan]["Usine"][key]
                break

        # Nettoyage des cases autour (croix condamnées)
        for key, croix in list(self.dico_UI_anim[plan]["Croix"].items()):
            if abs(croix.ligne - ligne) <= 1 and abs(croix.colonne - colonne) <= 1:
                self.grille.grille[croix.ligne][croix.colonne] = "terre"
                del self.dico_UI_anim[plan]["Croix"][key]

        # Perte économique
        self.data.profit = max(0, self.data.profit - 8)
        self.data.augmentation_profil = max(0, self.data.augmentation_profil - 7)

        # La case usine devient feu
        self.grille.grille[ligne][colonne] = "feu"
        self.ajout_feu(ligne, colonne)
        
    def update_extinction(self, meteo):

        for key, flamme in list(self.dico_UI_anim[self.plan_ref()]["Flamme"].items()):

            # Vitesse de combustion de base
            perte = 0.9

            # Température augmente durée de vie
            perte -= self.data.temperature / 175

            # Pluie accélère extinction
            if meteo.pluie_active:
                perte += 2

            # Minimum de perte
            perte = max(0.1, perte)

            flamme.vie -= perte

            if flamme.vie <= 0:

                # Mettre la grille logique à brulee
                self.grille.grille[flamme.ligne][flamme.colonne] = "brulee"

                # Supprimer la flamme
                del self.dico_UI_anim[self.plan_ref()]["Flamme"][key]

                # Supprimer la case visuelle normale
                for key_case, case in list(self.dico_UI_interact[self.plan_ref()]["Case"].items()):
                    if case.ligne == flamme.ligne and case.colonne == flamme.colonne:
                        del self.dico_UI_interact[self.plan_ref()]["Case"][key_case]
                        break

                # Créer une CaseBrulee
                case_brulee = CaseBrulee(self.screen, self.grille, flamme.ligne, flamme.colonne, self.dico_UI_interact, self.plan_ref)
                plan = self.plan_ref()
                key = flamme.ligne * self.grille.colonnes + flamme.colonne
                self.dico_UI_interact[plan]["CaseBrulee"][key] = case_brulee
                # Ajustement stats
                self.data.pollution -= 0.5
                self.data.temperature -= 0.8