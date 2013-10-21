#sg

from eventtype import EventType
from customer import Customer
from event import Event
import random
from heapq import *

class BasicSimulate:

    current_time = 0
    next_event_time = 0
    ARRIVAL_MEAN = 0.3
    customer_pool = {}
    def __init__(self):
        self.timeline = [] #to be used as a heap or a priority queue
        self.sim_start()
        

    def sim_start(self):

        #decide the time at which the first arrival will happen
        arrival = random.expovariate(self.ARRIVAL_MEAN)
        #create a customer which will arrive first
        cust = self.create_customer()
        #cust.print_customer()
        #Add the customer to pool
        BasicSimulate.customer_pool[cust.cust_id] = cust

        #Now create an event with this customer and add it to the timeline

        event = Event(cust, EventType.ARRIVAL, self.current_time)
        heappush(self.timeline, event)
        



    '''Creates a random customer to be inserted into the pool'''
    def create_customer(self):
        job_arr = [0] * Customer.NUM_JOBS
        while(sum(job_arr) == 0): #atleast 1 job
            for i in range(0, Customer.NUM_JOBS):
                if(int(random.random() * 10) % 2 == 0):
                    job_arr[i] = 1
                else:
                    job_arr[i] = 0
    
        return Customer(job_arr)




if __name__ == '__main__':
    b = BasicSimulate()
