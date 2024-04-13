# asset-pricing

Ce projet a pour objectif de pricer différents types de produits dérivés: des options Européennes et Asiatiques, des straddles et des swaps de taux.

Nous utilisons à chaque fois, l'équation de Black Scholes. Les options Européennes sont pricées grâce aux formules fermées tandis que les options Asiatiques sont pricées grâce à des simulations de Monte Carlo. 

Nous avons utilisé Dash Plotly pour créer notre application.

## Page 1: Pricing d'options Européennes

Entrées:

- Sous jacent: L'actif sous jacent;
- Type: Call ou Put;
- Maturité: Date de maturité. Nous considérons que la date de pricing est la date de récupération de nos données donc le 08/12/2023;
- S0: Prix du sous jacent à la date de pricing. Par défaut, nous prenons le prix du sous jacent à la date du 08/12/2023;
- Strike: le Strike;
- Taux d'intérêt: le taux d'intérêt.

Sorties:

- Volatilité implicite: La volatilité implicite de l'option selon les entrées fournies;
- Prix de l'option: Le prix de l'option selon les entrées fournies;
- Grecques de l'option: Les grecques de l'option selon les entrées fournies;
- Graphiques des greques en fonction du prix du sous-jacent: **Ce graphe pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée. Veuillez patienter s'il vous plaît**
        - Entrées additionnelles: Grecque (delta, gamma, vega, theta ou rho) le grecque désiré/ Min et Max les valeurs inférieure et supérieure de la tranche de prix à considérer
        - Sortie: Courbe du grec de l'option spécifiée sur la plage considérée
- Graphiques des greques en fonction du strike: **Ce graphe pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée. Veuillez patienter s'il vous plaît**
        - Entrées additionnelles: Grecque (delta, gamma, vega, theta ou rho) le grecque désiré/ Min et Max les valeurs inférieure et supérieure de la tranche de strike à considérer
        - Sortie: Courbe du grec de l'option spécifiée sur la plage considérée
- Volatilité implicite: Dans notre démarche nous avons dû calculer puis stocker les volatilités implicites pour chaque sous jacent, chaque strike et chaque maturité. Ce graphe représente donc la volatilité implicite en fonction du strike et de la maturité, pour le sous jacent choisi.

## Page 2: Pricing de straddle

Dans cette page nous priçons un straddle, produit structuré composé d'un call et d'un put sur un même sous jacent. Nous considérons que le call et le put ont un S0 commun et une maturité commune mais des strikes différents.

Entrées:

- Sous jacent: L'actif sous jacent;
- Maturité: Date de maturité. Nous considérons que la date de pricing est la date de récupération de nos données donc le 08/12/2023;
- S0: Prix du sous jacent à la date de pricing. Par défaut, nous prenons le prix du sous jacent à la date du 08/12/2023;
- Strike call: le Strike du call associé;
- Strike put: le Strike du put associé;
- Taux d'intérêt: le taux d'intérêt.

Sorties:

- Volatilités implicites: Les volatilités implicites du call et du put selon les entrées fournies;
- Prix du straddle: Le prix du straddle selon les entrées fournies;
- Grecques du straddle: Les grecques du straddle selon les entrées fournies;
- Graphiques des greques en fonction du prix du sous-jacent: **Ce graphe pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée, en particulier lorsque la plage de prix augmente. Veuillez patienter s'il vous plaît**
        - Entrées additionnelles: Grecque (delta, gamma, vega, theta ou rho) le grecque désiré/ Min et Max les valeurs inférieure et supérieure de la tranche de prix à considérer
        - Sortie: Courbe du grec du straddle spécifié en faisant varier le prix du sous jacent sur la plage considérée.
- Graphiques des greques en fonction du strike Call: **Ce graphe pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée, en particulier lorsque la plage de strike augmente. Veuillez patienter s'il vous plaît**
        - Entrées additionnelles: Grecque (delta, gamma, vega, theta ou rho) le grecque désiré/ Min et Max les valeurs inférieure et supérieure de la tranche de strike à considérer pour le call
        - Sortie: Courbe du grec du straddle spécifié en faisant varier le strike du call sur la plage considérée
