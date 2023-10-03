library(Hmisc)
library(dplyr)
library(corrplot)
library(ggplot2)
library(plotly)
library(xgboost)
library(caret)
################################ GESTION DE LA BASE#########################################

base<-read.csv("C:/Users/HP/Documents/cours_ENSEA/ISE_2/Data science/Projet/groupe_12_train.csv")

##Transformation de la variable Gender
for(i in 1:length(base$Gender)){
  if(base$Gender[i]=="Male") base$Gender[i]<-1
  if(base$Gender[i]=="Female") base$Gender[i]<-0
}
mode(base$Gender)<- "integer"

## Décomposition de la variable Vehicle_Age
for(i in 1:length(base$Vehicle_Age)){
  if(base$Vehicle_Age[i]=="< 1 Year") base$inf_1[i]<-1
  if(base$Vehicle_Age[i]!="< 1 Year") base$inf_1[i]<-0
}

for(i in 1:length(base$Vehicle_Age)){
  if(base$Vehicle_Age[i]=="1-2 Year") base$between_1_and_2[i]<-1
  if(base$Vehicle_Age[i]!="1-2 Year") base$between_1_and_2[i]<-0
}

for(i in 1:length(base$Vehicle_Age)){
  if(base$Vehicle_Age[i]=="> 2 Years") base$sup_2[i]<-1
  if(base$Vehicle_Age[i]!="> 2 Years") base$sup_2[i]<-0
}
base<- select(base, -Vehicle_Age)

##Transformation de la variable Vehicle_Damage
for(i in 1:length(base$Vehicle_Damage)){
  if(base$Vehicle_Damage[i]=="Yes") base$Vehicle_Damage[i]<-1
  if(base$Vehicle_Damage[i]=="No") base$Vehicle_Damage[i]<-0
}
mode(base$Vehicle_Damage)<- "integer"

##Suppression de la variable Policy_Sales_Channel
base<- select(base, -Policy_Sales_Channel)

###Suppression des valeurs aberrantes
Age_outlier<- boxplot.stats(base$Age)$out
length(Age_outlier)
Age_outlier_idx<- which(base$Age %in% c(Age_outlier))

prem_outlier<-boxplot.stats(base$Annual_Premium)$out
length(prem_outlier)
prem_outlier_idx<- which(base$Annual_Premium %in% c(prem_outlier))

vint_outlier<- boxplot.stats(base$Vintage)$out
length(vint_outlier)
vint_outlier_idx<- which(base$Vintage %in% c(vint_outlier))

un_outlier_idx= union(Age_outlier_idx, union(vint_outlier_idx, prem_outlier_idx))
cleaned_base<- base[-un_outlier_idx,]



##################################### ANALYSE EXPLORATOIRE ############################
describe(base)

### Analyse univariee
boxplot(cleaned_base$Age, ylab="Age", main= "Distribution de l'âge")
boxplot(cleaned_base$Annual_Premium, ylab="montant", main= "Distribution du montant premium anuuel")
boxplot(cleaned_base$Vintage, ylab="Vintage", main= "Distribution de l'ancienneté du client")

### Analyse bivariée

