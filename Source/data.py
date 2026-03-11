# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

from grille import *
from phrases_notif import PHRASES_POUVOIR

class Data:
    '''
    Cette classe permet de référencer et de gérer les intéractions et effet de chaque jauges et pouvoir avec le monde
    '''
    def __init__(self, grille, notif_manager):

        self.grille = grille
        self.notif = notif_manager

        # Paramètrage des taux de base des jauges
        
        self.pollution = 10
        self.temperature = 20
        self.eau = 90
        self.biodiversite = 95
        self.stabilite = 95
        self.profit = 0
        self.augmentation_profit = 30
        self.destruction = 0

        # Paramètrage des coefficients permettant de faire intéragir les jauges entre elles
        
        self.coeff_temp_from_pollution = 0.0002
        self.coeff_eau_from_temp = 0.00035
        self.coeff_biodiv_from_pollution = 0.00015
        self.coeff_biodiv_from_temp = 0.0006
        self.coeff_stab_from_eau = 0.0002
        self.coeff_stab_from_biodiv = 0.0022
        self.coeff_pollution_from_stab = 0.0004
        self.coeff_profit_from_profit = 0.04
        self.coeff_pollution_from_profit = 0.00015
        self.coeff_stab_from_stab = 0.00011

        # Gestion des pouvoirs et des effets
        
        self.pouvoirs = {
            "incendie": {
                "cout": 15,
                "effets": {
                    "pollution": 4,
                    "biodiversite": -3,
                    "temperature": 3,
                    "eau": -4
                }
            },
            "usine": {
                "cout": 18,
                "effets": {
                    "pollution": 7,
                    "augmentation_profit": 4
                }
            },
            "guerre": {
                "cout": 20,
                "effets": {
                    "stabilite": -8,
                    "pollution": 6
                }
            },
            "canicule": {
                "cout": 22,
                "effets": {
                    "temperature": 6,
                    "eau": -5,
                }
            },
            "Maree Noire": {
                "cout": 25,
                "effets": {
                    "pollution": 4,
                    "biodiversite": -3,
                    "eau": -3
                }
            },
            "desinformation": {
                "cout": 30,
                "effets": {
                    "stabilite": -6,
                    "augmentation_profit": 7
                }
            }
        }

        # Attribut qui stocke les stats du joueur affiché à la fin de la partie
        self.incendie_declaree = 0
        self.case_polluees = 0
        self.arbre_brules = 0
        self.usine_creee = 0
        self.desinformation_creee = 0
        self.guerre_declaree = 0

    # Mise à jour du monde 
    
    def update_world(self, temps):

        # Pollution influence température
        self.temperature += self.pollution * self.coeff_temp_from_pollution * temps

        # Température influence eau
        self.eau -= self.temperature * self.coeff_eau_from_temp * temps

        # Pollution + température influencent biodiversité
        self.biodiversite -= (
            self.pollution * self.coeff_biodiv_from_pollution +
            self.temperature * self.coeff_biodiv_from_temp
        ) * temps

        # Eau faible entraine instabilité
        if self.eau < 40:
            self.stabilite -= (40 - self.eau) * self.coeff_stab_from_eau * temps

        # Biodiversité faible entraine instabilité
        if self.biodiversite < 40:
            self.stabilite -= (40 - self.biodiversite) * self.coeff_stab_from_biodiv * temps

        # Instabilité entraine pollution (chaos)
        if self.stabilite < 30:
            self.pollution += (30 - self.stabilite) * self.coeff_pollution_from_stab * temps

        # Augmentation des profits
        self.profit += self.augmentation_profit * self.coeff_profit_from_profit * temps

        # Profit entraine pollution
        self.pollution += self.augmentation_profit * self.coeff_pollution_from_profit * temps

        # Plus le temps passe plus la stabilite augmente
        self.stabilite += self.stabilite * self.coeff_stab_from_stab * temps

        # Clamp des valeurs
        self.clamp_values()

        # Recalcul de la destruction
        self.update_destruction()

    # Activation d'un pouvoir
    
    def utiliser_pouvoir(self, nom, ligne = 0, colonne = 0):
        '''
        Cette méthode permet d'activer un pouvoir en particulier et de pouvoir le placer sur la grille si il est prévu pour
        '''

        if nom not in self.pouvoirs:  # On vérifie si le pouvoir existe
            return False
        
        # Ice on va vérifier des conditions spéciale pour les pouvoirs plaçable sur la grille (on ne peut pas placer du feu sur de l'eau)
        if nom == "incendie" and self.grille.grille[ligne][colonne] in [(0,0,255), "feu", "pollue"]:
            return False
        
        if nom == "usine" and self.grille.grille[ligne][colonne] in [(0,0,255), "feu", "pollue", "condamne", "brulee", (0,50,0)]:
            phrase = PHRASES_POUVOIR[1]
            self.notif.ajouter(phrase)
            return False
        
        if nom == "Maree Noire" and self.grille.grille[ligne][colonne] in [(0,255,0), (0,50,0), "pollue"]:
            phrase = PHRASES_POUVOIR[2]
            self.notif.ajouter(phrase)
            return False

        pouvoir = self.pouvoirs[nom]

        # On paye le coût
        self.profit -= pouvoir["cout"]

        # On applique les effets
        for stat, valeur in pouvoir["effets"].items():
            setattr(self, stat, getattr(self, stat) + valeur)

        self.clamp_values()
        self.update_destruction()

        return True

    # Calcul de la destruction

    def update_destruction(self):
        '''
        Cette méthode permet de calculer la destuction totale de la planète
        '''
        # Calcul de destruction prenant en compte chaque jauges
        base = (self.pollution * 0.1 + self.temperature * 0.1 + (100 - self.eau) * 0.1 + (100 - self.biodiversite) * 0.1 + (100 - self.stabilite) * 0.1)

        # Effet d'emballement climatique
        chaos = (self.pollution * self.temperature) / 140
        self.destruction = base + chaos

        # On clamp la valeur pour qu'elle ne dépasse pas 100 et reste au dessus de 0
        self.destruction = max(0, min(100, self.destruction))

    def clamp_values(self):
        '''
        Cette méthode permet de gérer le clamp des valeurs des jauges, c'est à dire d'empécher ces valeurs de dépasser une certaine limite
        Ici on les bloque entre 0 et 100
        '''

        self.pollution = max(0, min(100, self.pollution))
        self.temperature = max(0, min(100, self.temperature))
        self.eau = max(0, min(100, self.eau))
        self.biodiversite = max(0, min(100, self.biodiversite))
        self.stabilite = max(0, min(100, self.stabilite))
        self.profit = max(0, min(100, self.profit))
        self.destruction = max(0, min(100, self.destruction))

    def victoire(self):
        '''
        Cette méthode teste si la victoire est atteinte
        '''
        return self.destruction >= 100
