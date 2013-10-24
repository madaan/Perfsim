#sg
from eventtype import EventType
from customer import Customer
from event import Event
import random
from heapq import *
from Queue import *


class BasicSimulate:

    current_time = 0
    next_event_time = 0
    ARRIVAL_RATE = 0.01
    SERVICE_RATE = 0.2

    def __init__(self):

        self.customer_pool = {}  #should be a class variable, saving typing
        self.timeline = []  #to be used as a heap or a priority queue
        
        self.service_queue = Queue(0)  #infinite queue
        self.sim_start()
        self.timeline_processor()

    def sim_start(self):

        #decide the time at which the first arrival will happen
        first_arrival_time = self.current_time + random.expovariate(self.ARRIVAL_RATE)
        first_service_time = first_arrival_time + random.expovariate(self.SERVICE_RATE)
        #create a customer which will arrive first
        cust = self.create_customer()
        #cust.print_customer()
        #Add the customer to pool

        #Now create an event with this customer and add it to the timeline

        event = Event(cust, EventType.ARRIVAL, first_arrival_time)
        heappush(self.timeline, (first_arrival_time, event))

        event = Event(cust, EventType.SERVICE_FINISH, first_service_time)
        heappush(self.timeline, (first_service_time, event))
        #Inserting tuple at the moment


    def create_customer(self):
    
        '''Creates a random customer to be inserted into the pool'''
        job_arr = [0] * Customer.NUM_JOBS
        while(sum(job_arr) == 0): #atleast 1 job
            for i in range(0, Customer.NUM_JOBS):
                if(int(random.random() * 10) % 2 == 0):
                    job_arr[i] = 1
                else:
                    job_arr[i] = 0
    
        return Customer(job_arr)

    def print_timeline(self):
        print
        for (time,event) in self.timeline:
            print '(%f, %s) -> ' % (time, EventType.name(event.event_type)),
        print 'X'
            
    
    def timeline_processor(self):
    
        log_file = open('log', 'wb')
        '''the function which pulls out events from the timeline and
        processes them'''

        step = 0
        while(len(self.timeline) > 0 and step < 10000): 
            
            step = step + 1
            import os
            os.system('clear')
            
            self.print_timeline()
            (self.current_time, next_event) = heappop(self.timeline)
            print '\nTime  : %f \n' % self.current_time
            #print 'Event : ', self.current_time, EventType.name(next_event.event_type)
            print
            if(next_event.event_type == EventType.ARRIVAL):
                print 'Processing Arrival'
                self.handle_arrival(next_event)

            elif(next_event.event_type == EventType.SERVICE_FINISH):
                print 'Processing Service finish'
                self.handle_service_finish(next_event)
    
            #self.printQ()
            log_file.write('%d\n' % (self.service_queue.qsize()))
            #raw_input('\n\n\n[ENTER] to continue')

        log_file.close()
            
    
    def handle_arrival(self, arrive_event):
    
                       #Schedule another arrival

        #Time of next arrival
        next_arrival_time = random.expovariate(self.ARRIVAL_RATE) + self.current_time;
        
        #Create the customer that will arrive next
        next_cust = self.create_customer()

        #create an event with the next customer and arrival time
        event = Event(next_cust, EventType.ARRIVAL,next_arrival_time)
        
        #Push the event to the time line
        heappush(self.timeline, (next_arrival_time, event))

        #----------------------------------------------------------------
                    #Process current arrival

        #Get the customer related to the event
        cust = arrive_event.cust
        
        #Add the customer to the customer pool
        self.customer_pool[cust.cust_id] = cust
        
        #TODO : Add this customer to one of the queues
        #For now, add this customer to the only service queue that is present
        self.add_to_queue(self.service_queue, cust)
            
    def add_to_queue(self, Q, cust):

        '''Adds the customer to the specified Q'''
        Q.put(cust)
        '''
        if(Q.qsize() == 1):
            #We also need to schedule a departure now, becuase the waiting time of this process 
            #will be zero. Otherwise, the deaparture will be scheduled when a process is removed
            service_finish_time = self.current_time + random.expovariate(self.SERVICE_RATE)
            event = Event(cust, EventType.SERVICE_FINISH, service_finish_time)
            heappush(self.timeline, (service_finish_time, event))
        '''

#A departure cannot be scheduled right now because you don't really know how long 
        #you'll have to wait

    def printQ(self):
        
        print
        for ele in self.service_queue.queue:
            print '||  ',ele.cust_id,'  || -> ',
        print 'X'
    def handle_service_finish(self, finish_event):

        self.remove_from_queue(self.service_queue, finish_event.cust)

    #not directly using self.service_queue in this method because this could have been any queue
    def remove_from_queue(self, Q, cust):

        '''removes the top most executing process from the queue. Also
        schedules the next departure'''

        Q.get()

        if(Q.qsize() >= 1): #need to schedule a departure
            #get the next customer
            next_customer = Q.queue[0]
            
            service_finish_time = self.current_time + random.expovariate(self.SERVICE_RATE)
            event = Event(next_customer, EventType.SERVICE_FINISH, service_finish_time)
            heappush(self.timeline, (service_finish_time, event))

        if(Q.qsize() == 0):  #need to schedule an arrival and dept
            print 'Queue Empty'
            self.sim_start()

        


if __name__ == '__main__':
    b = BasicSimulate()
