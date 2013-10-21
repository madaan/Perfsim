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

    def __init__(self):

        self.customer_pool = {} #should be a class variable, saving typing
        self.timeline = [] #to be used as a heap or a priority queue
        self.sim_start()
        self.timeline_processor()
        

    def sim_start(self):

        #decide the time at which the first arrival will happen
        first_arrival_time = random.expovariate(self.ARRIVAL_MEAN)
        #create a customer which will arrive first
        cust = self.create_customer()
        #cust.print_customer()
        #Add the customer to pool
        self.customer_pool[cust.cust_id] = cust

        #Now create an event with this customer and add it to the timeline

        event = Event(cust, EventType.ARRIVAL, first_arrival_time)
        heappush(self.timeline, (self.current_time, event))
        #Inserting tuple at the moment
        



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

    def timeline_processor(self):
        '''the function which pulls out events from the timeline and
        processes them'''

        while(len(self.timeline) > 0):
            print self.current_time
            self.current_time, next_event = heappop(self.timeline)
            next_event.event_details()






if __name__ == '__main__':
    b = BasicSimulate()
