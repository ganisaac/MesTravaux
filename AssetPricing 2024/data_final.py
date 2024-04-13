
from src.business.objects.option import Option
from src.business.objects.person import Person
from src.business.services.bs_formula import BS_formula
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta




class Clean_data_final:
    def get_options_data(self, option,person):
        """
        Get options data for a given symbol and time period.
        """
        
        if option.name=="APPLE":
            name="aapl"
        elif option.name=="AMAZON":
            name="amzn"
        elif option.name=="ALI BABA":
            name="baba"
        elif option.name=="GOOGLE":
            name="googl"
        elif option.name=="META":
            name="meta"
        elif option.name=="MICROSOFT":
            name="msft"
        elif option.name=="SONY":
            name="sony"
        elif option.name=="TESLA":
            name="tsla"
        
        df= pd.read_csv(f'src/data/cleaned_ListAllOptions{name}.csv')
        
       
        df_filtered=df[df['Type']==person.type]
        return df
    
    def get_relative_maturity(self,maturities):
        maturities= pd.to_datetime(maturities, format='%Y-%m-%d')

        initial_date = datetime(2023, 12, 8)
        relative_maturities = []
        
        for maturity in maturities:
            temp_maturity = datetime(maturity.year, maturity.month, maturity.day)
            rel_maturity = relativedelta(temp_maturity, initial_date)
            rel_maturity = rel_maturity.years + rel_maturity.months / 12.0 + rel_maturity.days / 365.25
            relative_maturities.append(rel_maturity)    
        return relative_maturities
    
    def get_volatilities(self,option,person):
        df=self.get_options_data(option,person)
        
        
        strikes=df['Strike']
        prices=df['Last Price']
        
        volatilities = []

        relative_maturities = self.get_relative_maturity(df['Maturity'])
        
        
        types = df['Type']

        for i in range(len(strikes)):
            option=Option(name=option.name,K=strikes.iloc[i],T=relative_maturities[i],r=option.r)
            
            person=Person(types.iloc[i])
            
            objective_function = lambda sigma: (BS_formula(option,person,sigma).BS_price() - prices.iloc[i])**2
           
            result = minimize_scalar(objective_function)
            
            implied_vol = result.x
            volatilities.append(implied_vol)
        
        df['implied Volatility']=volatilities
        
        
        chemin_csv = f"src/data/clean_final_ListAllOptions{option.name}.csv"  
        
        df.to_csv(chemin_csv, index=False)
        
        
        return df
    
    
# Test the code to get all data
for name in ['Apple', 'Amazon', 'Ali baba', 'Google', 'Meta', 'Microsoft', 'Sony', 'Tesla']:
    
    name=name.upper()
    option=Option(name=name,K=100,T=1,r=0.052)
    person=Person("Call")
    clean_data_final=Clean_data_final()
    clean_data_final.get_volatilities(option,person)
