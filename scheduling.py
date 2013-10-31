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
        next_job = 0
        try:
            next_job = customer.jobs.index(1)
        
        except ValueError:
            next_job = -1

        return next_job


    naive = classmethod(naive)
