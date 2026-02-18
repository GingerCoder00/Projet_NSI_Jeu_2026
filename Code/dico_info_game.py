import os

class Dico_info_Game:
    def __init__(self):

        self.BASE_DIR = os.path.dirname(__file__)
        
        # Gestion des types de cases
        self.CASES_E_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_eau\\v2", "sprite_eau_")
        self.CASES_H_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_herbe", "sprite_herbe_")
        self.CASES_Fo_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_foret\\v2", "sprite_foret_")
        self.CASES_Fe_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_feu", "sprite_feu_")
        self.CASES_P_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_pollue", "sprite_pollue_")
        self.CASES_In_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_condamne", "sprite_condamne_")

        self.type_cases = {
            (0,0,255) : [f"{self.CASES_E_PATH}{i}.png" for i in range(4)],
            (0,255,0) : [f"{self.CASES_H_PATH}{i}.png" for i in range(4)],
            (0,50,0) : [f"{self.CASES_Fo_PATH}{i}.png" for i in range(4)],
            "Case ETDB" : [f"{self.CASES_Fe_PATH}{i}.png" for i in range(5)],
            "Case pollue" : [f"{self.CASES_P_PATH}{i}.png" for i in range(3)],
            "Case brulee" : "",
            "Terre inutilisable": [f"{self.CASES_In_PATH}{i}.png" for i in range(7)],
        }