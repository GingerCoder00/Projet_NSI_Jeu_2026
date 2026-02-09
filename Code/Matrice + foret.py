m =  [[0]*500 for i in range(200)]
print(m)

#1 = Arbre limite 100
#2 = Eau limite 100
#3 = Usines = 5


class Forêt :
    def __init__(self,espace=1,Sain=True,feu = False,cramé=False,risque=None):
        self.espace=espace
        self.sain=Sain
        self.feu=feu
        self.cramé= cramé
        self.risque=risque