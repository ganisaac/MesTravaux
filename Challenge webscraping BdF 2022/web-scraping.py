from bs4 import BeautifulSoup
from requests import get
import pandas as pd

result = []
for i in range(1,501) :
    base = "https://www.france-emploi.com"
    lien = "https://www.france-emploi.com/recherche-emploi/-/"
    page = get(lien+str(i))
    soup = BeautifulSoup(page.text, "html.parser")
    liste_soup = soup.find_all("li", {"class": "uneAnn"})
    for html in liste_soup :
        annonce = html.find("div", {"class" : "offer-info"})
        offre = []
        try:
            offre.append(annonce.find("h2", {"class" : "poste"}).a.attrs['title'])
        except : 
            offre.append(None)
        try :
            offre.append(base+annonce.find("h2", {"class" : "poste"}).a.attrs['href'])
        except :
            offre.append(None)
        try :
            offre.append(annonce.find("li", {"class":"date"}).text.strip()[:10])
        except :
            offre.append(None)
        try : 
            offre.append(annonce.find("li", {"class":"localisation"}).find("span").text.strip())
        except : 
            offre.append(None)
        try :
            offre.append(annonce.find("li", {"class":"contrat"}).attrs['title'])
        except :
            offre.append(None)
        try : 
            texte = annonce.find("li", {"class":"salaire"}).find("span").text.replace("\u202f", "").replace("\xa0", "")
            offre.append(texte)
            type_salaire = texte.split(",")[0]
            offre.append(type_salaire)
            sal = ""
            for txt in texte.split(",")[1:]:
                sal += txt+","
            sal = sal[:-1]
        except :
            offre.append(None)
            offre.append(None)
        if offre[-1] != None :
            try :
                if "à partir de" in texte :
                    borne_inf = sal[13:]
                elif "jusqu'à" in texte :
                    borne_sup = sal[9:]
                elif (("de" in texte) and ("à" in texte)) :
                    borne_inf = sal.split("à")[0][4:]
                    borne_sup = sal.split("à")[1][1:]
                else :
                        borne_inf = sal
                        borne_sup = sal
                offre.append(borne_inf)
                offre.append(borne_sup)
            except :
                offre.append(None)
                offre.append(None)
        else :
            offre.append(None)
            offre.append(None)
        
        try : 
            offre.append(annonce.find("div", {"class":"teaser"}).text.strip())
        except :
            offre.append(None)
        result.append(offre)

data_salaries = pd.DataFrame(result, columns = ["emploi", "lien", "date", "localisation", "contrat", "salaire", "type de salaire", "salaire minimum", "salaire maximum", "descriptif"])

data_salaries.to_csv(r"C:\Users\HP\Documents\ENSAI\Projet salaires BdF\données d'offres d'emploi en France.csv")
    
