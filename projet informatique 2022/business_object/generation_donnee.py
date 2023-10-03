import json
from business_object.regle_generation.typ import Type
from business_object.regle_generation.modality import Modality
from business_object.regle_generation.meta_type import Meta_type
import random
import numpy as np


class Generation_donnee:

    '''Classe qui a pour but de générer des données à partir des dictionnaires des types, modalités et metas types

    Attributes
    ----------
    Nb : int
        Le nombre d'observation que l'on souhaite générer
    meta_type :
        Avec quel meta type on souhaite générer les données
    '''

    jeu_donnee = {}
    meta_type1 = []
    tailles = []

    def __init__(self,Nb : int, meta_type :str):
        self.Nb = Nb
        self.meta_type = meta_type
       
        
    def generer_jeu_donnee(self):
        '''Fonction qui a pour but de générer les données
        '''
        res = len(Generation_donnee.jeu_donnee)
        for n in range(self.Nb):
            indivivu_n = {}
            for k in Meta_type.dict_meta_type[self.meta_type]:
                type_individu_n = Type.dict_type
                tx_r = int(type_individu_n[k]["remplissage"])
                if 100*random.random() < tx_r :
                    mod_list = []
                    for i in Modality.dict_modality:
                        if Modality.dict_modality[i]["type"] == k:
                            mod_list.append([Modality.dict_modality[i]["value"],Modality.dict_modality[i]["proba d'apparition"]])
                    mod_list2 = [row[0] for row in mod_list]
                    m = len(mod_list)
                    if "normal" in mod_list2 and "mean" in mod_list2 and "variance" in mod_list2:
                        index_mean = 0
                        index_var = 0
                        for j in range(0, m):
                            if mod_list[j][0] == "mean":
                                index_mean = j
                            if mod_list[j][0] == "variance":
                                index_var = j
                        mean = mod_list[index_mean][1]
                        var = mod_list[index_var][1]
                        mod = np.random.normal(mean,var ** (1/2),1)[0]
                        indivivu_n[k] = round(mod,2)
                    if "uniform" in mod_list2 and "borne1" in mod_list2 and "borne2" in mod_list2:
                        index_borne1 = 0
                        index_borne2 = 0
                        for j in range(0, m):
                            if mod_list[j][0] == "borne1":
                                index_borne1 = j
                            if mod_list[j][0] == "borne2":
                                index_borne2 = j
                        borne1 = mod_list[index_borne1][1]
                        borne2 = mod_list[index_borne2][1]
                        mod = np.random.uniform(borne1,borne2,1)[0]
                        indivivu_n[k] = round(mod,2)
                    if "exponential" in mod_list2 and "lambda" in mod_list2:
                        index_lambda = 0
                        for j in range(0, m):
                            if mod_list[j][0] == "lambda":
                                index_lambda = j
                        ilambda = mod_list[index_lambda][1]
                        mod = np.random.exponential(ilambda,1)[0]
                        indivivu_n[k] = round(mod,2)
                    if "normal" not in mod_list2 and "uniform" not in mod_list2 and "exponential" not in mod_list2:
                        weight = 0
                        for i in range(0, m):
                            weight = mod_list[i][1]+weight
                        mod_list[0][1] = (mod_list[0][1]/weight)*100
                        for i in range(1, m):
                            mod_list[i][1] = (mod_list[i][1]/weight)*100 + mod_list[i-1][1]
                        randfloat = random.uniform(0,100)
                        for i in range(0, m):
                            if randfloat < mod_list[0][1]:
                                mod = mod_list[0][0]
                            else:
                                if randfloat > mod_list[i-1][1] and randfloat < mod_list[i][1] :
                                    mod = mod_list[i][0]
                        indivivu_n[k] = mod
                else :
                    indivivu_n[k] = "mq"
            Generation_donnee.jeu_donnee.update({n + res : indivivu_n})
            Generation_donnee.meta_type1.append(self.meta_type)
            Generation_donnee.tailles.append(self.Nb)
        return Generation_donnee.jeu_donnee    
