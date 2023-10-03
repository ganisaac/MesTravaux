import json
from business_object.regle_generation.typ import Type
from business_object.regle_generation.modality import Modality
from business_object.regle_generation.meta_type import Meta_type
from business_object.generation_donnee import Generation_donnee
import random
import numpy as np

if __name__ == "__main__":
    t = Type(100, "age")
    t.add_type()
    t2 = Type(100, "prénom")
    t2.add_type()
    m = Modality("age", 100, 22)
    m.add_modality()
    m2 = Modality("prénom",100,"Rémi")
    m2.add_modality()
    mt = Meta_type("individu", ["prénom","age"])
    mt.add_meta_type()
    générer = Generation_donnee(10, "individu")
    if générer.generer_jeu_donnee() == {0: {'prénom': 'Rémi', 'age': 22}, 1: {'prénom': 'Rémi', 'age': 22}, 
                                        2: {'prénom': 'Rémi', 'age': 22}, 3: {'prénom': 'Rémi', 'age': 22}, 
                                        4: {'prénom': 'Rémi', 'age': 22}, 5: {'prénom': 'Rémi', 'age': 22}, 
                                        6: {'prénom': 'Rémi', 'age': 22}, 7: {'prénom': 'Rémi', 'age': 22},
                                        8: {'prénom': 'Rémi', 'age': 22}, 9: {'prénom': 'Rémi', 'age': 22}}:
        print("True")
    else :
        print("False")
    t3 = Type(100, 'adresse')
    t3.add_type()
    m3 = Modality('adresse', 100, 'SDF')
    m3.add_modality()
    mt2 = Meta_type("ind", ["prénom", "adresse"])
    mt2.add_meta_type()
    generer2 = Generation_donnee(10, "ind").generer_jeu_donnee()
    data = Generation_donnee.jeu_donnee
    liste = Generation_donnee.meta_type1
    if len(data) == 20:
        print("True")
    else:
        print("False")
    if len(liste) == 20:
        print("True")
    else:
        print("False")
    print(data)
