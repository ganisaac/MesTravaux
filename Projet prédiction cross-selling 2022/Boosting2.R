library(ggplot2)
library(rpart)
library(randomForest)
library(plotly)
library(xgboost)
library(caret)

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

## nombre d'arbre optimal correspondant à eta 
iters <- sapply(1:length(etas), function(ee){
  paramsTemp <- xgb_params
  paramsTemp$eta <- etas[ee]
  xgbcv <- xgb.cv(params = paramsTemp, data = dbTrain, metrics = "rmse",
                  nrounds = 600, nfold = 5, nthread=4, verbose = FALSE)
  iter <- as.numeric(xgbcv$evaluation_log[which(xgbcv$evaluation_log$test_rmse_mean == min(xgbcv$evaluation_log$test_rmse_mean)), "iter"][1])
  return(iter)
})

plot(etas,iters)

## Erreur de prédiction
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
plot(etas,errors)

eta<- 5/30
xgb_para<- list(booster = "gbtree", objective = "binary:logistic",
                eta=eta, gamma=0, max_depth=5,min_child_weight=1, 
                subsample=1,colsample_bytree=1,
                lambda = 0, alpha = 0,
                eval_metric = "rmse")
xgbcv <- xgb.cv(params = xgb_para, data = dbTrain, metrics = "rmse",
                nrounds = 600, nfold = 5, nthread=4, verbose = FALSE)
n_iter_eta <- as.numeric(xgbcv$evaluation_log[which(xgbcv$evaluation_log$test_rmse_mean == min(xgbcv$evaluation_log$test_rmse_mean)), "iter"][1])


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

### on choisit donc sto=0.95; gam=1; iter= 100

sto<-0.95
gam<-1
n_iter<- 1000

### train final

params_xgb<- list(booster = "gbtree", objective = "binary:logistic",
                eta=eta, gamma=gam, max_depth=5,min_child_weight=1, 
                subsample=sto,colsample_bynode=sto,
                lambda = 0, alpha = 0,
                eval_metric = "rmse")

xgb_fin <- xgb.train(params = xgb_para, data = dbTrain, nthread = 4,
                 nrounds = n_iter,verbose = FALSE)


### prédictions

prediction<- predict(xgb_fin, as(as.matrix(test_data[,-9]),"dgCMatrix"))
prediction<- as.numeric(prediction>0.5)



conf_mat<-confusionMatrix(factor(prediction), factor(as.numeric(test_data$Response)), mode="everything", positive = "1")
print(conf_mat)
