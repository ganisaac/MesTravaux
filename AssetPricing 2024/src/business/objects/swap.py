import datetime
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Swap :
    """ 
    Objet définissant un swap.
    direction (str): 'pay' si le client est celui qui achète le taux fixe ou 'receive' dans le cas contraire
    notional (float): le notionel
    fixedrate (float): le taux fixe
    maturitydate (str): la maturité au format'YYYY-MM-DD'
    valuedate (str): date de valeur au format'YYYYY-MM-DD'
    floatfrequency (int): la fréquence de paiement pour la jambe variable en mois
    fixedfrequency (int): la fréquence de paiement pour la jambe fixe en mois
    discountindex (float): L'indicateur à considérer pour le taux sans risque. 'SOFR', 'BGCR' ou 'TGCR'
    """
    def __init__(self, direction:str, notional:float, fixedrate:float, maturitydate:str, 
                valuedate:str, floatfrequency:int, fixedfrequency:int, discountindex='SOFR'): 
                #discountindex = SOFR ou BGCR ou TGCR
        self.direction = direction.lower()
        self.notional = notional
        self.fixedrate = fixedrate
        self.maturitydate =  pd.to_datetime(maturitydate, format= "%Y-%m-%d")
        self.valuedate = pd.to_datetime(valuedate, format= "%Y-%m-%d")
        self.floatfrequency = floatfrequency
        self.fixedfrequency = fixedfrequency
        self.discountindex = discountindex
        if self.direction == 'pay':
            self.fixedmultiplier = -1
        else:
            self.fixedmultiplier = 1

    def PrintSwapDetails(self):
        """ 
        Afficher quelques détails du swap.
        """

        swapdetails = 'Direction: ' + str(self.direction)+ '\n' + ' fixed rate: ' \
            + str(self.fixedrate) +'\n Date of value: '+ str(self.valuedate)+ '\n Maturity: ' \
            + str(self.maturitydate) + '\n notional: ' + str(self.notional)

        print(swapdetails)

    def recup_data(self):
        """ 
        Récupération des données de taux forward et de taux historiques.
        """
        NYFedRates = pd.read_excel("src/data/NYFedRates.xlsx")
        NYFedRates = NYFedRates[NYFedRates['Rate Type']== self.discountindex]
        NYFedRates['Effective Date'] = pd.to_datetime(NYFedRates['Effective Date']).dt.strftime("%d/%m/%Y")
        self.HistRates = NYFedRates[["Effective Date", "Rate Type", "Rate (%)"]] #format de date 'MM/DD/YYYY'
        # Taux d'intérêts SOFR estimés sur le site https://www.commloan.com/research/rate-calculator/
        ratecurve = [[1/12, 0.0533], 
                    [3/12, 0.0531],
                    [6/12, 0.0512],
                    [1, 0.0464],
                    [3, 0.0373],
                    [5, 0.0356], 
                    [7, 0.0354],
                    [10, 0.0356],
                    [15, 0.0362],
                    [30, 0.0348]]

        self.ratecurve = pd.DataFrame(ratecurve, columns = ["tenor", "rate"])


if __name__ == "__main__" :
    testSwap = Swap("pay", 100000, 0.05, '2025-01-14', '2024-01-14', 6, 6, 'SOFR')
    testSwap.PrintSwapDetails()
    testSwap.recup_data()
    print(testSwap.HistRates)
    print(testSwap.ratecurve)
