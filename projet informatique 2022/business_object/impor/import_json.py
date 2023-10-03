import pandas as pd
from business_object.regle_generation.typ import Type
from business_object.regle_generation.modality import Modality

class IMPORTJSON :
    def __init__(self, chemin_str) :
        self.chemin = chemin_str

    def import_dict(self) :
        metadonnees = pd.DataFrame.transpose(pd.read_json(self.chemin)) # importer le fichier JSON et le mettre en dataFrame         
        try: 
            for i in range(metadonnees.shape[0]) :
                metadonnees.iloc[i,0] = metadonnees.iloc[i,0].split("|") # spliter les différentes modalités pour avoir une liste des modalités
        except :
            texte = """Veuillez entrer un fichier JSON sous un format correct.\n
Le nom de chaque variable doit être mis comme clé, et la valeur de cette clé doit être un dictionnaire contenant les clés 'type' et 'remplissage' dans cet ordre.\n
la valeur de type contient les différentes modalités de la variable séparées par "|" et celle de remplissage contient le taux de remplissage de la variable.\n
Puis pour chaque modalité est associée une proba d'apparition. La pobra d'apparition est une liste (la première proba d'apparition correspond à la première modalité). \n
Si la liste des probas d'apparition commence par "same" alors toutes les proba d'apparition de toutes les modalités seront les mêmes.\n
La première clé de chaque variable doit être le 'type' et doit être une chaine de caractères\n

Pour faire en sorte qu'un type génère une variable continue et non avec des modalités il faut :
-créer le type en question
-rentrer comme modalité le type de loi que l'on veut générer (uniform, exponential ou normal), la proba d'apparition associée importe peu
-rentrer comme modalité du même type les paramêtre de la loi et pour la valeur souhaité de ces paramêtres celles-ci sont rentrés dans le champs proba d'apparition correspondant.
Par exemple si on veut générer une loi uniforme entre 0 et 10, on nome une première modalité uniform, puis une seconde borne1 (cela correspond à la borne inférieure), on remplit
dans le champs proba d'apparition associé 0, puis on nome une 3ème modalité borne2 et on remplit le champ de proba d'apparition associé avec la valeur 10.

Les paramètres à renseigner pour une loi uniform sont borne1 et borne2.
Les paramètres à renseigner pour une loi normal sont mean et variance.
Le paramètre à renseigner pour une loi exponential est lambda.

Par exemple, le fichier json peut se présenter comme suit\n



{
    "sexe": {
        "type": "M|F",
        "remplissage": 100,
        "proba d'apparition": ["same"]
    },
    "age": {
        "type": "uniform|borne1|borne2",
        "remplissage": 100,
        "proba d'apparition": [1,0,100]
    },
    "prenom": {
        "type": "Adrien|Abdoul|Laurène|Isaac|Nathan",
        "remplissage": 88.4,
        "proba d'apparition": ["same"]

    },
    "nom": {
        "type": "Cortada|Toure|Villacampa|Sandja",
        "remplissage": 85,
        "proba d'apparition": [20,20,20,20]
    },

    "taille": {
        "type": "normal|mean|variance",
        "remplissage": 100,
        "proba d'apparition": [1,177,5]
    },

    "nb_chevaux": {
        "type": "uniform|borne1|borne2",
        "remplissage": 100,
        "proba d'apparition": [1,80,200]
    },

    "marque": {
        "type": "mercedes|tesla|citroein|peugeot|audi|ferrari|ford",
        "remplissage": 86,
        "proba d'apparition": ["same"]
    }
    ,

    "vitesse_max": {
        "type": "exponential|lambda",
        "remplissage": 86,
        "proba d'apparition": [1,15]
    }
}
            """
            raise Exception(texte) # préciser la forme du fichier attendue en cas d'erreur
        number_row = -1
        for k in metadonnees.index.values:
            number_row = number_row + 1 
            t = Type(metadonnees.iloc[number_row][1], k)
            t.add_type()
            modality = metadonnees.iloc[number_row][0]
            n = len(modality)
            if metadonnees.iloc[number_row][2][0] == "same":
                for i in range (0,n):
                    m = Modality(k , 1, modality[i])
                    m.add_modality()
            else :
                for i in range (0,n):
                    m = Modality(k , metadonnees.iloc[number_row][2][i], modality[i])
                    m.add_modality()

        return [Type.dict_type, Modality.dict_modality]

