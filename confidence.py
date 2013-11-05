import numpy as np
from pylab import *
import scipy as sp
import scipy.stats
import statsmodels.formula.api as sm

data1 = [53,38,29]
data2 = [16,29,32,34,40,44,49,51,52,53]
data3=[45, 55, 67, 45, 68, 79, 98, 87, 84, 82]
#data3 = np.random.normal(loc=39,scale=10,size=30)
data = [data1,data2,data3]

def do_error_bar(x,e,lw=2,w=2):
    o = plot([x,x],[m+e,m-e],color='k',lw=lw)
    o = plot([x-w,x+w],[m+e,m+e],color='k',lw=lw)
    o = plot([x-w,x+w],[m-e,m-e],color='k',lw=lw)

#layout from 1 to 100
N = len(data)
total = 100
margin = 5
space = 15
fig_width = total - margin*2
all_spaces = (N-1)*space
total_group_width = fig_width - all_spaces
group_width = total_group_width * 1.0 / N

dx = group_width/3.0    # 4 elements per group
x = margin              # start
#tD = {3:3.182, 10:2.228, 30:2.042}
S = 50                  # large circle size
s = 10                  # small circle size
y = 5                  # y pos for text

for group in data:
    for g in group:
        scatter(x,g,s=s,color='k')

    x += dx
    n = len(group)
    m = np.mean(group)
    sd = np.std(group,ddof=1)
    scatter(x,m,s=S,color='k')
    do_error_bar(x,sd)
    text(x-1.5,y,'SD')
    text(x,y-5,'n = ' + str(n))

    x += dx
    se = sd/np.sqrt(n)
    print "SD : ",sd
    print "SE : ",se
#    t = tD[n]
    print sp.stats.t._ppf((1+0.95)/2., n-1)
    ci = se * sp.stats.t._ppf((1+0.95)/2., n-1)
    scatter(x,m,s=S,color='k')
    do_error_bar(x,ci)
    text(x-1.5,y,'CI')

    x += dx
    scatter(x,m,s=S,color='k')
    do_error_bar(x,se)
    text(x-1.5,y,'SE')
    x += space

ax = axes()
ax.xaxis.set_visible(False)
show()
