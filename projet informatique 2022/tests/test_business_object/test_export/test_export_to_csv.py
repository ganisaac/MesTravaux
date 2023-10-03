from unittest import TestCase
from unittest.mock import patch
import csv
import os.path
import json
import unittest
import pandas as pd 
from business_object.export.export_to_csv import Export_to_csv
class TestExport_to_csv(TestCase):
    
    

    def test_export_to_csv(self):
        table = {
    "sexe": {
        "type": "SEXE",
        "remplissage": 100
    },
    "age": {
        "type": "18|19|20",
        "remplissage": 100
    },
    "prenom": {
        "type": "NAME",
        "remplissage": 88.4
    },
    "nom": {
        "type": "NAME|'dupont'",
        "remplissage": 85
    }
}
    # Vérifier si le fichier existe ou non
        if os.path.isfile("D:/Projet_Informatique_2A/table_csv.csv"):
            print("fichier trouvé")
            tablecsv = Export_to_csv("D:/Projet_Informatique_2A/Projet-info-2A" , "table_csv1.csv")
            csvfile = pd.read_csv("D:/Projet_Informatique_2A/Projet-info-2A/table_csv.csv")
            table_csv1 = tablecsv.export(json.dumps(table))
            table_csv = pd.read_csv("D:/Projet_Informatique_2A/Projet-info-2A/table_csv1.csv")
            print(table_csv==csvfile)
        else:
            print("Fichier non trouvé")
if __name__=="__main__":
    unittest.main()
    
        
        
        