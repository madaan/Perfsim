#sg
'''This file hosts the functions that each take 2 arguments :

    1. Job array of the customer.
    2. Queues of the system (list of queue objects) 

    We don't think such a function would need to know anything else. 
    TODO : Ask ma'am if this indeed is the case

'''

class Scheduler:

    def naive(self, customer):
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


    def smallest_fastest_queue_next(self, customer, queues, config):

        '''
        Considers both the length of the queue and the service rate.
        Criteria ->
            Goodness of a server = 1 / (service_rate + len)
        '''
        INFTY = float('inf')
        lens = [queue.qsize() if customer.jobs[i] == 1 else INFTY for i,queue in enumerate(queues)]

        rate = [0] * len(customer.jobs)
        for i in range(0, len(customer.jobs)):
            if(customer.jobs[i] == 1):
                config_key = 'server_' + str(i)
                dist_rate = float(config.server_config[config_key]['service_dist_rate'])
                rate[i] = dist_rate
                
            else:
                rate[i] = INFTY

        goodness = [(1.0 / (rate[i] + lens[i])) for i in range(0, len(customer.jobs))]

        return goodness.index(max(goodness))


     
    def experience_counts(self, customer, queues, config):

        '''
        This is not a scheduling algorithm in itself, but is rather a filter.
        Experience of a customer is seen as a threshold for selecting various
        scheduling disciplines.
        It is hypothized that a customer that is well experienced will have some
        handle on how fast a server is, and thus will use the smallest_fastest_next
        algorithm. A user with average experience will choose the smallest_queue_next
        algorithm. The most inexperienced of the users will naively do the task 1
        after another
        '''
        SMALLEST_FASTEST_THRESHOLD = 0.75
        SMALLEST_THRESHOLD = 0.5

        if(customer.expr >= SMALLEST_FASTEST_THRESHOLD):
            return self.smallest_fastest_queue_next(customer, queues, config)

        elif(customer.expr >= SMALLEST_THRESHOLD):
            return self.smallest_queue_next(customer, queues)

        else:
            return self.naive(customer)




    naive = classmethod(naive)
    smallest_queue_next = classmethod(smallest_queue_next)
    smallest_fastest_queue_next = classmethod(smallest_fastest_queue_next)
    experience_counts = classmethod(experience_counts)
            
