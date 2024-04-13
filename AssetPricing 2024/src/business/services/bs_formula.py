from src.business.objects.option import Option
from src.business.objects.person import Person
import pandas as pd
import numpy as np
from scipy.stats import norm



class BS_formula:
    """ 
    Objet qui se charge de faire les calculs liés à la formule de Black Scholes pour les options Européennes.
    option (Option): Option à pricer
    person (Person): Renferme le type de l'option
    sigma (float): volatilité
    """

    def __init__(self, option:Option,person:Person,sigma:float): 
            
        self.s0 = option.S0 # underlying asset price
        self.k = option.K # stike price
        self.r = option.r # risk-free rate
        self.person=person
        self.option=option
        self.sigma=sigma
        self.T = option.T # time 2 maturity
        self.d1 = (np.log(self.s0/self.k)+(self.r+self.sigma**2/2)*self.T) / (self.sigma * np.sqrt(self.T))
        self.d2 = ((np.log(self.s0/self.k)+(self.r+self.sigma**2/2)*self.T) / (self.sigma * np.sqrt(self.T))) - self.sigma*np.sqrt(self.T)
        
    def BS_price(self): 
        """ 
        Prix de l'option par la formule fermée du modèle de Black Scholes.
        """
        c = self.s0*norm.cdf(self.d1) - self.k*np.exp(-self.r*self.T)*norm.cdf(self.d2)
        p = self.k*np.exp(-self.r*self.T)*norm.cdf(-self.d2) - self.s0*norm.cdf(-self.d1)
        
        if self.person.type=='Call':
            return c
        else:
            return p
        
        
    def BS_delta(self): 
        """ 
        Calcul du delta 
        """
        delta_call = norm.cdf(self.d1)
        delta_put = norm.cdf(self.d1)-1
        if self.person.type=='Call':
            return delta_call
        else: 
            return delta_put
        
    
    def BS_gamma(self): 
        """
        Calcul du gamma
        """
        
        gamma_put_call= norm.pdf(self.d1)/(self.s0*self.sigma*np.sqrt(self.T))
        return gamma_put_call
    
    def BS_vega(self): 
        """ 
        Calcul du vega 
        """
        vega_put_call= self.s0*np.sqrt(self.T)*norm.pdf(self.d1)
        return vega_put_call
    
    def BS_theta(self):
        """ 
        Calcul du theta
        """ 
        c_theta = -self.s0*norm.pdf(self.d1)*self.sigma / (2*np.sqrt(self.T)) - self.r*self.k*np.exp(-self.r*self.T)*norm.cdf(self.d2)
        p_theta = -self.s0*norm.pdf(self.d1)*self.sigma / (2*np.sqrt(self.T)) + self.r*self.k*np.exp(-self.r*self.T)*norm.cdf(-self.d2)
        
        if self.person.type=='Call':
            return c_theta
        else:
            return p_theta
        
    def BS_rho(self): 
        """ 
        Calcul du rho
        """ 
        if self.person.type=='Call':
            return self.k*self.T*np.exp(-self.r*self.T)*norm.cdf(self.d2)
        else:
            return -self.k*self.T*np.exp(-self.r*self.T)*norm.cdf(-self.d2)
        


if __name__ == "__main__":
    from business.services.opt_service import OptionsService
    
    P=Person('Call')
    for name in ['Apple', 'Amazon', 'Ali baba', 'Google', 'Meta', 'Microsoft', 'Sony', 'Tesla']:
        print(name)
        O=Option(name=name, K=50, T=0,r=0.052 )
        opt_service=OptionsService()
        print("Options Data:")
        opt_service.get_options_data(O,P)
        
        #print("Implied Volatilities:")
        #print(opt_service.get_volatilities(O,P))
        
        print("Volatility:")
        sigma=opt_service.calcul_impl_volatility(O,P)
        print(f"{sigma[0]:.2f}")

        # Create an instance of the Black-Scholes model
        print("BS Price:")
        bsm = BS_formula( O, P,sigma)

        # Calculate option prices
        call_price = bsm.BS_price()

        print(f"The theoretical price of the option is: {call_price[0]:.2f}")

        print(30 * "-")
        
        delta = bsm.BS_delta()
        print(f"The delta of the option is: {delta[0]:.2f}")
        
    
    