library(dplyr)
library(lmtest)
library(nlme)

data_pe <- read.csv("~/Travail webscraping/Results/data_final.csv", stringsAsFactors=TRUE)

data_pe$appellationlibelle <- as.factor(data_pe$appellationlibelle)
data_pe$typeContrat <- as.factor(data_pe$typeContrat)
data_pe$moisCreation<- recode(data_pe$moisCreation, "2023-01-01" = "Janvier 2023", "2023-02-01" = "Février 2023",
                                        "2023-03-01" = "Mars 2023", "2023-04-01" = "Avril 2023", "2023-05-01" = "Mai 2023", 
                                        "2023-06-01" = "Juin 2023", "2023-07-01" = "Juillet 2023", "2023-08-01" = "août 2023")
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
data_pe$qualification <- factor(data_pe$qualification, levels = c("Aucune formation scolaire", "Primaire à 4ème", "4ème achevée", 
                                                                  "3ème achevée ou Brevet", "2nd ou 1ère achevée", "CAP, BEP et équivalents",
                                                                  "Bac ou équivalent", "Bac+2 ou équivalents", "Bac+3, Bac+4 ou équivalents",
                                                                  "Bac+5 et plus ou équivalents", ""))

data_pe$csp <- factor(data_pe$csp, levels = c("Manouvre", "Ouvrier qualifié (P1,P2)", "Ouvrier qualifié (P3,P4,OHQ)", "Ouvrier spécialisé", 
                                              "Employé non qualifié", "Employé qualifié", "Technicien", "Agent de maîtrise", "Cadre", ""))

data_pe$lsalaire <- log(data_pe$salaireCorr)

# modèle de régression simple

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

## Validation du modèle 

residus <- reglin2$residuals

mean(residus)

plot(residus)
plot(density(residus), main = "Densité des résidus")

# Test d'homoscédasticité des résidus 

bptest(reglin2) # test de Breush-Pagan
# On rejette l'hypothèse nulle d'homoscédasticité

# Test de normalité des résidus
shapiro.test(residus) #test de Shapiro Wilk
ks.test(residus, "pnorm") #test de Kolmogorov Smirnov
#On rejette l'hypothèse nulle de non normalité

qqnorm(residus)
qqline(residus)

# Autocorrélation des résidus 
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
