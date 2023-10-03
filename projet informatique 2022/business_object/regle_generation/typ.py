
class Type:
    '''Une classe qui a pour but de définir un type, une variable composé de modalités qui sert à caractériser un objet ou un individu
    
    Attributes
    ----------
    tx_remplissage : float
        Un nombre compris entre 0 et 100 indiquant le pourcentage de chance que le type n'affiche pas de donnée manquante
    nom : str
        Le nom du type en question
'''

    dict_type = {}


    def __init__(self, tx_remplissage : float, nom : str):
        self.tx_remplissage = tx_remplissage
        self.nom = nom

    def add_type(self):
        '''Fonction qui a pour but d'ajouter un type au dictionnaire contenant l'ensemble des types définis dict_type
        
        Example
        ----------
        >>> t = Type(100, "age")
        >>> print(t.add_type())
        {'age': {'remplissage': 100, 'id': 1}}'''
        if self.nom in Type.dict_type:
            raise Exception("Please select an other name for this type it already exist")
        if self.tx_remplissage <= 100 and self.tx_remplissage >= 0:
            n = len(Type.dict_type) 
            if n == 0:
                id = 1
            else :
                id = 1
                for k in Type.dict_type:
                    res = Type.dict_type[k]["id"]
                    if res >= id :
                        id = res +1
            d = {self.nom : {"remplissage" : self.tx_remplissage, "id" : id}}
            Type.dict_type.update(d)
            return Type.dict_type
        else : 
            raise Exception("Please select a value between 0 and 100 for tx_remplissage ")

    def delete_type(nom : str):
        '''Fonction qui a pour but d'enlever un type au dictionnaire contenant l'ensemble des types définis dict_type

        Parameters
        -----------
        nom : str
            nom du type que l'on shouaite enlever du dictionnaire
        
        '''
        if nom in Type.dict_type:
            del Type.dict_type[nom]
            return Type.dict_type
        else:
            raise Exception("The type you selected hasn't been added yet please check your spelling") 

if __name__ == '__main__':
    import doctest
    doctest.testmod()

