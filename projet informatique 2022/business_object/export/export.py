from abc import ABC, abstractmethod
import json

class Export(ABC):
    def __init__(self,chemin:str, name:str) -> None:
        '''Constructeur
        Attributes
        ----------
        chemin : str 
                 Chemin sur lequel le jeu de données va être sauvegardé
        name : str
               Nom du fichier sur lequel le jeu de données va être sauvegardé
        '''
        self.chemin = chemin
        self.name = name

    @abstractmethod
    def export(self):
        pass