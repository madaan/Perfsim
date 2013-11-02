#sg
import random
class Customer:

    cust_count = 0 #count of customers, to be used to create cust_id

    def __init__(self, jobs):
        '''A unique customer id. Integers starting from 1'''
        self.cust_id = Customer.cust_count + 1

        '''
        Experience is between 0 and 1. A customer with high experience
        is likely to know his way around the office and thus experience
        less service time

        The following values are ad-hoc. 
        Ideally we should have gone to the bank for this.
        '''
        mu = .5
        variate = .1

        self.expr = random.normalvariate(mu, variate)

        Customer.cust_count = Customer.cust_count + 1
        self.jobs = jobs
        self.wait = 0
        self.arrival_time = 0
        self.finish_time = float("inf")    
    
    def print_customer(self):
        print 'Customer id : %d, Jobs : ' % self.cust_id,
        print self.jobs,

