from business_object.regle_generation.typ import Type

class Modality:
    '''Classe permettant de définir les différents modalités associées à chaque type en les stockant dans un dictionnaire
    
    
    Attributes
    ----------
    nom_type : str
        le nom du type à laquelle est associée la modalité
    proba d'apparition : float
        un nombre qui caractérise la probabilité d'appararition d'une modalité parmis les autres modalités qui concernent le même type
    value
        la valeur de la modalité'''

    dict_modality = {}


    def __init__(self, nom_type : str, proba_apparition : float, value):
        self.proba_apparition = proba_apparition
        self.value = value
        self.nom_type = nom_type

    def add_modality(self):
        '''Fonction qui a pour but d'ajouter une nouvelle modalité au dictionnaire des modalités
        
        Example
        -----------
        >>> m = Modality("age", 100, 22)
        >>> t = Type(100, "age")
        >>> t.add_type()
        {'age': {'remplissage': 100, 'id': 1}}
        >>> print(m.add_modality())
        {1: {'type': 'age', 'value': 22, "proba d'apparition": 100}}
        '''
        if self.nom_type in Type.dict_type :
            id_modality = len(Modality.dict_modality) + 1
            d = {id_modality : {"type" : self.nom_type , "value" : self.value, "proba d'apparition" : self.proba_apparition}}
            Modality.dict_modality.update(d)
            return Modality.dict_modality 
        else : 
            raise Exception("The modality has no type associated please check your spelling") 
        

    def delete_modality(nom_type : str, value):
        '''Fonction qui a pour but d'enlever une modalité au dictionnaire des modalités

        Parameters
        -----------
        nom_type : str
            le nom du type au quel est associé la modalité que l'on veut retirer
        value 
            la valeur de la modalité que l'on veut retirer
        
        '''
        for k in Modality.dict_modality :
            if Modality.dict_modality[k]["value"] == value and Modality.dict_modality[k]["type"] == nom_type:
                Modality.dict_modality[k]["proba d'apparition"] = 0
                return Modality.dict_modality
            else : 
                raise Exception("please check your spelling") 

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    