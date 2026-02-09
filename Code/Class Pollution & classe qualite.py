class Pollution:
    def __init__(self, nb_usines=0):
        self.nb_usines = nb_usines
        self.taux = 0

    def calcul_pollution(self):
        """
        Pollution(t+1) = Pollution(t) + nombre d'usines
        """
        self.niveau += self.nb_usines
        return self.niveau

    def regeneration_naturelle(self, nb_forets):
        """
        Chaque forêt réduit la pollution
        """
        return nb_forets * 0.5

class Qualite:
    def __init__(self, air=100, eau=100):
        self.air = air
        self.eau = eau

    def qualite_air(self, pollution, regeneration):
        """
        Air(t+1) = Air(t) -pollution + régénération
        """
        self.air = self.air - pollution + regeneration
        return self.air

    def qualite_eau(self, pollution, regeneration):
        """
        Eau(t+1) = Eau(t)-pollution+ régénération
        """
        self.eau = self.eau - pollution + regeneration
        return self.eau

    def qualite_planete(self):
        """
        IndicePlanete = (Air + Eau) / 2
        """
        return (self.air + self.eau) / 2
