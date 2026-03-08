# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from dico_info_game import *
from ui_tools import UI_PNG
from random import random, randint
from animation import Animation

class Pollue:
    def __init__(self, screen, grille, data, dico_UI_anim, dico_UI_interact, plan_ref, notif):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.dico_UI_interact = dico_UI_interact
        self.plan_ref = plan_ref  # référence vers le plan du jeu
        self.animation = Animation(screen, plan_ref, dico_UI_anim, grille)
        self.BASE_DIR = os.path.dirname(__file__)
        self.notif = notif

        self.dico_info = Dico_info_Game()
        self.pollue_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case pollue"]]

        self.file_propagation = []
        self.last_pollue_update = pygame.time.get_ticks()
        self.pollue_delay = 1200

        self.nbr_pollue_spawn = 0

        self.SOUND_POLLUE_PATH = [os.path.join(self.BASE_DIR, "sound", f"fire{i}") for i in range(1,4)]
        

    def ajout_pollue(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        pollue = UI_PNG(self.screen, self.dico_info.type_cases["Case pollue"][0], (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0)

        pollue.frame = 0
        pollue.last_update = pygame.time.get_ticks()
        pollue.vie = randint(350, 450)
        pollue.ligne = ligne
        pollue.colonne = colonne

        self.data.eau -= 1
        self.data.biodiversite -= 2
        self.data.pollution += 0.8

        plan = self.plan_ref()
        self.dico_UI_anim[plan]["Poubelle"][self.nbr_pollue_spawn] = pollue

        self.nbr_pollue_spawn += 1

    def anim_pollue(self):
        frame_delay = 105  # ms
        now = pygame.time.get_ticks()

        for pollue in self.dico_UI_anim[self.plan_ref()]["Poubelle"].values():
            if now - pollue.last_update >= frame_delay:
                pollue.frame = (pollue.frame + 1) % len(self.dico_info.type_cases["Case pollue"])
                pollue.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                pollue.img_base = self.pollue_frames[pollue.frame]

    def proba_propagation(self):
        """
        Retourne une probabilité entre 0 et 1
        dépendante de la température
        """
        # Base minimale
        base = 0.4

        # Influence température (0 → 100)
        influence = self.data.eau / 240

        # Limite max
        return min(0.9, base - influence)
    
    def puissance_pollue(self):
        '''
        Détermine la profondeur de propagation
        '''
        return 4 - int(self.data.eau / 250)
    
    def case_polluable(self, ligne, colonne):

        case = self.grille.grille[ligne][colonne]
        plan = self.plan_ref()

        # Herbe
        if case == (0,255,0):
            return False
        
        # Foret
        if case == (0,50,0):
            return False
        
        # Usine
        if case == "usine":
            return False

        # Déjà en feu
        if case == "feu":
            return False

        # Polluée
        if case == "pollue":
            return False

        # Case brûlée
        if case == "brulee":
            return False

        # Croix condamnée
        for croix in self.dico_UI_anim[plan]["Croix"].values():
            if croix.ligne == ligne and croix.colonne == colonne and (croix.case_originel == (0,50,0) or croix.case_originel == (0,255,0)):
                return False

        return True

    def propagation_pollue(self, ligne, colonne, puissance, spawn_anim=False):
        
        if puissance <= 0:
            return

        if not self.case_polluable(ligne, colonne):
            return
        
        else:
            if spawn_anim:
                frames = [os.path.join(self.BASE_DIR, "sprite", "sprite_pollue", f"sprite_pollue_spawn_{str(i).zfill(2)}.png") for i in range(10)]
                self.animation.ajouter_animation(frames, self.animation.scale(5, ligne, colonne)[1], self.animation.scale(5, ligne, colonne)[0], frame_delay = 50)

                self.pollue_sound = pygame.mixer.Sound(f"{self.SOUND_POLLUE_PATH[randint(0,2)]}.wav")
                self.pollue_sound.set_volume(0.05)
                self.pollue_sound.play()

            self.grille.grille[ligne][colonne] = "pollue"
            self.ajout_pollue(ligne, colonne)

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

    def update_propagation_pollue(self):
        now = pygame.time.get_ticks()

        if now - self.last_pollue_update < self.pollue_delay:
            return

        self.last_pollue_update = now

        # On prend une vague complète
        vague = self.file_propagation.copy()
        self.file_propagation.clear()

        for ligne, colonne, puissance in vague:
            self.propagation_pollue(ligne, colonne, puissance)

    def update_extinction(self, meteo):

        plan = self.plan_ref()

        for key, pollue in list(self.dico_UI_anim[plan]["Poubelle"].items()):

            # VITESSE D'EXTINCTION
            perte = 0.9

            # L'eau ralentit la pollution
            perte -= self.data.eau / 250

            # La pluie accélère l’extinction
            if meteo.pluie_active:
                perte += 4

            perte = max(0.1, perte)

            pollue.vie -= perte

            # EXTINCTION
            if pollue.vie <= 0:

                ligne = pollue.ligne
                colonne = pollue.colonne

                # Mise à jour logique
                self.grille.grille[ligne][colonne] = (0,0,255)

                # Suppression pollution
                del self.dico_UI_anim[plan]["Poubelle"][key]

                # Suppression case visuelle existante
                for key_case, case in list(self.dico_UI_interact[plan]["Case"].items()):
                    if case.ligne == ligne and case.colonne == colonne:
                        del self.dico_UI_interact[plan]["Case"][key_case]
                        break

                # Création nouvelle case eau
                x, y = self.grille.placement_grille(colonne, ligne)

                sprite = self.dico_info.type_cases[(0,0,255)]
                img = sprite[randint(0, len(sprite) - 1)]

                case_eau = UI_PNG(self.screen, img, (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0.01)

                case_eau.ligne = ligne
                case_eau.colonne = colonne

                new_key = ligne * self.grille.colonnes + colonne
                self.dico_UI_interact[plan]["Case"][new_key] = case_eau

                # Ajustement stats
                self.data.eau += 1
                self.data.biodiversite += 2
                self.data.pollution -= 0.8