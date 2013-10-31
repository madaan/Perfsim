#sg
'''This file hosts the functions that each take 2 arguments :

    1. Job array of the customer.
    2. Queues of the system (list of queue objects) 

    We don't think such a function would need to know anything else. 
    TODO : Ask ma'am if this indeed is the case

'''

class Scheduler:

    def naive(self, customer, queues):
        '''Simple scheduler. Returns the next pending job, does not considers th           e state of the queue'''
        '''Returns -1 if a customer is done'''
        next_job = 0
        try:
            next_job = customer.jobs.index(1)
        
        except ValueError:
            next_job = -1

        return next_job
    
    def smallest_queue_next(self, customer, queues):
        '''(Relatively) Smarter scheduling strategy. Get to the queue which is the smallest in length. In case of a tie, go to the queue which has a smaller queue number'''

        #Find the lengths of the queue which the customer needs.
        #Set length of other queues to INF so that they don't interfere
        #with calculation of minimum
        INFTY = float("inf")
        lens = [queue.qsize() if customer.jobs[i] == 1 else INFTY for i,queue in enumerate(queues)]
        
        #Now return the queue number of the queue which is the shortest
        return lens.index(min(lens))


    naive = classmethod(naive)
    smallest_queue_next = classmethod(smallest_queue_next)
