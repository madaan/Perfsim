##The simulator now has the following features :
1. Any number of servers be specified.
2. Distribution for servers can be specified.
3. Customers are picked from a user pool which grows only till a user specified
limit. 
4. Users have an experience which keeps on increasing as they visit the bank.
5. The servers have a fatigue cap after which they stand up to take a break.
6. Several scheduling algorithms are implemented in scheduler.py
7. Most of the options can be specified in the config file which is parsed befor
8. Essential statistics are being calculated.
9. Simple plotting is being done.
10. Lots of attention is paid to the design of the simulator.
##Simulator for a server with load dependent service rate and dynamic queue joining probabilities

Imple notes :

1. timeline is a heap which stores event tuples.
2. event tuple : (timestamp, event object)

Scheduling departure : 

The departure will be scheduled either during adding if the process being added is the only process. Otherwise, a departure will be scheduled every time there is a departure. A departure is also scheduled if the queue is empty and there is an arrival to happen.

TODO :
1. The scheduling algorithm should be included as an option in the config file.
2. Need to model interrupts while servicing.
