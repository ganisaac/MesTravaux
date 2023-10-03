library(tseries)
library("forecast")

data_ts <- read.csv("~/Travail webscraping/Results/data_ts2.csv")


data_ts <- data_ts[-c(1)]
data_ts<- na.omit(data_ts)
data_ts <- ts(data_ts[,c(2,3)], frequency = 1, names = c("mean_salaries", "median_salaries"))
print(data_ts)

plot.ts(data_ts)

moyennes = data_ts[,1]
medianes  = data_ts[,2]

plot.ts(moyennes, xlab = "jour", ylab = "salaire moyen", main = "Evolution du salaire moyen par jour")
plot.ts(medianes, xlab = "jour", ylab = "salaire médian", main = "Evolution du salaire médian par jour")

## test de stationnarité 

adf_test_moy <- adf.test(moyennes)
adf_test_med <- adf.test(medianes)

print(adf_test_moy)
print(adf_test_med)

test_trend_moy <- lm(moyennes~seq(1,length(moyennes)))
summary(test_trend_moy)

test_trend_med <- lm(medianes~seq(1,length(medianes)))
summary(test_trend_med)

## séries différenciées

diff_moy <- diff(moyennes)
diff_med <- diff(medianes)

plot.ts(diff_moy, xlab = "jour", ylab = "salaire moyen différencié", main = "Evolution du salaire moyen différencié par jour")
plot.ts(diff_med, xlab = "jour", ylab = "salaire médian différencié", main = "Evolution du salaire médian différencié par jour")

adf_test_moy <- adf.test(diff_moy)
adf_test_med <- adf.test(diff_med)

print(adf_test_moy)
print(adf_test_med)

test_trend_moy2 <- lm(diff_moy~seq(1,length(diff_moy)))
summary(test_trend_moy2)

test_trend_med2 <- lm(diff_med~seq(1,length(diff_med)))
summary(test_trend_med2)

## Identification

acf(diff_moy)
pacf(diff_moy)  ## AR(1), AR(6)


acf(diff_med)
pacf(diff_med)  ## AR(1)

## Estimation des paramètres

est_moy <- arima(moyennes, order = c(1,1,0))
est_moy2 <- arima(moyennes, order = c(6,1,0))
est_med <- arima(medianes, order = c(1,1,0))

print(est_moy)
print(est_moy2)
print(est_med)

## Vérification 
residus_moy <- est_moy$residuals
residus_moy2 <- est_moy2$residuals
residus_med <- est_med$residuals

acf(residus_moy)
acf(residus_moy2)
acf(residus_med)

Box.test(residus_moy)
Box.test(residus_moy2)
Box.test(residus_med)

## Prévision

forecast_moy <- forecast(est_moy2, h = 30, )



