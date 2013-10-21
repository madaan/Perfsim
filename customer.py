#sg
class Customer:

    cust_count = 0 #count of customers, to be used to create cust_id
    NUM_JOBS = 3 #Total number of different jobs a customer might have to perform in the bank

    def __init__(self, jobs):
        self.cust_id = cust_count + 1
        cust_count = cust_count + 1
        self.jobs = jobs
    
    def print_customer(self):
        print 'Customer id : %d, Jobs : ' % self.cust_id
        print self.jobs