- Graphiques des greques en fonction du strike Put: **Ce graphe pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée, en particulier lorsque la plage de strike augmente. Veuillez patienter s'il vous plaît**
        - Entrées additionnelles: Grecque (delta, gamma, vega, theta ou rho) le grecque désiré/ Min et Max les valeurs inférieure et supérieure de la tranche de strike à considérer pour le put
        - Sortie: Courbe du grec du straddle spécifié en faisant varier le strike du put sur la plage considérée
- Volatilité implicite: Dans notre démarche nous avons dû calculer puis stocker les volatilités implicites pour chaque sous jacent, chaque strike et chaque maturité. Ce graphe représente donc la volatilité implicite en fonction du strike et de la maturité, pour le sous jacent choisi.


# Page 3: Pricing de swaps de taux

Entrées:
- Direction : Pay ou Receive. 
              Pay lorsque le client achète le taux fixe. Le prix en valeur absolue est alors ce qu'il doit donner en échange du contrat.
              Receive lorsque le client vend le taux fixe. Le prix en valeur absolue est alors ce qu'il doit recevoir en échange du contrat.
- Notionnel: Le notionnel du contrat;
- Date de pricing: La date qu'on considère comme instant de pricing;
- Index taux: L'index qu'on choisit pour les taux sans risque, lorsqu'on utilise des taux historiques. L'index pour les taux forward est le SOFR;
- Date de valeur: La date d'entrée dans le contrat;
- Maturité: La maturité ou date de fin du contrat;
- Fréquence de la jambe fixe: Nous avons choisi de différé les fréquences de paiement pour les jambes fixes et variables. Il s'agit de la fréquence pour la jambe fixe exprimée en mois;
- Fréquence de la jambe variable: Il s'agit de la fréquence pour la jambe variable exprimée en mois;
- Taux fixe : Le taux fixe.

Sorties:
- Taux obligataires B(t,T) avec t la date de pricing et T la date de valeur T1 ou la date de maturité Tn. On distingue le calcul pour la jambe fixe et pour la jambe variable car les fréquences de paiement des deux jambes sont éventuellement différentes;
- Valeur de jambe: Les valeurs des jambes fixe et variable;
- Prix du swap: La différence entre les valeurs des deux jambes, avec le signe correspondant à la direction.

## Page 4: Pricing d'options Asiatiques

Entrées:

- Sous jacent: L'actif sous jacent;
- Type: Call ou Put;
- Maturité: Date de maturité. Nous considérons que la date de pricing est la date de récupération de nos données donc le 08/12/2023;
- S0: Prix du sous jacent à la date de pricing. Par défaut, nous prenons le prix du sous jacent à la date du 08/12/2023;
- Strike: le Strike;
- Taux d'intérêt: le taux d'intérêt.
- Simulations le nombre de simulations de Monte Carlo
- Fenêtre: La fenêtre en jours ouvrés à considérer pour le calcul de la moyenne des prix. Par défaut la vaeur de 20 jours ouvrés correspond approximativement à un mois.


Sorties:

- Volatilité historique: La volatilité historique obtenue en se servant de l'historique des cours du sous jacent;
- Prix de l'option: Le prix de l'option selon les entrées fournies. **Cette sortie pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée, en particulier lorsque le nombre de simulations de Monte Carlo est grand. Veuillez patienter s'il vous plaît**;
- Grecques de l'option: Les grecques (delta, gamma, vega) de l'option selon les entrées fournies. les grecques sont calculés par la méthode des différences finies. **Cette sortie pourrait demander quelques secondes de patience avant d'apparaitre ou après le changement des valeurs d'entrée, en particulier lorsque le nombre de simulations de Monte Carlo est grand. Veuillez patienter s'il vous plaît**. Les grecques sont assez peu stables et héritent des limites de la méthode utilisée pour les estimer à savoir le problème de convergence et les assez grandes erreurs d'approximation.