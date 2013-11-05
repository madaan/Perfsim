#sg
from numpy import arange,array,ones,linalg
from pylab import *
import csv
import pandas as pd
import statsmodels.formula.api as sm
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.stats
#from scipy.stats import norm
import math
data=[45, 55, 67, 45, 68, 79, 98, 87, 84, 82]
a=1.0*np.array(data)
n=len(a)
m=np.mean(a)
n, min_max, mean, var, skew, kurt =sp.stats.describe(a)
std=math.sqrt(var)	#Standard Deviation
print "VAR ",var
print "SD ",std
x=std/math.sqrt(n)
print "Standard Error : ",x
print "T values : ",sp.stats.t._ppf((1+0.95)/2., n-1)
h = x * sp.stats.t._ppf((1+0.95)/2., n-1)
print "MEAN : ",mean," CONFIDENCE INTERVAL : ",mean-h,mean+h	#Mean and 98% confidence interval


#range = np.arange(min_max[0], min_max[1], 1)
#print range
#plt.plot(range, norm.pdf(range, mean, std))
#plt.show()
head=["exp","waittime"]
with open('regression.csv','wb') as f:
	writer=csv.writer(f)
	writer.writerow(head)
	writer.writerow([1,2])
	writer.writerow([4,5])
	writer.writerow([3,8])
	writer.writerow([4,12])
	writer.writerow([8,14])
	writer.writerow([9,19])
	writer.writerow([8,22])
mydata=pd.read_csv('regression.csv')
model = sm.ols(formula='exp ~ waittime', data=mydata)
fitted = model.fit()
#print fitted.summary()
#print fitted.fittedvalues
#plt.plot(mydata["exp"], mydata["waittime"], 'ro')
#plt.plot(mydata["exp"], fitted.fittedvalues, 'b')
plt.ylim(0, 25)
plt.xlim(0, 10)
#plt.show()
print "( Coefficient of Correlation , Probability value for testing non-correlation )",scipy.stats.pearsonr([1,4,3,4,8,9,8], [2,5,8,12,14,19,22])	#Coefficient of Correlation &
x=[1,4,3,4,8,9,8]
y=[2,5,8,12,14,19,22]
X=[3,4,4.5,5,5.5,6,6.5,7,7.5]
Y=[0.1,0.2,0.25,0.32,0.33,0.35,0.47,0.49,0.53]
print "( Slope, Intercept, r-value(Correlation Coefficient), p-value, Standard Error of the Estimate ) ",scipy.stats.linregress(x,y)
#b=array(1,4,3,4,8,9,8)
#A = array([b,ones(9)])
#y=[2,5,8,12,14,19,22]
#w = linalg.lstsq(A.T,y)[0]

(m,b)=polyfit(x,y,1)
print m,b
yp=polyval([m,b],x)
plt.plot(x,yp)
scatter(x,y)
plt.show()
