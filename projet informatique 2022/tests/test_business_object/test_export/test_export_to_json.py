from unittest import TestCase
from unittest.mock import patch
import csv
import xml
import os.path
import json
import unittest
import pandas as pd 

from business_object.export.export_to_xml import Export_to_xml

class TestExport_to_json(TestCase):
    
    

    def test_export_to_json(self):
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
        if os.path.isfile("D:/Projet_Informatique_2A/Projet-info-2A/output.xml"):
            print("fichier trouvé")
            tablexml = Export_to_json("D:/Projet_Informatique_2A/Projet-info-2A" , "table_xml1")
            jsonfile = pd.read_json("D:/Projet_Informatique_2A/Projet-info-2A/output.xml")
            table_json1 = tablejson.export(json.dumps(table))
            table_json = pd.read_json("D:/Projet_Informatique_2A/Projet-info-2A/table_xml1")
            print(table_json==jsonfile)
        else:
            print("Fichier non trouvé")
        
if __name__=="__main__":
    unittest.main()