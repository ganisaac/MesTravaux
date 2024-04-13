class Option:
    """ 
    Définit un objet représentant une option.
    name (str): Nom du ticker représentant l'option
    K (float): strike
    T (float): maturité en années
    r (float): taux d'intérêt. La valeur par défaut est 0.052
    S0 (float): prix actuel de l'option
    """
    def __init__(self, name:str, K:float, T:float, r=0.052, S0=None):
        self.name = name.upper()
        if S0 is None:
            self.S0 = self.default_price(self.name)
        else:
            self.S0 = S0
        self.K = K        # Option strike price
        self.T = T        # Time to expiration
        self.r = r        # Risk-free interest rate

    def default_price(self, name: str):
        """ 
        Prix par défaut de l'option, constaté à l'instant téléchargement des données.
        name(str): Ticker de l'option 
        """
        prices = {
            "APPLE": 182.01,
            "AMAZON": 145.68,
            "ALI BABA": 73.22,
            "GOOGLE": 137.65,
            "META": 351.77,
            "MICROSOFT": 368.63,
            "SONY": 91.60,
            "TESLA": 238.93
        }
        return prices.get(name, 0)  # Retourne 0 si le nom n'est pas trouvé
