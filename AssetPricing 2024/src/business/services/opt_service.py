from src.business.objects.option import Option
from src.business.objects.person import Person
from src.business.services.bs_formula import BS_formula
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from scipy.interpolate import interp2d
from scipy.optimize import minimize_scalar
from scipy.stats import norm

import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import warnings

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

class OptionsService:
    """
    Permet de faire quelques opérations utiles sur les options
    """
    
    def get_relative_maturity(self,maturities:list):
        """
        Transforme les dates en durée relativement à la date de récupération 
        des données qui est considérée comme la date de pricing pour l'option Européenne.
        maturities (list): liste contenant les dates à transformer en durée.
        """
        maturities= pd.to_datetime(maturities, format='%Y-%m-%d')

        initial_date = datetime(2023, 12, 8)
        relative_maturities = []
        
        for maturity in maturities:
            temp_maturity = datetime(maturity.year, maturity.month, maturity.day)
            rel_maturity = relativedelta(temp_maturity, initial_date)
            rel_maturity = rel_maturity.years + rel_maturity.months / 12.0 + rel_maturity.days / 365.25
            relative_maturities.append(rel_maturity)    
        return relative_maturities

    def calcul_impl_volatility(self,option:Option,person: Person):
        """
        Calcul la volatilité implicite d'une option
        option (Option): Objet de type option
        person (Person): Renferme le type de l'option
        """

        if option.name=="APPLE":
            name="APPLE"
        elif option.name=="AMAZON":
            name="AMAZON"
        elif option.name=="ALI BABA":
            name="ALI BABA"
        elif option.name=="GOOGLE":
            name="GOOGLE"
        elif option.name=="META":
            name="META"
        elif option.name=="MICROSOFT":
            name="MICROSOFT"
        elif option.name=="SONY":
            name="SONY"
        elif option.name=="TESLA":
            name="TESLA"
        df= pd.read_csv(f'src/data/clean_final_ListAllOptions{name}.csv')
        
        strike=option.K
        strikes=df['Strike']
        types=df['Type']
        volatilities=df['implied Volatility']

        relative_maturities = self.get_relative_maturity(df['Maturity'])
        
        option_in_data = False
        index_in_data = None
        for i in range(len(df)):
            if relative_maturities[i] ==option.T and strikes[i]==option.K and types[i] == person.type:
                option_in_data == True
                index_in_data = i
            if option_in_data:
                break       
        if option_in_data:
            volatility = float(df["implied Volatility"].iloc[index_in_data])
        else :
            interp_func = interp2d(strikes, relative_maturities, volatilities, kind='linear')
            volatility = interp_func(option.K, option.T)
            
        return volatility

    def calcul_hist_volatility(self,option,person):
        """
        Calcul la volatilité historique. Pour cela on se sert des données sur l'historique des prix du sous jacent depuis l'année 2021(post covid).
        option (Option): Objet de type option
        person (Person): Renferme le type de l'option
        """
        df= pd.read_csv(f'src/data/StockPrices{option.name}.csv')

        returns = np.log(df['close'] / df['close'].shift(1))
        
        historical_volatility = np.std(returns) * np.sqrt(252)
          
        return historical_volatility

    def plot_volatilities(self, option, person):

        df = pd.read_csv(f'src/data/clean_ListAllOptions{option.name}.csv')
        relative_maturities = np.array(self.get_relative_maturity(df['Maturity']))
        strikes= np.array(df['Strike'])
        volatilities= np.array(df['implied Volatility'])
        print(volatilities)

        fig = go.Figure(data=[go.Surface(
            x=strikes,
            y=relative_maturities,
            z=volatilities,
            
            )])
        # modify the axis to correspond to the data range
        # make the relative maturities axis logarithmic
        fig.update_layout(title='Implied Volatility Surface',
                          scene = dict(
                          xaxis_title='Strike',
                          yaxis_title='Relative Maturity',
                          zaxis_title='Implied Volatility',
                          xaxis=dict(range=[-10+min(strikes), max(strikes)+10],),
                          yaxis=dict(range=[-0.2+min(relative_maturities), max(relative_maturities)]+0.2,),
                          zaxis=dict(range=[min(volatilities), max(volatilities)],),),                          
                          autosize=False,
                          width=800, height=800,
                          margin=dict(l=65, r=50, b=65, t=90))
        
        fig.write_html('first_figure.html', auto_open=True)
        
        

if __name__ == "__main__":
    P=Person('Call')
    O=Option('Google', 100, 100, 1)
    opt_service=OptionsService()
    print("Options Data:")
    print("Volatility:")
    print(opt_service.calcul_impl_volatility(O,P))
    opt_service.plot_volatilities(O, P)
    
    