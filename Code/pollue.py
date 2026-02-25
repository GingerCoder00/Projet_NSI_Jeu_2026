
import pygame
from dico_info_game import *
from ui_tools import UI_PNG
from random import random, randint

class Pollue:
    def __init__(self, screen, grille, data, dico_UI_anim, plan_ref):
        self.screen = screen
        self.grille = grille
        self.data = data
        self.dico_UI_anim = dico_UI_anim
        self.plan_ref = plan_ref  # référence vers le plan du jeu

        self.dico_info = Dico_info_Game()
        self.poubelle_frames = [pygame.image.load(path).convert_alpha() for path in self.dico_info.type_cases["Case ETDB"]]

        self.nbr_poubelle_spawn = 0

    def ajout_pollue(self, ligne, colonne):
        x, y = self.grille.placement_grille(colonne, ligne)

        poubelle = UI_PNG(
            self.screen,
            self.dico_info.type_cases["Case pollue"][0],
            (x, y, self.grille.case_Long, self.grille.case_larg),
            5, 0
        )

        poubelle.frame = 0
        poubelle.last_update = pygame.time.get_ticks()

        self.dico_UI_anim[0]["Poubelle"][len(self.dico_UI_anim[0]["Poubelle"])] = poubelle
        self.grille.grille[ligne][colonne] = "pollue"
        self.nbr_poubelle_spawn += 1

    def anim_pollue(self):
        FRAME_DELAY = 120  # ms
        now = pygame.time.get_ticks()

        for poubelle in self.dico_UI_anim[self.plan_ref()]["Poubelle"].values():
            if now - poubelle.last_update >= FRAME_DELAY:
                poubelle.frame = (poubelle.frame + 1) % len(self.dico_info.type_cases["Case pollue"])
                poubelle.last_update = now

                # Mise à jour DU CŒUR de l'image affichée
                poubelle.IMG_PATH = self.dico_info.type_cases["Case pollue"][poubelle.frame]
                poubelle.img_base = pygame.image.load(poubelle.IMG_PATH).convert_alpha()

    def proba_propagation(self):
        """
        Retourne une probabilité entre 0 et 1
        dépendante de la température
        """
        # Base minimale
        base = 0.2

        # Influence température (0 → 100)
        influence = self.data.eau / 150  

        # Limite max
        return min(0.8, base - influence)
    
    def puissance_pollue(self):
        '''
        Détermine la profondeur de propagation
        '''
        return 3 - int(self.data.eau / 50)
    
    def case_polluable(self, ligne, colonne):

        case = self.grille.grille[ligne][colonne]
        plan = self.plan_ref()

        # Eau
        if case == (0,0,255):
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

        # Croix condamnée (protection)
        for croix in self.dico_UI_anim[plan]["Croix"].values():
            if croix.ligne == ligne and croix.colonne == colonne and croix.case_originel == (0,0,255):
                return False

        return True

    def propagation_pollue(self, ligne, colonne, puissance, spawn_anim=False):
        
        if puissance <= 0:
            return
        
        case = self.grille.grille[ligne][colonne]

        # Si on tombe sur une usine
        if case == "usine":
            self.detruire_usine(ligne, colonne)
            return

        if not self.case_inflammable(ligne, colonne):
            return
        
        else:
            if spawn_anim:
                frames = [
                    os.path.join(self.BASE_DIR, "sprite", "sprite_feu", f"sprite_feu_spawn_{str(i).zfill(2)}.png")
                    for i in range(18)
                ]
                self.animation.ajouter_animation(
                    frames,
                    self.animation.scale(5, ligne, colonne)[1],
                    self.animation.scale(5, ligne, colonne)[0],
                    frame_delay = 3
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


    def update_propagation_pollue(self):
        now = pygame.time.get_ticks()

        if now - self.last_fire_update < self.fire_delay:
            return

        self.last_fire_update = now

        # On prend une vague complète
        vague = self.file_propagation.copy()
        self.file_propagation.clear()

        for ligne, colonne, puissance in vague:
            self.propagation_feu(ligne, colonne, puissance)

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