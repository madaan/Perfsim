#sg
from eventtype import EventType
from customer import Customer
from event import Event
import random
from heapq import *
from Queue import *
#import matplotlib.pyplot as plt
import numpy as np

#TODO : Find next job for the customer should be a function

class BasicSimulate:

    current_time = 0
    next_event_time = 0
    ARRIVAL_RATE = .40      #lambda
    SERVICE_RATE = .50        #mu
    NUM_QUEUES = 115

    def __init__(self):
        '''The constructor'''
        self.customer_pool = {}  #should be a class variable, saving typing
        self.timeline = []  #to be used as a heap or a priority queue
        

        self.SERVER_BUSY = [] #This is required to ensure that a process does not enter the queue if there is no one else in the system
        self.service_queue = []
        for i in range(0, self.NUM_QUEUES):
            self.service_queue.append(Queue(0)) #infinite queue
            self.SERVER_BUSY.append(False)

        self.sim_start()
        self.timeline_processor()
        
    def sim_start(self):
        '''Initialize the system when no process is there'''
        #create a customer which will arrive first
        cust = self.create_customer()

        #Now create an event with this customer
        self.create_arrival_event(self.current_time, cust)
        
        #get the job which he will first need to finish
        #next_job = self.get_next_job(cust)

        #self.create_finish_event(atime + self.current_time, EventType.type_from_num(next_job), cust)
        #heappush(self.timelinec, (first_service_time, event))
        #Inserting tuple at the moment


    def timeline_processor(self):
        '''Te function which pulls out events from the timeline and processes them'''

        step = 0
        while(len(self.timeline) > 0 and step < 2500): 

            step = step + 1
            print 'Finished : ', step
            import os
            os.system('clear')

            self.print_timeline()
            (self.current_time, next_event) = heappop(self.timeline)
            print '\nTime  : %f \n' % self.current_time
            print 'Event : ', self.current_time, EventType.name(next_event.event_type)
            print
            if(next_event.event_type == EventType.ARRIVAL):
                print 'After Processing Arrival :\n'
                self.handle_arrival(next_event)
				
				
            else : #elif(next_event.event_type == EventType.SERVICE_FINISH_1)
                print 'After Processing Service finish :\n'
                self.handle_service_finish(next_event)
            self.printQ()
            self.print_timeline() 
            #log_file.write('%d\n' % (self.service_queue.qsize()))
            #raw_input('\n\n\n[ENTER] to continue')
            import time
            time.sleep(.15)

    def handle_arrival(self, arrive_event):
        '''Handles the arrival event'''

                       #Schedule another arrival

        #Create the customer that will arrive next
        next_cust = self.create_customer() #random customer

        self.create_arrival_event(self.current_time, next_cust)

        #----------------------------------------------------------------
			#Process current arrival

        #Get the customer related to the event
        cust = arrive_event.customer

        #Add the customer to the customer pool
        self.customer_pool[cust.cust_id] = cust

        
        #If a job has arrived here, there must be some job pending
        job_requested = self.get_next_job(cust)

        if(self.SERVER_BUSY[job_requested]): 
            self.add_to_queue(self.service_queue[job_requested], cust)
        else: #No need to add to queue, but should mark the server as busy
            self.SERVER_BUSY[job_requested] = True
            #since the server is not busy, it will immediately start processing the event
            self.create_finish_event(self.current_time, EventType.type_from_num(job_requested), cust) 


    def add_to_queue(self, Q, cust):
        '''Add customer to given service queue'''

        Q.put(cust)
        #A departure cannot be scheduled right now because you don't really know how long you'll have to wait


    def handle_service_finish(self, finish_event):
        '''Handle service finish event'''

        #We now need a way to determine to which queue was the person added
        
        cust = finish_event.customer

        etype = finish_event.event_type

        qno = EventType.queue_from_event(etype); 
        #returns the queue number which has caused the event

        Q = self.service_queue[qno]


        #Mark the bit vector of the customer to reflect the change

        cust.jobs[qno] = 0
        
        if(sum(cust.jobs) > 0): 
            #not yet done, need to find the next pending job
            next_job = self.get_next_job(cust)
            if(self.SERVER_BUSY[next_job]):
                self.add_to_queue(self.service_queue[next_job], cust)
            else:
                self.SERVER_BUSY[next_job] = True
                self.create_finish_event(self.current_time, EventType.type_from_num(next_job), cust) 

        else:
            pass
            #nothing to do, the customer is done with all the jobs.

        #Done handling the current customer
        #The following code handles the customer which is now at the head of hte queue
        if(Q.qsize() >= 1): 
            #need to schedule a departure
            #get the next customer
            next_customer = Q.queue[0]
            #find out the next job that has to be performed
            next_job = qno

            self.create_finish_event(self.current_time, EventType.type_from_num(next_job), next_customer)

            #Now remove it from the queue and send it to service
            self.remove_from_queue(Q)

        #QSize already 0? Can finish here
        if(Q.qsize() == 0):  #need to schedule an arrival and dept
            self.SERVER_BUSY[qno] = False
            #print 'Queue Empty'
            if(len(self.timeline) == 0): #There is no event
                self.sim_start()


    def remove_from_queue(self, Q):

        '''Removes the top most executing process from the queue. Also schedules the next departure'''
       
        if(Q.qsize() > 0):
            Q.get()

    def create_arrival_event(self, time_from, customer):
        '''Put an arrival event given the parameters on the timeline and return the event time'''

        #Time of next arrival
        next_arrival_time = random.expovariate(self.ARRIVAL_RATE) + time_from;


		#create an event with the next customer and arrival timeline
        event =  Event(customer, EventType.ARRIVAL,next_arrival_time)
        heappush(self.timeline, (next_arrival_time, event))
        return next_arrival_time

    def create_finish_event(self, time_from, etype, customer):

        '''Put a departure event given the parameters on the timeline and return the event time'''
        service_finish_time = float(time_from) + random.expovariate(self.SERVICE_RATE)
        #find a job that is yet incomplete

        #raw_input('>')
        event =  Event(customer, etype, service_finish_time)
        heappush(self.timeline, (float(service_finish_time), event))

        return service_finish_time

    def get_next_job(self, customer):
        '''Returns the next queue that a customer should join'''
        '''Returns -1 if a customer is done'''

        next_job = 0
        try:
            next_job = customer.jobs.index(1)
        
        except ValueError:
            next_job = -1

        return next_job

        #Later, the complex scheduling poilicies may be entered here

    def printQ(self):
        '''Prints the service queue'''

        for i in range(0, self.NUM_QUEUES):
            print 'Queue', i
            Q = self.service_queue[i]
            print
            for ele in Q.queue:
                print '|| ',ele.cust_id,'(', ele.jobs, ') || <- ',
            print 'X'


    def print_timeline(self):
        '''A function to print the timeline'''
        print
        for (time,event) in self.timeline:
            print '(%f, %d, %s, %s) <- ' % (time, event.customer.cust_id, EventType.name(event.event_type), ' '.join(str(event.customer.jobs))),
        print 'X'


    def create_customer(self):

        '''Creates a random customer to be inserted into the pool'''
        job_arr = [0] * self.NUM_QUEUES
        while(sum(job_arr) == 0): #loop till the new customer has atleast 1 job
            for i in range(0, self.NUM_QUEUES):
                if(random.random() > 0.5):
                    job_arr[i] = 1
                else:
                    job_arr[i] = 0

        return Customer(self.NUM_QUEUES, job_arr)



if __name__ == '__main__':
    b = BasicSimulate()
