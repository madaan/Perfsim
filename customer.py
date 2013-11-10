#sg
import random
class Customer:

    cust_count = 0 #count of customers, to be used to create cust_id

    def __init__(self, jobs):
        '''A unique customer id. Integers starting from 1'''
        self.cust_id = Customer.cust_count + 1
        self.first_entry_time = -1
        self.final_exit_time = -1
        '''
        Experience is between 0 and 1. A customer with high experience
        is likely to know his way around the office and thus experience
        less service time

        The following values are ad-hoc. 
        Ideally we should have gone to the bank for this.
        '''
        mu = .2
        variate = .1
        self.expr = random.normalvariate(mu, variate)
        
        '''
        Patience : Every customer has a level of patience. The customer
        enters the bank, looks at the queue status for the jobs that he has
        to perform, and decides to either enter the bank or leaves at that
        moment. Note that right now, if a customer enters the bank, he performs
        the job with certainity. 
        
        Patience : Right now the cumulative length of queues that a customer can
        handle.

        Massive TODO : Include timeouts.  
        '''
        mu = 20
        variate = 2
        self.patience = random.normalvariate(mu, variate)


    
        Customer.cust_count = Customer.cust_count + 1
        self.jobs = jobs
        self.waiting_time = 0
        self.arrival_time = 0
        self.finish_time = float("inf")    
    
    def print_customer(self):
        print 'Customer id : %d, First entry  : %f, Final exit : %f' % (self.cust_id, self.first_entry_time, self.final_exit_time)
        #print self.jobs,

