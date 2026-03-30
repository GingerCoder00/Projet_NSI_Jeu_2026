# Projet : Let's Break Down The Earth
# Auteurs : ARTHUR LE GULUDEC, NOAH DEBAILLEUX, LEANA WEBER, LEWELINE COLLIN--MONTRON

import os

class Dico_info_Game:
    '''
    Cette classe permet de gérer les sprites des types de cases ou des effets de cases. On charge les chemins de sprite dans le disque
    une seule fois ce qui permet de ne pas surcharger le processeur
    '''
    def __init__(self):

        self.BASE_DIR = os.path.dirname(__file__)
        
        # Gestion des types de cases
        self.CASES_E_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_eau\\v2", "sprite_eau_")
        self.CASES_H_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_herbe\\v2", "sprite_herbe_")
        self.CASES_Fo_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_foret\\v4", "sprite_foret_")
        self.CASES_Fe_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_feu", "sprite_feu_")
        self.CASES_P_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_pollue", "sprite_pollue_")
        self.CASES_B_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_case_brulee", "sprite_case_brulee_")
        self.CASES_In_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_condamne", "sprite_condamne_")
        self.CASES_U_PATH = os.path.join(self.BASE_DIR, "sprite", "sprite_usine", "sprite_usine_")

        # On charge les chemins à l'avance pour les réutiliser plus tard
        self.type_cases = {
            (0,0,255) : [f"{self.CASES_E_PATH}{i}.png" for i in range(4)],
            (0,255,0) : [f"{self.CASES_H_PATH}{i}.png" for i in range(4)],
            (0,50,0) : [f"{self.CASES_Fo_PATH}{i}.png" for i in range(6)],
            "Case ETDB" : [f"{self.CASES_Fe_PATH}{i}.png" for i in range(5)],
            "Case pollue" : [f"{self.CASES_P_PATH}{i}.png" for i in range(3)],
            "Case brulee" : [f"{self.CASES_B_PATH}{i}.png" for i in range(2)],
            "Terre inutilisable": [f"{self.CASES_In_PATH}{i}.png" for i in range(7)],
            "Usine": [f"{self.CASES_U_PATH}{i}.png" for i in range(5)],
        }
