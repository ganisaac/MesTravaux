from src.business.objects.swap import Swap

import pandas as pd
import numpy as np
import math
import copy
from scipy.optimize import fsolve

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

class SwapPricer :
    """ Classe permettant de pricer un swap de taux
    swap (Swap): le swap à pricer
    valuationdate (str): Date de pricing au format 'YYYY-MM-DD'
    """
    def __init__(self, swap:Swap, valuationdate:str):
        self.swap = swap
        self.swap.recup_data()
        self.valuationdate = pd.to_datetime(valuationdate, format= "%Y-%m-%d")
    
    def DiscountRate(self, dateval, frequency):
        """ 
        Calcul du taux obligataire pour une maturité donnée par dateval
        """

        tenor =  (dateval - self.valuationdate).days / 365.25
        interpolatedrate = np.interp(tenor, self.swap.ratecurve['tenor'], self.swap.ratecurve['rate'])
        frequency = 12 / frequency
        return np.exp(-interpolatedrate*tenor)

    def ForwardRate(self, datefrom, frequency):
        """ 
        Calcul du taux forward pour une maturité donnée par datefrom+frquency
        """

        tenorfrom =  (datefrom - self.valuationdate).days / 365.25
        interpolatedratefrom = np.interp(tenorfrom, self.swap.ratecurve['tenor'], self.swap.ratecurve['rate'])

        dateto =  datefrom + pd.DateOffset(months = frequency)
        tenorto = (dateto - self.valuationdate).days / 365.25
        interpolatedrateto = np.interp(tenorto, self.swap.ratecurve['tenor'], self.swap.ratecurve['rate'])

        frequency = 12 / frequency

        return (np.exp(-interpolatedratefrom*tenorfrom)/np.exp(-interpolatedrateto*tenorto)-1) * frequency


    def CreateRollSchedule(self, leg:str):
        """ Création d'un programme de paiements pour une jambe qui renvoie une liste de  
        [la date courante de paiement, le taux forward, le taux obligataire, la prochaine date de paiement]
        leg (str) : 'fixed' pour la jambe fixe ou 'float' pour la jambe variable
        """
        if leg == 'fixed':
            legfrequency = self.swap.fixedfrequency
        elif leg=='float':
            legfrequency = self.swap.floatfrequency
        else:
            raise ValueError("Veuillez choisir comme paramètre leg 'fixed' ou 'float'")

        leg = str(leg) + 'frequency'
        legschedule = []
        nextrolldate = self.swap.valuedate
        i = 0

        while nextrolldate < self.swap.maturitydate:
            histrates = self.swap.HistRates
            if leg == 'fixedfrequency':
                currentrolldate = self.swap.valuedate + pd.DateOffset(months = i * self.swap.fixedfrequency)
                nextrolldate = self.swap.valuedate + pd.DateOffset(months = (i+1) * self.swap.fixedfrequency)
                forwardrate = self.swap.fixedrate
                
            else:
                currentrolldate = self.swap.valuedate + pd.DateOffset(months = i * self.swap.floatfrequency)
                nextrolldate = self.swap.valuedate + pd.DateOffset(months = (i+1) * self.swap.floatfrequency)

                #if currentrolldate is in the past, obtain a fixing instead of a forward rate
                if currentrolldate <= self.valuationdate:
                    forwardrate = histrates.loc[histrates['Effective Date'] 
                        == currentrolldate.strftime('%d/%m/%Y'), 'Rate Type']
                    if forwardrate.empty:
                        print ('Missing Fixing Rate for ' + currentrolldate.strftime('%Y/%m/%d'))
                        exit()
                    else:
                        forwardrate = forwardrate.values[0]
                else:
                    forwardrate = self.ForwardRate(currentrolldate,self.swap.floatfrequency)


            paydatediscountrate = self.DiscountRate(nextrolldate, legfrequency)
            legscheduleelement = np.array([[currentrolldate, forwardrate, 
                paydatediscountrate, nextrolldate]])

            if i == 0:
                legschedule = legscheduleelement
            else:
                legschedule = np.vstack((legschedule, legscheduleelement))
            i = i + 1

        return legschedule

    def LegPV(self, leg, notional):
        """ 
        Calcul du prix d'une jambe
        """
        legschedule = self.CreateRollSchedule(leg)
        pv = 0
        for row in legschedule:
            pv = pv + notional * float(row[1]) * float(row[2]) \
                * (row[3]-row[0]).days / 365.25    

        return pv
    

    def swap_price(self) :
        """ 
        Calcul du prix du swap
        """

        floatlegschedule = self.CreateRollSchedule('float')
        if (self.swap.fixedfrequency == self.swap.floatfrequency):
            fixedlegschedule = copy.copy(floatlegschedule)
            fixedlegschedule = [[elt[0], self.swap.fixedrate, elt[2], elt[3]] for elt in fixedlegschedule]
        else:
            fixedlegschedule = self.CreateRollSchedule('fixed')

        #presentvalue = self.LegPV('fixed') - self.LegPV('float')
        presentvalue = self.LegPV('fixed', self.swap.notional * self.swap.fixedmultiplier) \
        + self.LegPV('float', self.swap.notional * -self.swap.fixedmultiplier)

        return presentvalue


if __name__ == "__main__" :
    testSwap = Swap("pay", 100000, 0.05, '2025-01-14', '2024-01-15', 6, 6, 'SOFR')
    testSwap.PrintSwapDetails()
    testswappricer = SwapPricer(testSwap, "2024-01-14")
    print(testswappricer.LegPV('fixed', 100000))
    print(testswappricer.LegPV('float', -100000))
    print(f"Le prix que vous devez payer pour ce swap est: {-testswappricer.swap_price()}")



