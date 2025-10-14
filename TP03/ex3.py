import random

class Pokemon:
    def __init__(self, nom, pv, atk):
        """------------"""
        self.nom = nom
        self.pv = pv
        self.atk = atk

    # Getters
    @property
    def nom(self):
        return self.__nom

    @property
    def pv(self):
        return self.__pv

    @property
    def atk(self):
        return self.__atk

    # Setters
    @nom.setter
    def nom(self, nom):
        if not isinstance(nom, str):
            raise TypeError("Il doit s'agir d'une chaîne")
        self.__nom = nom

    @pv.setter
    def pv(self, pv):
        if not isinstance(pv, int) or pv <= 0:
            raise ValueError("La valeur doit être un entier positif.")
        self.__pv = pv

    @atk.setter
    def atk(self, atk):
        if not isinstance(atk, int) or atk <= 0:
            raise ValueError("La valeur doit être un entier positif.")
        self.__atk = atk

    @property
    def est_ko(self):
        """------------"""
        return self.__pv <= 0

    def attaquer(self, autre):
        """------------"""
        degats = random.randint(0, self.atk)
        nouveaux_pv = autre.pv - degats
        autre.pv = nouveaux_pv
        
class PokemonFeu(Pokemon): 
    def __init__(self,nom,pv,atk):
        super().__init__(nom)
        super().__init__(pv)
        super().__init__(atk)
    def attaquer(self,autre):
        """------------"""
        degats = random.randint(0, self.atk)
        if isinstance(autre
    
    
