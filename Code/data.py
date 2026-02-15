
class Data:
    def __init__(self):
        # JAUGES PRINCIPALES
        
        self.pollution = 10
        self.temperature = 15
        self.eau = 100
        self.biodiversite = 100
        self.stabilite = 100
        self.profit = 35
        self.destruction = 0

        # PARAMÈTRES MONDE
        
        self.coeff_temp_from_pollution = 0.002
        self.coeff_eau_from_temp = 0.0015
        self.coeff_biodiv_from_pollution = 0.001
        self.coeff_biodiv_from_temp = 0.001
        self.coeff_stab_from_eau = 0.01
        self.coeff_stab_from_biodiv = 0.008
        self.coeff_pollution_from_stab = 0.02
        self.coeff_pollution_from_profit = 0.001

        # POUVOIRS
        
        self.pouvoirs = {
            "incendie": {
                "cout": 10,
                "effets": {
                    "pollution": 8,
                    "biodiversite": -12
                }
            },
            "usine": {
                "cout": 15,
                "effets": {
                    "pollution": 15,
                    "profit": 10
                }
            },
            "guerre": {
                "cout": 20,
                "effets": {
                    "stabilite": -20,
                    "pollution": 10
                }
            },
            "canicule": {
                "cout": 12,
                "effets": {
                    "temperature": 10
                }
            },
            "maree_noire": {
                "cout": 18,
                "effets": {
                    "pollution": 12,
                    "biodiversite": -15
                }
            },
            "desinformation": {
                "cout": 25,
                "effets": {
                    "stabilite": -15,
                    "profit": 15
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

        # Profit génère pollution passive
        self.pollution += self.profit * self.coeff_pollution_from_profit * temps

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
        self.destruction = (
            self.pollution * 0.25 +
            self.temperature * 0.2 +
            (100 - self.eau) * 0.15 +
            (100 - self.biodiversite) * 0.15 +
            (100 - self.stabilite) * 0.15 +
            self.profit * 0.1
        )

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
