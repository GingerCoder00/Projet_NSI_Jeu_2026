
class Resp_tools:
    def __init__(self, long_screen:int, larg_screen:int):
        self.Long = long_screen
        self.larg = larg_screen

    def resp(self, ratio_x:float, ratio_y:float, ratio_long:float, ratio_larg:float):
        '''Méthode qui gère la responsive des surfaces comme les boutons, les interfaces ou les champs'''
        # On convertit tout les éléments par rapport à un ratio et à la taille de l'écran
        x = self.Long * ratio_x
        y = self.larg * ratio_y
        L = self.Long * ratio_long
        l = self.larg * ratio_larg
        return (x, y, L, l)

    def resp_font(self, ratio_long:float, ratio_font:float):
        '''
        Méthode qui gère la responsive des tailles de polices d'écriture en fonction de la 
        longueur d'une surface
        '''
        return int(self.Long * ratio_long * ratio_font)

    def resp_text(self, ratio_x:float, ratio_y:float):
        '''
        Méthode qui gère la responsive des positions des textes à partir d'un ratio x et y
        '''
        return (self.Long * ratio_x, self.larg * ratio_y)