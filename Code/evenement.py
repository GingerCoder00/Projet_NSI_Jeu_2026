from random import randint

class Evenement:
    def __init__(self):
        pass

    def evenement_malchanceux(self):
        event = randint(1, 4)
        if event == 1:
            return "Forte pluie"
        elif event == 2:
            return "Ressource supplémentaire"
        elif event == 3:
            return "Diminution de la pollution"
        elif event == 4:
            return "Décontamination d'une usine"
        
    def evenement_chanceux(self):
        event = randint(1, 3)
        if event == 1:
            return "Explosion d'une usine"
        elif event == 2:
            return "Catastrophe naturelle"
        elif event == 3:
            return "Pic de pollution"

    def evenement_tres_chanceux(self):
        return "Guerre nucléaire"

    def evenement(self):
        tirage = randint(1, 1000)
        if 1 <= tirage <= 100:
            return self.evenement_chanceux()
        elif 102 <= tirage <=750 :
            return None
        elif 750 <= tirage <= 1000:
            return self.evenement_malchanceux()
        elif tirage == 101:
            return self.evenement_tres_chanceux()