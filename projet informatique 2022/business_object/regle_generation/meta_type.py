from business_object.regle_generation.typ import Type

class Meta_type:
    '''Classe qui permet de créer les metas types, de définir quels données on va vouloir générer
    
    Attributes
    ----------
    nom : str
        le nom du meta type en question
    list_type : list 
        liste contenant le nom des types composant le meta type'''

    dict_meta_type = {}

    def __init__(self, nom : str, list_type : list):
        self.nom = nom
        self.list_type = list_type
    
    def add_meta_type(self):
        '''Fonction qui a pour but d'ajouter un metatype au dictionnaire contenant les metatypes
        
        Example
        ----------
        >>> mt = Meta_type("individu", ["nom","age"])
        >>> t1 = Type(100, "age")
        >>> t2 = Type(100, "nom")
        >>> t2.add_type()
        {'nom': {'remplissage': 100, 'id': 1}}
        >>> t1.add_type()
        {'nom': {'remplissage': 100, 'id': 1}, 'age': {'remplissage': 100, 'id': 2}}
        >>> print(mt.add_meta_type())
        {'individu': ['nom', 'age']}
        '''
        if self.nom in Meta_type.dict_meta_type:
            raise Exception("Please Select an other name for this meta type it has to be unique")
        n = len(self.list_type)
        res = 0
        for k in range(0, n):
            if self.list_type[k] in Type.dict_type:
                res = res + 1
        if res == n :
            dic = {self.nom : self.list_type}
            Meta_type.dict_meta_type.update(dic)
            return Meta_type.dict_meta_type
        else : 
            raise Exception("All type selected are not define please check the spelling") 
            
            
    def delete_meta_type(nom_meta_type):
        
        if nom_meta_type in Meta_type.dict_meta_type : 
            del Meta_type.dict_meta_type[nom_meta_type]
            return Meta_type.dict_meta_type
        else : 
            raise Exception("Please check youre spelling this meta type do not exist") 

if __name__ == '__main__':
    import doctest
    doctest.testmod()