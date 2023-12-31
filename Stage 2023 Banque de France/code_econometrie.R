library(dplyr)
library(lmtest)
library(nlme)

data_pe <- read.csv("~/Travail webscraping/Results/data_final.csv", stringsAsFactors=TRUE)

data_pe$appellationlibelle <- as.factor(data_pe$appellationlibelle)
data_pe$typeContrat <- as.factor(data_pe$typeContrat)
data_pe$moisCreation<- recode(data_pe$moisCreation, "2023-01-01" = "Janvier 2023", "2023-02-01" = "F�vrier 2023",
                                        "2023-03-01" = "Mars 2023", "2023-04-01" = "Avril 2023", "2023-05-01" = "Mai 2023", 
                                        "2023-06-01" = "Juin 2023", "2023-07-01" = "Juillet 2023", "2023-08-01" = "ao�t 2023")
data_pe$moisCreation <- as.factor(data_pe$moisCreation)
data_pe$departement <- as.factor(data_pe$departement)
data_pe$secteurActivite <- as.factor(data_pe$secteurActivite)
data_pe$romeLibelle <- as.factor(data_pe$romeLibelle)
data_pe$romeCode <- as.factor(data_pe$romeCode)
data_pe$experienceExige <- as.factor(data_pe$experienceExige)
data_pe$indic_compl <- as.factor(data_pe$indic_compl)
data_pe$indic_alter <- as.factor(data_pe$indic_alter)
data_pe$section_rome <- as.factor(data_pe$section_rome)
data_pe$dureeTravailLibelleConverti <- as.factor(data_pe$dureeTravailLibelleConverti)
data_pe$csp <- as.factor(data_pe$qualificationLibelle)
data_pe$codeNAF <- as.factor(data_pe$codeNAF)
data_pe$metier_agg <- as.factor(data_pe$metier_agg)
data_pe$qualification <- as.factor(data_pe$qualification)
data_pe$qualification <- factor(data_pe$qualification, levels = c("Aucune formation scolaire", "Primaire � 4�me", "4�me achev�e", 
                                                                  "3�me achev�e ou Brevet", "2nd ou 1�re achev�e", "CAP, BEP et �quivalents",
                                                                  "Bac ou �quivalent", "Bac+2 ou �quivalents", "Bac+3, Bac+4 ou �quivalents",
                                                                  "Bac+5 et plus ou �quivalents", ""))

data_pe$csp <- factor(data_pe$csp, levels = c("Manouvre", "Ouvrier qualifi� (P1,P2)", "Ouvrier qualifi� (P3,P4,OHQ)", "Ouvrier sp�cialis�", 
                                              "Employ� non qualifi�", "Employ� qualifi�", "Technicien", "Agent de ma�trise", "Cadre", ""))

data_pe$lsalaire <- log(data_pe$salaireCorr)

# mod�le de r�gression simple

reglin <- lm(lsalaire ~ metier_agg + secteurActivite + departement + typeContrat + moisCreation + 
               indic_compl + experienceExige + indic_alter+ nb_formations + dureeTravailLibelleConverti + 
               csp + qualification,
             data = data_pe)

options(max.print = 4000)

summary(reglin)


reglin2 <- lm(lsalaire ~ metier_agg + secteurActivite + departement + typeContrat + 
                indic_compl + experienceExige + indic_alter+ nb_formations + dureeTravailLibelleConverti + 
                csp + qualification,
              data = data_pe)

summary(reglin2)

## Validation du mod�le 

residus <- reglin2$residuals

mean(residus)

plot(residus)
plot(density(residus), main = "Densit� des r�sidus")

# Test d'homosc�dasticit� des r�sidus 

bptest(reglin2) # test de Breush-Pagan
# On rejette l'hypoth�se nulle d'homosc�dasticit�

# Test de normalit� des r�sidus
shapiro.test(residus) #test de Shapiro Wilk
ks.test(residus, "pnorm") #test de Kolmogorov Smirnov
#On rejette l'hypoth�se nulle de non normalit�

qqnorm(residus)
qqline(residus)

# Autocorr�lation des r�sidus 
Box.test(residus, type = "Ljung-Box")

gls_model <- gls(lsalaire ~ metier_agg + secteurActivite + departement + typeContrat + 
                   indic_compl + experienceExige + indic_alter+ nb_formations + dureeTravailLibelleConverti + 
                   csp + qualification,
                 data = data_pe, na.action = na.omit)
sort(gls_model$coefficients)
gls_model$fitted
gls_model$call

summary(gls_model)
residus_gls <- gls_model$residuals

qqnorm(residus_gls)
qqline(residus_gls)
