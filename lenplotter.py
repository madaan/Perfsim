#sg
'''
Demo to show use of the engineering Formatter.
'''

import numpy as np
from pylab import *

def plotQ(arr):

    x = np.array([i for i in range(0, len(arr))])
    #ion()
    plot(x, arr)
    show()

