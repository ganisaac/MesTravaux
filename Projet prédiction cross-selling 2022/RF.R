library(randomForest)
random_for <- randomForest(data=train_data, factor(Response) ~ ., ntree = 500, mtry = sqrt(ncol(train_data)-1),
                   nodesize = 1,maxnodes=NULL)
random_for$predicted
random_for$type

varImpPlot(random_for, main = "Importance des variables de la base")

plot(random_for, main = "Stabilisation de l'erreur OOB")

errorVar <- sapply(1:(ncol(train_data)-1),function(ii){
  return(tail(randomForest(data=train_data,factor(Response)~.,maxnodes=NULL, mtry = ii, ntree = 500)$err.rate[,1], 1) )
})
plot(errorVar)
### 4 covariables conviendraient

errorNod <- sapply((1:5)*100,function(ii){
  errs <-replicate(5,{tail(randomForest(data=train_data,factor(Response)~.,maxnodes=ii,mtry = 4, ntree = 500)$err.rate[,1], 1)})
  return(mean(errs))
})
plot(x=(1:5)*100,y=errorNod)
### 500

### random_forest final

random_for1 <- randomForest(data=train_data, factor(Response) ~ ., ntree = 500, mtry = 4, nodesize = 1,maxnodes=NULL)

prediction<- predict(random_for1, test_data)
### résultats 
random_for1$type
random_for1$predicted
random_for1$confusion

conf_mat<-confusionMatrix(factor(prediction), factor(as.numeric(test_data$Response)), mode="everything", positive = "1")
print(conf_mat)
