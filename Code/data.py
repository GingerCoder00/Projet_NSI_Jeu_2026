
from grille import *
from phrases_notif import PHRASES_POUVOIR

class Data:
    def __init__(self, grille, notif_manager):

        self.grille = grille
        self.notif = notif_manager

        # JAUGES PRINCIPALES
        
        self.pollution = 10
        self.temperature = 10
        self.eau = 100
        self.biodiversite = 100
        self.stabilite = 100
        self.profit = 0
        self.augmentation_profil = 25
        self.destruction = 0

        # PARAMÈTRES MONDE
        
        self.coeff_temp_from_pollution = 0.0002
        self.coeff_eau_from_temp = 0.00035
        self.coeff_biodiv_from_pollution = 0.00015
        self.coeff_biodiv_from_temp = 0.0006
        self.coeff_stab_from_eau = 0.0002
        self.coeff_stab_from_biodiv = 0.0022
        self.coeff_pollution_from_stab = 0.0004
        self.coeff_profit_from_profit = 0.04
        self.coeff_pollution_from_profit = 0.00015

        # POUVOIRS
        
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
                    "augmentation_profil": 4
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
            "maree_noire": {
                "cout": 25,
                "effets": {
                    "pollution": 7,
                    "biodiversite": -7,
                    "eau": -6
                }
            },
            "desinformation": {
                "cout": 30,
                "effets": {
                    "stabilite": -6,
                    "augmentation_profil": 7
                }
            }
        }

    # UPDATE MONDE
    
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

        # Eau faible → instabilité
        if self.eau < 40:
            self.stabilite -= (40 - self.eau) * self.coeff_stab_from_eau * temps

        # Biodiversité faible → instabilité
        if self.biodiversite < 40:
            self.stabilite -= (40 - self.biodiversite) * self.coeff_stab_from_biodiv * temps

        # Instabilité → pollution (chaos)
        if self.stabilite < 30:
            self.pollution += (30 - self.stabilite) * self.coeff_pollution_from_stab * temps

        # Augmentation des profits
        self.profit += self.augmentation_profil * self.coeff_profit_from_profit * temps

        # Profit génère pollution passive
        self.pollution += self.augmentation_profil * self.coeff_pollution_from_profit * temps

        # Clamp des valeurs
        self.clamp_values()

        # Recalcul destruction
        self.update_destruction()

    # ACTIVER UN POUVOIR
    
    def utiliser_pouvoir(self, nom, ligne = 0, colonne = 0):

        if nom not in self.pouvoirs:
            return False
        
        if nom == "incendie" and self.grille.grille[ligne][colonne] in [(0,0,255), "feu", "pollue"]:
            phrase = PHRASES_POUVOIR[0]
            self.notif.ajouter(phrase)
            return False
        
        if nom == "usine" and self.grille.grille[ligne][colonne] in [(0,0,255), "feu", "pollue", "condamne", "brulee", (0,50,0)]:
            phrase = PHRASES_POUVOIR[1]
            self.notif.ajouter(phrase)
            return False
        
        
        if nom == "maree_noire" and self.grille.grille[ligne][colonne] in [(0,255,0), (0,50,0), "pollue", "condamne"]:
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

    # CALCUL DESTRUCTION

    def update_destruction(self):
        base = (
            self.pollution * 0.1 +
            self.temperature * 0.1 +
            (100 - self.eau) * 0.1 +
            (100 - self.biodiversite) * 0.1 +
            (100 - self.stabilite) * 0.1
        )
        # Effet d'emballement climatique
        chaos = (self.pollution * self.temperature) / 135
        self.destruction = base + chaos
        self.destruction = max(0, min(100, self.destruction))



    # CLAMP 0-100

    def clamp_values(self):

        self.pollution = max(0, min(100, self.pollution))
        self.temperature = max(0, min(100, self.temperature))
        self.eau = max(0, min(100, self.eau))
        self.biodiversite = max(0, min(100, self.biodiversite))
        self.stabilite = max(0, min(100, self.stabilite))
        self.profit = max(0, min(100, self.profit))
        self.destruction = max(0, min(100, self.destruction))

    # VICTOIRE

    def victoire(self):
        return self.destruction >= 100
