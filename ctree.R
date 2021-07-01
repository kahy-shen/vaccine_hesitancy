library(party)
covid_data <- read.csv(file="/Users/keshen/Desktop/covidR_(3.21).csv", header=T)
covid_data$vaccine <- as.factor(covid_data$vaccine)
covid_data$gender<-as.factor(covid_data$gender)
covid_data$employed_situation<-as.factor(covid_data$employed_situation)
covid_data$ethnicity<-as.factor(covid_data$ethnicity)
covid_data$education<-as.factor(covid_data$education)
covid_data$party<-as.factor(covid_data$party)
covid_data$trust_in_government<-as.factor(covid_data$trust_in_government)

head(covid_data)

apart.data <- function(covid_data, percent = 0.7) {
  train.index <- sample(c(1:nrow(covid_data)),round(percent*nrow(covid_data)))
  covid_data.train <- covid_data[train.index,]
  covid_data.test <- covid_data[-c(train.index),]
  result <- list(train = covid_data.train, test = covid_data.test)
  result
}
p.data <- apart.data(covid_data)
covid_data.train <- p.data$train
covid_data.test <- p.data$test

fit.ctree <- ctree(vaccine~.,data = covid_data, control = ctree_control(mincriterion=0.99, maxdepth=4))  #生成条件决策树

plot(fit.ctree,main = 'Conditional Inference Tree', font.main="Serif", cex.main = 3) #画出决策树
table(covid_data$vaccine, predict(fit.ctree))