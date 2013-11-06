#sg
from eventtype import EventType
from customer import Customer
from event import Event
import random
from heapq import *
from Queue import *
#import matplotlib.pyplot as plt
import numpy as np
from scheduling import Scheduler
from configuration import Config
from stats import Stats
from server import Server
#TODO : Find next job for the customer should be a function

class BasicSimulate:

    current_time = 0
    next_event_time = 0
    #No new customers will be created once this limit is reached
    #A customer will be picked up from the existing pool with slightly more 
    #experience
    config = Config('perfsim.config')
    def __init__(self):
        '''The constructor'''

        self.num_cust = 0
        self.customer_pool = {}  #should be a class variable, saving typing
        self.timeline = []  #to be used as a heap or a priority queue
        
        self.NUM_SERVER = BasicSimulate.config.NUM_SERVER
        self.NUM_STEPS = BasicSimulate.config.NUM_STEPS
        self.CUSTOMER_POOL_SIZE = BasicSimulate.config.CUSTOMER_POOL_SIZE
        self.SERVER_BUSY = [] #This is required to ensure that a process does not enter the queue if there is no one else in the system
        self.server = []
        for i in range(0, self.NUM_SERVER):
            #self.server.append(Queue(0)) #infinite queue
            #self.SERVER_BUSY.append(False)
            self.server.append(Server(10, .4))

        self.verbose = False
        self.do_wait = False
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
        '''The function which pulls out events from the timeline and processes them'''

        import time
        import os
        step = 0
        while(len(self.timeline) > 0 and step < self.NUM_STEPS): 

            step = step + 1
            if(self.verbose):
                print 'Finished : ', step
                os.system('clear')
                self.print_timeline()
            (self.current_time, next_event) = heappop(self.timeline)
            if(self.verbose):
                print '\nTime  : %f \n' % self.current_time
                print 'Event : ', self.current_time, EventType.name(next_event.event_type)
            if(next_event.event_type == EventType.ARRIVAL):
                if(self.verbose):
                    print 'After Processing Arrival :\n'
                self.handle_arrival(next_event)
				
				
            else : #elif(next_event.event_type == EventType.SERVICE_FINISH_1)
                if(self.verbose):
                    print 'After Processing Service finish :\n'
                self.handle_service_finish(next_event)
            if(self.verbose):
                self.printQ()
                self.print_timeline() 
            #log_file.write('%d\n' % (self.server.qsize()))
            #raw_input('\n\n\n[ENTER] to continue')
            if(self.do_wait):
                time.sleep(1)
        #self.print_customer_pool()
        print 'Average waiting time : ', Stats.average_waiting_time(self.customer_pool)
        print 'Average response time : ', Stats.average_response_time(self.customer_pool) 
        print 'Throughtput : ', Stats.throughput(self.customer_pool, 0, self.current_time) 
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
        
        #Need to update the first arrival time if required
        if(cust.first_entry_time == -1): #First entry in the system
            cust.first_entry_time = self.current_time

        #Add the customer to the customer pool
        self.customer_pool[cust.cust_id] = cust

        
        #If a job has arrived here, there must be some job pending
        job_requested = self.get_next_job(cust)

        if(self.server[job_requested].SERVER_BUSY): 
            self.add_to_queue(self.server[job_requested].Q, cust)
        else: #No need to add to queue, but should mark the server as busy
            self.server[job_requested].SERVER_BUSY = True
            #since the server is not busy, it will immediately start processing the event
            self.create_finish_event(self.current_time, EventType.type_from_num(job_requested), cust) 


    def add_to_queue(self, Q, cust):
        '''Add customer to given service queue'''

        cust.arrival_time = self.current_time
        '''
        print '\tEntering the queue'
        print 'Customer : ', cust.cust_id
        print 'Arrival Time : ', cust.arrival_time
        '''
        Q.put(cust)
        #A departure cannot be scheduled right now because you don't really know how long you'll have to wait


    def handle_service_finish(self, finish_event):
        '''Handle service finish event'''
        #We now need a way to determine to which queue was the person added
        cust = finish_event.customer
        etype = finish_event.event_type
        #get the queue number which has caused the event
        qno = EventType.queue_from_event(etype); 
        Q = self.server[qno].Q
        #Add 1 to the number of customers served till now
        self.server[qno].served = self.server[qno].served + 1
        #Mark the bit vector of the customer to reflect the change
        cust.jobs[qno] = 0 #1 -> 0, job over
        
        if(sum(cust.jobs) > 0): 
            #not yet done, need to find the next pending job
            next_job = self.get_next_job(cust)
            if(self.server[next_job].SERVER_BUSY):
                self.add_to_queue(self.server[next_job].Q, cust)
            else:
                self.server[next_job].SERVER_BUSY = True
                self.create_finish_event(self.current_time, EventType.type_from_num(next_job), cust) 

        else:
            #Need to update the final finish time of the customer
            cust.final_exit_time = self.current_time

        #Done handling the current customer

        #The following code handles the customer which is now at the head of the queue
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
            self.server[qno].SERVER_BUSY = False
            #print 'Queue Empty'
            if(len(self.timeline) == 0): #There is no event
                self.sim_start()



    def remove_from_queue(self, Q):

        '''Removes the top most executing process from the queue. Also schedules the next departure'''
       
        if(Q.qsize() > 0):
            cust = Q.get()
            cust.finish_time = self.current_time
            cust.waiting_time = cust.waiting_time + \
                                cust.finish_time - cust.arrival_time
        

        '''
        print '\tLeaving the queue'
        print 'Customer : ', cust.cust_id
        print 'Arrival Time : ', cust.arrival_time
        print 'Departure Time : ', cust.finish_time
        print 'waiting time : ', cust.waiting_time
        '''

    def create_arrival_event(self, time_from, customer):

        '''Put an arrival event given the parameters on the timeline and return the event time'''

        next_arrival_time = 0
        #Time of next arrival
        if(self.config.ARRIVAL_DIST == 'E'):
            
            next_arrival_time = random.expovariate(float(self.config.ARRIVAL_DIST_MEAN)) + time_from

        elif(self.config.ARRIVAL_DIST_MEAN == 'D'):
            next_arrival_time = float(self.config.ARRIVAL_DIST_MEAN) + time_from

		#create an event with the next customer and arrival timeline
        event =  Event(customer, EventType.ARRIVAL,next_arrival_time)
        heappush(self.timeline, (next_arrival_time, event))
        return next_arrival_time





    def create_finish_event(self, time_from, etype, customer):

        '''Put a departure event given the parameters on the timeline and return the event time'''
        #Decide finish time based
        # 1. Get the queue
        qno = EventType.queue_from_event(etype)
        
        config_key = 'server_' + str(qno) #get distribution and mean from config
        dist = self.config.server_config[config_key]['service_dist']
        dist_rate = float(self.config.server_config[config_key]['service_dist_rate'])
        
        service_finish_time = 0 
        if(dist == 'E'):
            #Interrupt time is time for which the server is interrupted
            service_finish_time = float(time_from) + random.expovariate(dist_rate) + self.get_interrupt_time(self.server[qno])
        elif(dist == 'D'):
            service_finish_time = float(time_from) + dist_rate + self.get_interrupt_time(self.server[qno])


        #find a job that is yet incomplete

        #raw_input('>')
        event =  Event(customer, etype, service_finish_time)
        heappush(self.timeline, (float(service_finish_time), event))

        return service_finish_time

    def get_next_job(self, customer):
        '''Calls the correct scheduler, passing the customer and the list of queues in the system. The scheduler can be chosen by the customer by specifying in a config file.'''

        if(sum(customer.jobs) == 0): 
            return -1
        return Scheduler.experience_counts(customer, self.server, self.config)

    def get_interrupt_time(self, serving_server): #Talk of variable names
        '''This returns the time for which a customer might have to wait due to servers taking interrupts (A phone call, a cup of tea and the likes)''' 
        #Everytime the server reaches its fatigue limit, it takes break
        if(serving_server.served % serving_server.fatigue_cap == 0):
            return serving_server.break_time
        else:
            return 0








    def printQ(self):
        '''Prints the service queue'''

        for i in range(0, self.NUM_SERVER):
            print 'Queue', i
            Q = self.server[i].Q
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
        import random

        if(Customer.cust_count > self.CUSTOMER_POOL_SIZE):
            #need to pick a customer from the pool only
            # 1.Randomly get an index for the customer to be entered
            selection = random.randrange(1, self.CUSTOMER_POOL_SIZE, 1)
            cust= self.customer_pool[selection]
            
            #log for debugging
            #self.cust_log(cust)

            #increase the experience by ?
            cust.expr = cust.expr + random.random() / 100
            
            #update the times
            cust.first_entry_time = -1
            cust.final_exit_time = -1
            cust.waiting_time = 0
            
            return cust
            

        job_arr = [0] * self.NUM_SERVER
        while(sum(job_arr) != 2): #loop till the new customer has atleast 1 job
            for i in range(0, self.NUM_SERVER):
                if(random.random() > 0.5):
                    job_arr[i] = 1
                else:
                    job_arr[i] = 0

        cust  = Customer(job_arr)
        self.customer_pool[cust.cust_id] = cust
        return cust




    def print_customer_pool(self):
        '''prints customer pool'''
        for cust_id in self.customer_pool.keys():
            self.customer_pool[cust_id].print_customer()


    def cust_log(self, cust):
        '''logs customer information to stdout'''
        print 'id : %d, expr : %f, entered : %f, exited : %f,  waiting time : %f' % (cust.cust_id, cust.expr, cust.first_entry_time, cust.final_exit_time, cust.waiting_time)



if __name__ == '__main__':
    b = BasicSimulate()
