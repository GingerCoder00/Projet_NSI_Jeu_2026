# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import pygame
from dico_info_game import *
from ui_tools import UI_PNG
from random import random, randint
from animation import Animation


# Classe qui gère le système de pollution dans la grille
class Pollue:

    # Initialisation du système de pollution
    def __init__(self, screen, grille, data, dico_UI_anim, dico_UI_interact, plan_ref, notif):

        # Surface principale du jeu
        self.screen = screen

        # Référence vers la grille du jeu
        self.grille = grille

        # Données globales du jeu (biodiversité, eau, pollution...)
        self.data = data

        # Dictionnaire contenant les éléments UI animés
        self.dico_UI_anim = dico_UI_anim

        # Dictionnaire contenant les éléments interactifs de l'UI
        self.dico_UI_interact = dico_UI_interact

        # Référence vers le plan actuel du jeu
        self.plan_ref = plan_ref

        # Système d'animation
        self.animation = Animation(screen, plan_ref, dico_UI_anim, grille)

        # Chemin du dossier du script
        self.BASE_DIR = os.path.dirname(__file__)

        # Système de notifications
        self.notif = notif

        # Chargement des informations du jeu (sprites, types de cases...)
        self.dico_info = Dico_info_Game()

        # Chargement des images utilisées pour l'animation de pollution
        self.pollue_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case pollue"]]

        # File d'attente utilisée pour propager la pollution
        self.file_propagation = []

        # Temps du dernier calcul de propagation
        self.last_pollue_update = pygame.time.get_ticks()

        # Délai entre deux vagues de propagation
        self.pollue_delay = 1200

        # Compteur du nombre de pollutions générées
        self.nbr_pollue_spawn = 0

        # Chemins des sons de pollution
        self.SOUND_POLLUE_PATH = [os.path.join(self.BASE_DIR, "sound", f"fire{i}") for i in range(1,4)]
        

    # Création d'une nouvelle case polluée
    def ajout_pollue(self, ligne, colonne):

        # Position de la case dans la grille
        x, y = self.grille.placement_grille(colonne, ligne)

        # Création de l'objet graphique
        pollue = UI_PNG(self.screen, self.dico_info.type_cases["Case pollue"][0], (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0)

        # Initialisation animation
        pollue.frame = 0
        pollue.last_update = pygame.time.get_ticks()

        # Durée de vie de la pollution
        pollue.vie = randint(350, 450)

        # Position logique
        pollue.ligne = ligne
        pollue.colonne = colonne

        # Impact environnemental
        self.data.eau -= 1
        self.data.biodiversite -= 2
        self.data.pollution += 0.8

        # Récupération du plan actif
        plan = self.plan_ref()

        # Ajout dans les objets animés
        self.dico_UI_anim[plan]["Poubelle"][self.nbr_pollue_spawn] = pollue

        self.nbr_pollue_spawn += 1


    # Animation des cases polluées
    def anim_pollue(self):

        frame_delay = 105  # temps entre deux frames
        now = pygame.time.get_ticks()

        # Parcours de toutes les pollutions actives
        for pollue in self.dico_UI_anim[self.plan_ref()]["Poubelle"].values():

            if now - pollue.last_update >= frame_delay:

                # Passage à la frame suivante
                pollue.frame = (pollue.frame + 1) % len(self.dico_info.type_cases["Case pollue"])

                pollue.last_update = now

                # Mise à jour de l'image affichée
                pollue.img_base = self.pollue_frames[pollue.frame]


    # Calcul de la probabilité de propagation de la pollution
    def proba_propagation(self):
        """
        Retourne une probabilité entre 0 et 1
        dépendante de la quantité d'eau
        """

        base = 0.4

        # L'eau réduit la propagation
        influence = self.data.eau / 240

        return min(0.9, base - influence)
    

    # Détermine la puissance de propagation
    def puissance_pollue(self):
        '''
        Détermine la profondeur de propagation
        '''
        return 4 - int(self.data.eau / 250)
    

    # Vérifie si une case peut être polluée
    def case_polluable(self, ligne, colonne):

        case = self.grille.grille[ligne][colonne]
        plan = self.plan_ref()

        # Différents cas interdits

        if case == (0,255,0):  # herbe
            return False
        
        if case == (0,50,0):  # forêt
            return False
        
        if case == "usine":
            return False

        if case == "feu":
            return False

        if case == "pollue":
            return False

        if case == "brulee":
            return False

        # Vérifie si une croix interdit la case
        for croix in self.dico_UI_anim[plan]["Croix"].values():
            if croix.ligne == ligne and croix.colonne == colonne and (croix.case_originel == (0,50,0) or croix.case_originel == (0,255,0)):
                return False

        return True


    # Propagation de la pollution
    def propagation_pollue(self, ligne, colonne, puissance, spawn_anim=False):
        
        # Arrêt si la puissance est nulle
        if puissance <= 0:
            return

        # Vérifie si la case peut être polluée
        if not self.case_polluable(ligne, colonne):
            return
        
        else:

            # Animation de spawn
            if spawn_anim:

                frames = [os.path.join(self.BASE_DIR, "sprite", "sprite_pollue", f"sprite_pollue_spawn_{str(i).zfill(2)}.png") for i in range(10)]

                self.animation.ajouter_animation(frames, self.animation.scale(5, ligne, colonne)[1], self.animation.scale(5, ligne, colonne)[0], frame_delay = 50)

                # Son de pollution
                self.pollue_sound = pygame.mixer.Sound(f"{self.SOUND_POLLUE_PATH[randint(0,2)]}.wav")
                self.pollue_sound.set_volume(0.05)
                self.pollue_sound.play()

            # Mise à jour logique
            self.grille.grille[ligne][colonne] = "pollue"

            # Création visuelle
            self.ajout_pollue(ligne, colonne)

            # Probabilité de propagation
            proba = self.proba_propagation()

            # Propagation dans les 4 directions

            if ligne > 0 and random() < proba:
                self.file_propagation.append((ligne - 1, colonne, puissance - 1))

            if ligne < self.grille.lignes - 1 and random() < proba:
                self.file_propagation.append((ligne + 1, colonne, puissance - 1))

            if colonne > 0 and random() < proba:
                self.file_propagation.append((ligne, colonne - 1, puissance - 1))

            if colonne < self.grille.colonnes - 1 and random() < proba:
                self.file_propagation.append((ligne, colonne + 1, puissance - 1))


    # Mise à jour de la propagation
    def update_propagation_pollue(self):

        now = pygame.time.get_ticks()

        # Limite la vitesse de propagation
        if now - self.last_pollue_update < self.pollue_delay:
            return

        self.last_pollue_update = now

        # On traite une vague complète
        vague = self.file_propagation.copy()
        self.file_propagation.clear()

        for ligne, colonne, puissance in vague:
            self.propagation_pollue(ligne, colonne, puissance)


    # Gestion de la disparition de la pollution
    def update_extinction(self, meteo):

        plan = self.plan_ref()

        for key, pollue in list(self.dico_UI_anim[plan]["Poubelle"].items()):

            # Vitesse de disparition
            perte = 0.9

            # L'eau ralentit la pollution
            perte -= self.data.eau / 250

            # La pluie accélère l'extinction
            if meteo.pluie_active:
                perte += 4

            perte = max(0.1, perte)

            pollue.vie -= perte

            # Si la pollution disparaît
            if pollue.vie <= 0:

                ligne = pollue.ligne
                colonne = pollue.colonne

                # Mise à jour logique de la grille
                self.grille.grille[ligne][colonne] = (0,0,255)

                # Suppression de l'objet pollution
                del self.dico_UI_anim[plan]["Poubelle"][key]

                # Suppression de l'ancienne case graphique
                for key_case, case in list(self.dico_UI_interact[plan]["Case"].items()):
                    if case.ligne == ligne and case.colonne == colonne:
                        del self.dico_UI_interact[plan]["Case"][key_case]
                        break

                # Création d'une nouvelle case eau
                x, y = self.grille.placement_grille(colonne, ligne)

                sprite = self.dico_info.type_cases[(0,0,255)]
                img = sprite[randint(0, len(sprite) - 1)]

                case_eau = UI_PNG(self.screen, img, (x, y, self.grille.case_Long, self.grille.case_larg), 5, 0.01)

                case_eau.ligne = ligne
                case_eau.colonne = colonne

                new_key = ligne * self.grille.colonnes + colonne
                self.dico_UI_interact[plan]["Case"][new_key] = case_eau

                # Ajustement des statistiques environnementales
                self.data.eau += 1
                self.data.biodiversite += 2
                self.data.pollution -= 0.8