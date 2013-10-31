#sg
class Customer:

    cust_count = 0 #count of customers, to be used to create cust_id

    def __init__(self, num_jobs, jobs):
        self.cust_id = Customer.cust_count + 1
        Customer.cust_count = Customer.cust_count + 1
        self.num_jobs = num_jobs
        self.jobs = jobs
    
    def print_customer(self):
        print 'Customer id : %d, Jobs : ' % self.cust_id,
        print self.jobs,

