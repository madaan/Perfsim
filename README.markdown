##Simulator for a server with load dependent service rate and dynamic queue joining probabilities

 ### The following data structures will be maintained :
    --Timeline : The event list. A priority queue which will have the events indexed by the timestamp of occurrence.
    
    --Customer pool : A hash table that stores the customers entering the system. 

   --Queues : The priority queues that will simulate the actual service queues.


 ### Classes 
    Event : Storing event type and customer with which the event is related.
    
    Customer
    
    
 
Imple notes :

1. timeline is a heap which stores event tuples.
2. event tuple : (timestamp, event object)

Scheduling departure : 

The departure will be scheduled either during adding if the process being added is the only process. Otherwise, a departure will be scheduled every time there is a departure. A departure is also scheduled if the queue is empty and there is an arrival to happen.
