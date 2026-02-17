
class Data:
    def __init__(self):
        # JAUGES PRINCIPALES
        
        self.pollution = 10
        self.temperature = 25
        self.eau = 100
        self.biodiversite = 100
        self.stabilite = 100
        self.profit = 0
        self.augmentation_profil = 20
        self.destruction = 0

        # PARAMÈTRES MONDE
        
        self.coeff_temp_from_pollution = 0.0008
        self.coeff_eau_from_temp = 0.0009
        self.coeff_biodiv_from_pollution = 0.0005
        self.coeff_biodiv_from_temp = 0.0006
        self.coeff_stab_from_eau = 0.007
        self.coeff_stab_from_biodiv = 0.0022
        self.coeff_pollution_from_stab = 0.015
        self.coeff_profit_from_profit = 0.037
        self.coeff_pollution_from_profit = 0.0006

        # POUVOIRS
        
        self.pouvoirs = {
            "incendie": {
                "cout": 10,
                "effets": {
                    "pollution": 4,
                    "biodiversite": -4
                }
            },
            "usine": {
                "cout": 15,
                "effets": {
                    "pollution": 8,
                    "augmentation_profil": 5
                }
            },
            "guerre": {
                "cout": 20,
                "effets": {
                    "stabilite": -10,
                    "pollution": 6
                }
            },
            "canicule": {
                "cout": 12,
                "effets": {
                    "temperature": 8
                }
            },
            "maree_noire": {
                "cout": 18,
                "effets": {
                    "pollution": 7,
                    "biodiversite": -8
                }
            },
            "desinformation": {
                "cout": 25,
                "effets": {
                    "stabilite": -10,
                    "augmentation_profil": 12
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
    
    def utiliser_pouvoir(self, nom):

        if nom not in self.pouvoirs:
            return False

        pouvoir = self.pouvoirs[nom]

        if self.profit < pouvoir["cout"]:
            return False

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
            self.pollution * 0.25 +
            self.temperature * 0.25 +
            (100 - self.eau) * 0.2 +
            (100 - self.biodiversite) * 0.15 +
            (100 - self.stabilite) * 0.15
        )
        # Effet d'emballement climatique
        chaos = (self.pollution * self.temperature) / 200
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
