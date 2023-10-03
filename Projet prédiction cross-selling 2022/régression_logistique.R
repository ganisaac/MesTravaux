library("caret")
parts = createDataPartition(cleaned_base$Response, p = 0.8, list = F)
train_data= cleaned_base[parts,]
test_data= cleaned_base[-parts, ]

### Estimation du modèle logit
logistic_reg<- glm(Response~Gender+Age+Driving_License+Region_Code+Previously_Insured+
                     Vehicle_Damage+Annual_Premium+Vintage+inf_1+between_1_and_2,
                   family = binomial(link = "logit"),
                   data=train_data)
summary(logistic_reg)


##prédiction 
variabl<-matrix(c(test_data$Gender, test_data$Age, test_data$Driving_License, test_data$Region_Code,
    test_data$Previously_Insured, test_data$Vehicle_Damage, test_data$Annual_Premium, 
    test_data$Vintage, test_data$inf_1, test_data$between_1_and_2),
    ncol=10, byrow = FALSE)
logit_val<- variabl%*%(logistic_reg$coefficients[-1])+ logistic_reg$coefficients[1]

logit_prd<- exp(logit_val)/(1+exp(logit_val))

### prédictions

prediction<- as.numeric(logit_prd>0.5)
print(prediction)


conf_mat<-confusionMatrix(factor(prediction), factor(as.numeric(test_data$Response)), mode="everything", positive = "1")
print(conf_mat)

### nouvelle base nettoyée
new_cleaned_base<- cleaned_base[,-c(4,8)]
write.table(new_cleaned_base, "cleaned_base.csv", sep = ";", row.names=FALSE)
parts = createDataPartition(new_cleaned_base$Response, p = 0.8, list = F)
train_data= new_cleaned_base[parts,]
test_data= new_cleaned_base[-parts, ]


