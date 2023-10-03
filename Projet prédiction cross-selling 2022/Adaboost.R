library(adabag)
library(caret) 
### premier modèle
parts = createDataPartition(data$Species, p = 0.8, list = F)
model_adaboost <- adabag::boosting(Response~., data=new_cleaned_base, boos=TRUE, mfinal=100, control = (minsplit = 0), coeflearn = 'Breiman')

summary(model_adaboost)

pred_test = predict(model_adaboost, test)

cvmodel = boosting.cv(Species~., data=iris, boos=TRUE, mfinal=10, v=5)