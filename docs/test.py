#sg
import random
sum = 0
for i in range(0, 1000):
    sum = sum +  random.expovariate(0.3)

print (1.0 * sum) / 1000


