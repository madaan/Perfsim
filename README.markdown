#Simulator for a system which has servers with load dependent service rates and customers with dynamic queue joining probabilities. 

###In simpler terms, we are trying to model the situation at places where public dealing is involved.

##The simulator now has the following features :
    1. Any number of servers be specified.
	2. Distribution for servers can be specified.
	3. Customers are picked from a user pool which grows only till a user specified
	limit. 
	4. Users have an experience which keeps on increasing as they visit the bank.
	5. The servers have a fatigue cap after which they stand up to take a break.
	6. Several scheduling algorithms are implemented in scheduler.py
	7. Most of the options can be specified in the config file which is parsed before
	starting the simulation.
	8. Essential statistics are being calculated.
	9. Simple plotting is being done.
	10. Lots of attention is paid to the design of the simulator.
    11. Every customer has a level of patience. The user enters the system and if the
    total number of users in the system exceed the patience level, the user does not join.


##How are we modelling interrupts?

1. Interrupts occur frequently in public offices. We model these by noting that an interrupt simply means that the service time of a user is more than it should have been. Thus, we if an interrupt occurs, the service finished event for that particular customer is delayed by some amount.

2. This is being done right now by counting the number of users served by a server. A server takes a (random) break everytime it has served a fixed number of users.
We call this number fatigue cap of the server.

##Writing a configuration file

### A) Distributions

    *D : Deterministic
    Rate : Actually the time interval that elapses between events. Eg service rate = 5 means that the server takes 5 units of time to serve a customer.

    *E : Exponential
    Rate : Inverse of the mean.

### B) Scheduling
Refer to Scheduler.py for details.

    0 : Naive : Naive scheduler
    1. SQN : Shortest queue next
    2. SFQN : Shortest fastest queue next
    3. OBS : Order based scheduling 
    4. EC : Experience counts


###More information can be found in docs/
###[Why](http://www.quora.com/Python-programming-language-1/What-are-some-cool-Python-tricks) [python?](http://xkcd.com/353/)
##License (Current)
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    


Imple notes :

1. timeline is a heap which stores event tuples.
2. event tuple : (timestamp, event object)

Scheduling departure : 

The departure will be scheduled either during adding if the process being added is the only process. Otherwise, a departure will be scheduled every time there is a departure. A departure is also scheduled if the queue is empty and there is an arrival to happen.

TODO :
1. The scheduling algorithm should be included as an option in the config file.
2. Need to model interrupts while servicing.
