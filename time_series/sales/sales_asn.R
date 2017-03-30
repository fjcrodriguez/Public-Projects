setwd("~/googledrive/Analytics/msan604/AS1/")
rm(list=ls())

sales <- read.table("SALES.txt")
sales <- ts(sales, start=1999, frequency=12)

t <- time(sales)
t2 <- t^2
month <- as.factor(cycle(sales))

trend_reg <- lm(sales~ t + t2)
plot(sales)
points(t,predict.lm(trend_reg),type='l',col='red')

# Quadratic trend fits the movement of the data extremely well. From visual inspection, the 
# curve pass through the center of each cycle, capturing the overall movement of the data equally. 


trend_reg <- lm(sales~ t + t2 + month)
plot(sales)
points(t,predict.lm(trend_reg),type='l',col='red')


t.new <- seq(2011,2012,length=13)[1:12] 
t2.new <- t.new^2
month.new <- factor(rep(1:12,1)) 

new <- data.frame(t=t.new, t2=t2.new, month=month.new)
pred <- predict.lm(trend_reg,new,interval='prediction')
  
plot(sales,xlim=c(1999,2012),ylim=c(0,80)) #plotting the data

abline(v=2011,col='blue',lty=2)
lines(pred[,1]~t.new,type='l',col='red')
lines(pred[,2]~t.new,col='green') 
lines(pred[,3]~t.new,col='green')