boxplot(Age~Gender, cleaned_base, ylab="Age", main="Représentation de l'âge en fonction du sexe")
boxplot(Annual_Premium~Gender, cleaned_base, ylab="Montant", main="Représentation du montant premium en fonction du sexe")
boxplot(Vintage~Gender, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté en fonction du sexe")

boxplot(Age~Driving_License, cleaned_base, ylab="Age", main="Représentation de l'âge en fonction de l'obtention du permis")
boxplot(Annual_Premium~Driving_License, cleaned_base, ylab="Montant", main="Représentation du montant premium en fonction de l'obtention du permis")
boxplot(Vintage~Driving_License, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté en fonction de l'obtention du permis")

boxplot(Age~Driving_License, cleaned_base, ylab="Age", main="Représentation de l'âge en fonction de l'obtention du permis")
boxplot(Annual_Premium~Driving_License, cleaned_base, ylab="Montant", main="Représentation du montant premium en fonction de l'obtention du permis")
boxplot(Vintage~Driving_License, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté en fonction de l'obtention du permis")

boxplot(Age~Previously_Insured, cleaned_base, ylab="Age", main="Représentation de l'âge selon que le client soit assuré ou pas")
boxplot(Annual_Premium~Previously_Insured, cleaned_base, ylab="Montant", main="Représentation du montant premium selon que le client soit assuré ou pas")
boxplot(Vintage~Previously_Insured, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté selon que le client soit assuré ou pas")

boxplot(Age~Vehicle_Damage, cleaned_base, ylab="Age", main="Représentation de l'âge selon que le client ait déjà endommagé son véhicule ou pas")
boxplot(Annual_Premium~Vehicle_Damage, cleaned_base, ylab="Montant", main="Représentation du montant premium selon que le client ait déjà endommagé son véhicule ou pas")
boxplot(Vintage~Vehicle_Damage, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté selon que le client ait déjà endommagé son véhicule ou pas")

boxplot(Age~inf_1, cleaned_base, ylab="Age", main="Représentation de l'âge selon que le client ait un véhicule de moins d'un an ou pas")
boxplot(Annual_Premium~inf_1, cleaned_base, ylab="Montant", main="Représentation du montant premium selon que le client ait un véhicule de moins d'un an ou pas")
boxplot(Vintage~inf_1, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté selon que le client ait un véhicule de moins d'un an ou pas")

boxplot(Age~between_1_and_2, cleaned_base, ylab="Age", main="Représentation de l'âge selon que le client ait un véhicule d'entre un et deux ans ou pas")
boxplot(Annual_Premium~between_1_and_2, cleaned_base, ylab="Montant", main="Représentation du montant premium selon que le client ait un véhicule d'entre un et deux ans ou pas")
boxplot(Vintage~between_1_and_2, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté selon que le client ait un véhicule d'entre un et deux ans ou pas")

boxplot(Age~Gender, cleaned_base, ylab="Age", main="Représentation de l'âge en fonction du sexe")
boxplot(Annual_Premium~Gender, cleaned_base, ylab="Montant", main="Représentation du montant premium en fonction du sexe")
boxplot(Vintage~Gender, cleaned_base, ylab="Nombre de jours", main="Représentation de l'ancienneté en fonction du sexe")

boxplot(Age~Response, cleaned_base, ylab="Age", names = c("not interested", "interested"), main="Représentation de l'âge en fonction de la réponse")
boxplot(Region_Code~Response, cleaned_base, ylab="Region", names = c("not interested", "interested"), main="Représentation de la région en fonction de la réponse")
boxplot(Annual_Premium~Response, cleaned_base, ylab="Montant", names= c("not interested", "interested"),main="Montant premium en fonction de la réponse")
boxplot(Vintage~Response, cleaned_base, ylab="Nombre de jours", names= c("not interested", "interested"), main="Représentation de l'ancienneté en fonction de la réponse")


barplot(table(cleaned_base[which(cleaned_base$Gender==1),]$Response)/sum(cleaned_base$Gender), xlab="réponse",names.arg = c("not interested", "interested"), ylab="effectif", col="grey", main="proportion des réponses pour les hommes")
barplot(table(cleaned_base[which(cleaned_base$Gender==0),]$Response)/(length(cleaned_base$Gender)-sum(cleaned_base$Gender)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="effectif", col="grey", main="proportion des réponses pour les femmes")

plot(cleaned_base$Age, cleaned_base$Response, xlab="Age", ylab="Réponse", main="Réponse des clients selon l'âge")

barplot(table(cleaned_base[which(cleaned_base$Driving_License==1),]$Response)/sum(cleaned_base$Driving_License), xlab="réponse",names.arg = c("not interested", "interested"), ylab="pourcentage", col="grey", main="Avec permis de conduire")
barplot(table(cleaned_base[which(cleaned_base$Driving_License==0),]$Response)/(length(cleaned_base$Gender)-sum(cleaned_base$Driving_License)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="pourcentage", col="grey", main="Sans permis de conduire")

plot(cleaned_base$Region_Code, cleaned_base$Response, xlab="Région", ylab="Réponse", main = "Réponse des clients vs la région")

barplot(table(cleaned_base[which(cleaned_base$Previously_Insured==1),]$Response)/sum(cleaned_base$Previously_Insured), xlab="réponse",names.arg = c("not interested", "interested"), ylab="Pourcentage", col="grey", main="possession d'une assurance automobile")
barplot(table(cleaned_base[which(cleaned_base$Previously_Insured==0),]$Response)/(length(cleaned_base$Gender)-sum(cleaned_base$Previously_Insured)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="Pourcentage", col="grey", main="Non possession d'une assurance automobile")

barplot(table(cleaned_base[which(cleaned_base$Vehicle_Damage==1),]$Response)/sum(cleaned_base$Vehicle_Damage), xlab="réponse",names.arg = c("not interested", "interested"), ylab="Pourcentage", col="grey", main="Clients ayant déjà endommagé leur véhicule")
barplot(table(cleaned_base[which(cleaned_base$Vehicle_Damage==0),]$Response)/(length(cleaned_base$Vehicle_Damage)-sum(cleaned_base$Gender)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="Pourcentage", col="grey", main="Clients n'ayant jamais endommagé leur véhicule")

barplot(table(cleaned_base[which(cleaned_base$inf_1==1),]$Response)/sum(cleaned_base$inf_1), xlab="réponse",names.arg = c("not interested", "interested"), ylab="Pourcentage", col="grey", main="Véhicule âgé de moins d'un an")
barplot(table(cleaned_base[which(cleaned_base$inf_1==0),]$Response)/(length(cleaned_base$Gender)-sum(cleaned_base$inf_1)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="Pourcentage", col="grey", main="Véhicule agé de plus d'un an")

barplot(table(cleaned_base[which(cleaned_base$between_1_and_2==1),]$Response)/sum(cleaned_base$between_1_and_2), xlab="réponse",names.arg = c("not interested", "interested"), ylab="Pourcentage", col="grey", main="Véhicule âgé d'entre un et 2 ans")
barplot(table(cleaned_base[which(cleaned_base$between_1_and_2==0),]$Response)/(length(cleaned_base$Gender)-sum(cleaned_base$between_1_and_2)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="Pourcentage", col="grey", main="Véhicule d'un âge non compris entre 1 et 2")

barplot(table(cleaned_base[which(cleaned_base$sup_2==1),]$Response)/sum(cleaned_base$sup_2), xlab="réponse",names.arg = c("not interested", "interested"), ylab="Pourcentage", col="grey", main="Véhicule âgé de plus de 2 ans")
barplot(table(cleaned_base[which(cleaned_base$sup_2==0),]$Response)/(length(cleaned_base$sup_2)-sum(cleaned_base$between_1_and_2)),names.arg = c("not interested", "interested"), xlab="réponse", ylab="Pourcentage", col="grey", main="Véhicule d'un âge inférieur à 2")

####Matrice de corrélation
corrplot(cor(cleaned_base))



################################# ESTIMATION DU MODELE #################################

## partition de la base train
parts = createDataPartition(cleaned_base$Response, p = 0.8, list = F)
train_data= cleaned_base[parts,]
test_data= cleaned_base[-parts, ]

## data management
dbX <- as(as.matrix(train_data[,-9]),"dgCMatrix")
dbY <- as.numeric(train_data$Response)
dbTrain <- xgb.DMatrix(data = dbX, label = dbY)
varN <- colnames(train_data[,-9])


### Train et importance des variables 

xgb_params <- list(booster = "gbtree", objective = "binary:logistic",
                   eta=0.1, gamma=0, max_depth=5,min_child_weight=1, 
                   subsample=1,colsample_bytree=1,
                   lambda = 0, alpha = 0,
                   eval_metric = "rmse")

xgb_deb <- xgb.train(params = xgb_params, data = dbTrain, nthread = 4,
                     nrounds = 50,verbose = FALSE)

importance <- xgb.importance(feature_names = varN, model = xgb_deb)
xgb.plot.importance(importance_matrix = importance, main= "Importance des variables")


### Tuning des hyperparametres

etas <- (1:10)/40

######## Cross validation
nfold <- 5
folds <- cut(seq(1,nrow(train_data)),breaks=nfold,labels=FALSE)

xgb_params <- list(booster = "gbtree", objective = "binary:logistic",
                   eta=0.1, gamma=0, max_depth=5,min_child_weight=1, 
                   subsample=1,colsample_bytree=1,
                   lambda = 0, alpha = 0,
                   eval_metric = "rmse")

## nombre d'arbre optimal correspondant à chaque eta 
iters <- sapply(1:length(etas), function(ee){
  paramsTemp <- xgb_params
  paramsTemp$eta <- etas[ee]
  xgbcv <- xgb.cv(params = paramsTemp, data = dbTrain, metrics = "rmse",
                  nrounds = 600, nfold = 5, nthread=4, verbose = FALSE)
  iter <- as.numeric(xgbcv$evaluation_log[which(xgbcv$evaluation_log$test_rmse_mean == min(xgbcv$evaluation_log$test_rmse_mean)), "iter"][1])
  return(iter)
})

plot(etas,iters)

## Erreur de prédiction correspondant à chaque eta
errors <- sapply(1:length(etas), function(ee){
  errorFolds <- sapply(1:nfold, function(kk){
    ## Data management
    train <- train_data[which(folds != kk),]
    dbX <- as(as.matrix(train[,-7]),"dgCMatrix")
    dbY <- as.numeric(train$Response)
    dbTrain <- xgb.DMatrix(data = dbX, label = dbY)
    test <- train_data[which(folds == kk),]
    dbX <- as(as.matrix(test[,-7]),"dgCMatrix")
    dbY <- as.numeric(test$Response)
    dbTest <- xgb.DMatrix(data = dbX, label = dbY)
    ## Training & predicting
    paramsTemp <- xgb_params
    paramsTemp$eta <- etas[ee]
    xgb <- xgb.train(params = paramsTemp, data = dbTrain, nthread =4 ,
                     nrounds = iters[ee],verbose = FALSE)
    res <- sqrt(mean((predict(xgb,dbTest)-dbY)^2))
    return(res)
  })
  return(mean(errorFolds))
})
plot(etas,errors)  ### on prend eta = 5/40

eta<- 5/40

### Tuning de sub/col/gamma

xgb_param <- list(booster = "gbtree", objective = "binary:logistic",
                  eta=eta, gamma=1, max_depth=3,min_child_weight=1, 
                  subsample=1,colsample_bynode=1,
                  lambda = 1, alpha = 0,
                  eval_metric = "rmse")

## Corresponding nrounds
hyperp <- expand.grid(sto = c(0.95,0.9,0.85,0.8),gam= c(0,1,3,5,10),KEEP.OUT.ATTRS = FALSE)
iters2 <- sapply(1:nrow(hyperp), function(ii){
  paramsTemp <- xgb_param
  paramsTemp$colsample_bynode <- hyperp$sto[ii]
  paramsTemp$subsample <- hyperp$sto[ii]
  paramsTemp$gamma <- hyperp$gam[ii]
  xgbcv <- xgb.cv(params = paramsTemp, data = dbTrain, metrics = "rmse",
                  nrounds = 1500, nfold = 5, nthread=4, verbose = FALSE)
  iter <- as.numeric(xgbcv$evaluation_log[which(xgbcv$evaluation_log$test_rmse_mean == min(xgbcv$evaluation_log$test_rmse_mean)), "iter"][1])
  return(iter)
})
hyperp$iter <- iters2
plot_ly(data=hyperp,x=~sto,y=~gam,z=~iter,type = "heatmap")


## Estimating prediction error
errors2 <- sapply(1:nrow(hyperp), function(ii){
  errorFolds <- sapply(1:nfold, function(kk){
    ## Data management
    # Train
    train <- train_data[which(folds != kk),]
    dbX <- as(as.matrix(train[,-7]),"dgCMatrix")
    dbY <- as.numeric(train$Response)
    dbTrain <- xgb.DMatrix(data = dbX, label = dbY)
    # Test
    test <- train_data[which(folds == kk),]
    dbX <- as(as.matrix(test[,-7]),"dgCMatrix")
    dbY <- as.numeric(test$Response)
    dbTest <- xgb.DMatrix(data = dbX, label = dbY)
    ## Training & predicting
    paramsTemp <- xgb_param
    paramsTemp$colsample_bynode <- hyperp$sto[ii]
    paramsTemp$subsample <- hyperp$sto[ii]
    paramsTemp$gamma <- hyperp$gam[ii]
    xgb <- xgb.train(params = paramsTemp, data = dbTrain, nthread = 4,
                     nrounds = hyperp$iter[ii],verbose = FALSE)
    res <- sqrt(mean((predict(xgb,dbTest)-dbY)^2))
    return(res)
  })
  return(mean(errorFolds))
})
hyperp$error <- errors2
plot_ly(data=hyperp,x=~sto,y=~gam,z=~error,type = "heatmap")

### on choisit donc sto=0.95; gam=1; iter= 1500

sto<-0.95
gam<-1
n_iter<- 1500

### train final

params_xgb<- list(booster = "gbtree", objective = "binary:logistic",
                  eta=eta, gamma=gam, max_depth=5,min_child_weight=1, 
                  subsample=sto,colsample_bynode=sto,
                  lambda = 0, alpha = 0,
                  eval_metric = "error")

xgb_fin <- xgb.train(params = params_xgb, data = dbTrain, nthread = 4,
                     nrounds = n_iter,verbose = FALSE)


### prédictions

prediction<- predict(xgb_fin, as(as.matrix(test_data[,-9]),"dgCMatrix"))
prediction<- as.numeric(prediction>0.5)

conf_mat<-confusionMatrix(factor(prediction), factor(as.numeric(test_data$Response)), mode="everything", positive = "1")
print(conf_mat)



######################## FICHIER DE PREDICTIONS ###################################

test<-read.csv("C:/Users/HP/Documents/cours_ENSEA/ISE_2/Data science/Projet/groupe_12_test.csv")

# préparation de la base test 

##Transformation de la variable Gender
for(i in 1:length(test$Gender)){
  if(test$Gender[i]=="Male") test$Gender[i]<-1
  if(test$Gender[i]=="Female") test$Gender[i]<-0
}
mode(test$Gender)<- "integer"

## Décomposition de la variable Vehicle_Age
for(i in 1:length(test$Vehicle_Age)){
  if(test$Vehicle_Age[i]=="< 1 Year") test$inf_1[i]<-1
  if(test$Vehicle_Age[i]!="< 1 Year") test$inf_1[i]<-0
}

for(i in 1:length(test$Vehicle_Age)){
  if(test$Vehicle_Age[i]=="1-2 Year") test$between_1_and_2[i]<-1
  if(test$Vehicle_Age[i]!="1-2 Year") test$between_1_and_2[i]<-0
}

for(i in 1:length(test$Vehicle_Age)){
  if(test$Vehicle_Age[i]=="> 2 Years") test$sup_2[i]<-1
  if(test$Vehicle_Age[i]!="> 2 Years") test$sup_2[i]<-0
}
test<- select(test, -Vehicle_Age)

##Transformation de la variable Vehicle_Damage
for(i in 1:length(test$Vehicle_Damage)){
  if(test$Vehicle_Damage[i]=="Yes") test$Vehicle_Damage[i]<-1
  if(test$Vehicle_Damage[i]=="No") test$Vehicle_Damage[i]<-0
}
mode(test$Vehicle_Damage)<- "integer"

##Suppression de la variable Policy_Sales_Channel
test<- select(test, -Policy_Sales_Channel)


### Predictions

prediction<- predict(xgb_fin, as(as.matrix(test[,-1]),"dgCMatrix"))
prediction<- as.numeric(prediction>0.5)

fichier_prediction <- data.frame(test$id)
colnames(fichier_prediction)<- c("id")
fichier_prediction$Response<- prediction


##################### fichier de prédiction
write.table(fichier_prediction, "groupe_12_prédictions.csv", sep = ";", row.names=FALSE)
