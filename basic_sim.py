#sg

import event
import customer
import random

class BasicSimulate:

    time = 0
    next_event_time = 0
    ARRIVAL_MEAN = 0.3
    def __init__(self):
        self.Timeline = [] #to be used as a heap or a priority queue
        sim_start()
        

    def sim_start():

        #decide the time at which the first arrival will happen
        arrival = random.expovariate(ARRIVAL_MEAN)
        #create a customer which will arrive first
        cust = create_customer()
        cust.print_customer
        



    '''Creates a random customer to be inserted into the pool'''
    def create_customer():
        job_arr = [None] * Customer.NUM_JOBS
        for i in range(0, Customer.NUM_JOBS):
            if((random.random() * 10) % 2 == 0):
                job_arr[i] = 1
            else:
                job_arr[i] = 0

       return Customer(job_arr)




if __name__ == '__main__':
    b = BasicSimulate()
