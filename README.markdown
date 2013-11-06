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

##License 
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
    

##Simulator for a server with load dependent service rate and dynamic queue joining probabilities

Imple notes :

1. timeline is a heap which stores event tuples.
2. event tuple : (timestamp, event object)

Scheduling departure : 

The departure will be scheduled either during adding if the process being added is the only process. Otherwise, a departure will be scheduled every time there is a departure. A departure is also scheduled if the queue is empty and there is an arrival to happen.

TODO :
1. The scheduling algorithm should be included as an option in the config file.
2. Need to model interrupts while servicing.
