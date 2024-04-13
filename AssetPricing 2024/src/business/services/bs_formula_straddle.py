from src.business.objects.option import Option
from src.business.objects.person import Person
import pandas as pd
import numpy as np
from scipy.stats import norm



class BS_formula_Straddle:
    """ 
    Objet qui se charge de faire les calculs liés à la formule de Black Scholes pour les straddles.
    call (Option): Call
    put (Option): Put
    sigmac (float): volatilité du call
    sigmap (float): volatilité du put
    """

    def __init__(self, call:Option, put:Option, sigmac:float, sigmap:float): 
            
        self.s0 = call.S0 # underlying asset price
        self.kc = call.K # stike for the call
        self.kp = put.K
        self.r = call.r # risk-free rate
        self.call =call
        self.put = put
        self.sigmac=sigmac
        self.sigmap= sigmap
        self.T = call.T # time 2 maturity

        self.d1_c = (np.log(self.s0/self.kc)+(self.r+self.sigmac**2/2)*self.T) / (self.sigmac * np.sqrt(self.T))
        self.d2_c = ((np.log(self.s0/self.kc)+(self.r+self.sigmac**2/2)*self.T) / (self.sigmac * np.sqrt(self.T))) - self.sigmac*np.sqrt(self.T)
        self.d1_p = (np.log(self.s0/self.kp)+(self.r+self.sigmap**2/2)*self.T) / (self.sigmap * np.sqrt(self.T))
        self.d2_p = ((np.log(self.s0/self.kp)+(self.r+self.sigmap**2/2)*self.T) / (self.sigmap * np.sqrt(self.T))) - self.sigmap*np.sqrt(self.T)
        
    def BS_price(self): 
        """ 
        Prix par la formule de Black Scholes. 
        Somme du prix du call (calculé avec sa maturité et sa volatilité propres) et 
        du prix du put (calculé avec sa maturité et sa volatilité propres)
        """
        c = self.s0*norm.cdf(self.d1_c) - self.kc*np.exp(-self.r*self.T)*norm.cdf(self.d2_c)
        p = self.kp*np.exp(-self.r*self.T)*norm.cdf(-self.d2_p) - self.s0*norm.cdf(-self.d1_p)
        
        return p+c
        
        
    def BS_delta(self): 
        """ 
        Calcul du delta. Somme des delta du call et du put, chacun avec ses caractéristiques propres.
        """
        delta_call = norm.cdf(self.d1_c)
        delta_put = norm.cdf(self.d1_p)-1
        return delta_call+delta_put
        
    
    def BS_gamma(self): 
        """
        Calcul du gamma. Somme des gamma du call et du put, chacun avec ses caractéristiques propres
        """

        return norm.pdf(self.d1_c)/(self.s0*self.sigmac*np.sqrt(self.T)) + norm.pdf(self.d1_p)/(self.s0*self.sigmap*np.sqrt(self.T))
    
    def BS_vega(self): 
        """ 
        Calcul du vega. Somme des vega du call et du put, chacun avec ses caractéristiques propres 
        """
        return  self.s0*np.sqrt(self.T)*norm.pdf(self.d1_c) +  self.s0*np.sqrt(self.T)*norm.pdf(self.d1_p)
    
    def BS_theta(self):
        """ 
        Calcul du theta. Somme des theta du call et du put, chacun avec ses caractéristiques propres
        """ 
        c_theta = -self.s0*norm.pdf(self.d1_c)*self.sigmac / (2*np.sqrt(self.T)) - self.r*self.kc*np.exp(-self.r*self.T)*norm.cdf(self.d2_c)
        p_theta = -self.s0*norm.pdf(self.d1_p)*self.sigmap / (2*np.sqrt(self.T)) + self.r*self.kp*np.exp(-self.r*self.T)*norm.cdf(-self.d2_p)
        
        return c_theta+p_theta
        
    def BS_rho(self): 
        """ 
        Calcul du rho. Somme des rho du call et du put, chacun avec ses caractéristiques propres
        """ 
        rho_c = self.kc*self.T*np.exp(-self.r*self.T)*norm.cdf(self.d2_c)
        rho_p = -self.kp*self.T*np.exp(-self.r*self.T)*norm.cdf(-self.d2_p)
        return rho_c+rho_p
        


if __name__ == "__main__":
    from src.business.services.opt_service import OptionsService
    Pc = Person("Call")
    Pp = Person("Put")
    for name in ['Apple', 'Amazon', 'Ali baba', 'Google', 'Meta', 'Microsoft', 'Sony', 'Tesla']:
        print(name)
        C=Option(name=name, K=60, T=0,r=0.052 )
        P = Option(name=name, K=50, T=0,r=0.052 )
        opt_service=OptionsService()
        
        print("Volatility:")
        sigmap=opt_service.calcul_impl_volatility(P,Pp)
        print(f"{sigmap[0]:.2f}")
        sigmac=opt_service.calcul_impl_volatility(C,Pc)
        print(f"{sigmac[0]:.2f}")


        print("BS Price:")
        bsm_s = BS_formula_Straddle(C, P, sigmac, sigmap)

        straddle_price = bsm_s.BS_price()

        print(f"The theoretical price of the Straddle is: {straddle_price[0]:.2f}")

        print(30 * "-")
        
        delta_s = bsm_s.BS_delta()
        print(f"The delta of the option is: {delta_s[0]:.2f}")
        
    
    