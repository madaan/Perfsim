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

class Simulate:
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
        

        #Whether a customer has to be tracked or not
        self.track_customer = True
        self.track_id = 35
        if(self.track_customer):
            self.cust_tracking_file = open('experience_waitresp_time.txt', 'w')

        self.NUM_SERVER = Simulate.config.NUM_SERVER
        self.NUM_STEPS = Simulate.config.NUM_STEPS
        self.CUSTOMER_POOL_SIZE = Simulate.config.CUSTOMER_POOL_SIZE
        self.SERVER_BUSY = [] #This is required to ensure that a process does not enter the queue if there is no one else in the system
        self.server = []
        for i in range(0, self.NUM_SERVER):
            #self.server.append(Queue(0)) #infinite queue
            #self.SERVER_BUSY.append(False)

            fatigue_cap = random.random() * 10;
            break_time = random.random() * 10;
            self.server.append(Server(fatigue_cap, break_time))

        #Set true if you want to see tons of output
        self.verbose = False
        
        #Set false if you want the screen to hold
        self.do_wait = False
        self.response_time_list = []
        self.waiting_time_list = []
        self.overall_waiting_time = []
        self.MIN_JOBS = 11
        self.step = 0
        self.total_jobs_finished = []
        self.sim_start()
        self.timeline_processor()
        
    def sim_start(self):
        '''Initialize the system when no process is there'''
        #create a customer which will arrive first
        cust = self.create_customer()

        #Now create an event with this customer
        if(cust != None):
            self.create_arrival_event(self.current_time, cust)
        

    def timeline_processor(self):
        '''The function which pulls out events from the timeline and processes them'''

        import time
        import os
        step = 0
        while(len(self.timeline) > 0 and self.step < self.NUM_STEPS): 

            self.step = self.step + 1
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
        for ss in self.total_jobs_finished:
            print ss[0], ss[1]
        self.dump_stats()

    def dump_stats(self):
        TRANSIENT = 1000
        print len(self.overall_waiting_time), len(self.response_time_list)
        print 'Throughput : ',  1.0 * (len(self.waiting_time_list[TRANSIENT:]) / self.current_time)
        print 'Average waiting time : ', 1.0 * sum(self.overall_waiting_time[TRANSIENT:]) / len(self.overall_waiting_time[TRANSIENT:])
        print 'Average waiting time (Per queue): ', 1.0 * sum(self.waiting_time_list[TRANSIENT:]) / len(self.waiting_time_list[TRANSIENT:])
        print 'Average response time : ', 1.0 * sum(self.response_time_list[TRANSIENT:]) / len(self.response_time_list[TRANSIENT:])
        len_dist = open('qlen_dist', 'w')
        for i,server in enumerate(self.server):
            len_dist.write('Server : %d\n' % (i))
            server.printQlog(len_dist)

    def handle_arrival(self, arrive_event):
        '''Handles the arrival event'''

                       #Schedule another arrival

        #Create the customer that will arrive next
        next_cust = self.create_customer() #random customer

        if(next_cust != None):
            self.create_arrival_event(self.current_time, next_cust)
        #----------------------------------------------------------------
			#Process current arrival
        #Get the customer related to the event
        cust = arrive_event.customer
        #Need to update the first arrival time if required
        if(cust.first_entry_time == -1): #First entry in the system
            if(cust.cust_id == self.track_id and self.track_customer):    
                self.cust_tracking_file.write('%d entered at %f, expr : %f\n' % (cust.cust_id, self.current_time, cust.expr))
                self.cust_tracking_file.write(str(cust.jobs) +'\n' )
            cust.last_served_time = self.current_time
            cust.first_entry_time = self.current_time

        #note the arrival time for this customer for waiting time calculation
        cust.arrival_time = self.current_time

        #Add the customer to the customer pool
        self.customer_pool[cust.cust_id] = cust

        
        #If a job has arrived here, there must be some job pending
        job_requested = self.get_next_job(cust)
        if(self.server[job_requested].SERVER_BUSY):
            self.server[job_requested].quelenlog(self.current_time)
            self.add_to_queue(self.server[job_requested].Q, job_requested, cust)

        else: #No need to add to queue, but should mark the server as busy
            if(cust.cust_id == self.track_id and self.track_customer):    
                self.cust_tracking_file.write('started service at %d at %f\n' % (job_requested, self.current_time))
            self.server[job_requested].SERVER_BUSY = True
            #since the server is not busy, it will immediately start processing the event
            #zero should be added to calculate the right average
            cust.finish_time = self.current_time
            self.waiting_time_list.append(cust.finish_time - cust.arrival_time) #i.e. 0
            self.create_finish_event(self.current_time, EventType.type_from_num(job_requested), cust) 

    def add_to_queue(self, Q, job_requested, cust):
        '''Add customer to given service queue'''

        '''
        print '\tEntering the queue'
        print 'Customer : ', cust.cust_id
        print 'Arrival Time : ', cust.arrival_time
        '''
        Q.put(cust)
        if(cust.cust_id == self.track_id and self.track_customer):    
            self.cust_tracking_file.write('Entered queue %d at %f\n' % (job_requested, self.current_time))
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
        if(cust.cust_id == self.track_id and self.track_customer):    
            self.cust_tracking_file.write('Finished service at %d at %f\n' % (qno, self.current_time))
        
        if(sum(cust.jobs) > 0): 
            #not yet done, need to find the next pending job
            next_job = self.get_next_job(cust)
            if(self.server[next_job].SERVER_BUSY):
                cust.arrival_time = self.current_time
                self.add_to_queue(self.server[next_job].Q, next_job, cust)
            else:
                self.server[next_job].SERVER_BUSY = True
                if(cust.cust_id == self.track_id and self.track_customer):    
                    self.cust_tracking_file.write('started service at %d at %f\n' % (next_job, self.current_time))
                self.create_finish_event(self.current_time, EventType.type_from_num(next_job), cust) 

        else:
            #Need to update the final finish time of the customer
            if(cust.cust_id == self.track_id and self.track_customer):
                self.cust_tracking_file.write('%d exited at %f, expr : %f\n' % (cust.cust_id, self.current_time, cust.expr))
                self.cust_tracking_file.write('%f %f %f %f\n' % (self.current_time, cust.expr, cust.waiting_time, (self.current_time - cust.first_entry_time)))
            self.overall_waiting_time.append(cust.waiting_time)
            self.response_time_list.append(self.current_time - cust.first_entry_time)
            cust.final_exit_time = -1


        #Done handling the current customer

        #The following code handles the customer which is now at the head of the queue
        if(Q.qsize() >= 1): 
            #need to schedule a departure
            #get the next customer
            next_customer = Q.queue[0]
            
            #find out the next job that has to be performed
            next_job = qno

            #Also calculate the waiting time for this customer and add it ot the waiting_time list

            next_customer.waiting_time = self.current_time - next_customer.arrival_time + next_customer.waiting_time
            
            

            self.waiting_time_list.append(self.current_time - next_customer.arrival_time)
            self.create_finish_event(self.current_time, EventType.type_from_num(next_job), next_customer)

            #log the queue length before changing it
            self.server[qno].quelenlog(self.current_time)
            #Now remove it from the queue and send it to service
            self.remove_from_queue(Q, qno)

            
        #QSize already 0? Can finish here
        if(Q.qsize() == 0):  #need to schedule an arrival and dept
            self.server[qno].SERVER_BUSY = False
            #print 'Queue Empty'
            if(len(self.timeline) == 0): #There is no event
                self.sim_start()



    def remove_from_queue(self, Q, qno):

        '''Removes the top most executing process from the queue. Also schedules the next departure'''
       
        if(Q.qsize() > 0):
            next_customer  = Q.get()
            if(next_customer.cust_id == self.track_id and self.track_customer):    
                self.cust_tracking_file.write('started service at %d at %f\n' % (qno, self.current_time))
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


       #First of all, see if the total time for which the customer has been in the 
       #system exceeds 
        if((self.current_time - customer.first_entry_time) > customer.timeout):
            #need to go out
            if(customer.cust_id == self.track_id and self.track_customer):
                print 'timeout : %f, spent : %f' % (customer.timeout, self.current_time - customer.first_entry_time)
                print 'Timeout : ', customer.expr, self.NUM_SERVER - sum(customer.jobs)
                self.total_jobs_finished.append((customer.expr, self.NUM_SERVER - sum(customer.jobs)))

            service_finish_time = self.current_time #the person leaves, finishes right now
            customer.jobs = [0 for i in range(0, len(customer.jobs))]
            customer.final_exit_time = -1

        else:
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
        
        #return Scheduler.smallest_slowest_queue_next(customer, self.server, self.config)
        #return Scheduler.smallest_fastest_queue_next(customer, self.server, self.config)
        #return Scheduler.smallest_queue_next(customer, self.server)
        return Scheduler.naive(customer)
        #return Scheduler.experience_counts(customer, self.server, self.config)

    def get_interrupt_time(self, serving_server): #Talk of variable names
        '''This returns the time for which a customer might have to wait due to servers taking interrupts (A phone call, a cup of tea and the likes)''' 
        #Everytime the server reaches its fatigue limit, it takes break
        if(serving_server.served % serving_server.fatigue_cap == 0):
            return serving_server.break_time
        else:
            return 0


    def sum_qlens(self):
        total = 0
        for s in self.server:
            total = total + s.Q.qsize()
        return total

    def create_customer(self):

        '''Creates a random customer to be inserted into the pool'''
        import random

        if(Customer.cust_count > self.CUSTOMER_POOL_SIZE):
            #need to pick a customer from the pool only
            # 1.Randomly get an index for the customer to be entered
            num_tries = 10 #else no one is ready yet
            selection = random.randrange(1, self.CUSTOMER_POOL_SIZE, 1)
            

            '''
            if(self.track_customer):
                tracked = self.customer_pool[self.track_id]

                if(tracked.first_entry_time == -1 and tracked.patience < self.sum_qlens()):
                    for i in range(0, self.NUM_SERVER):
                        tracked.jobs[i] = 1
                    tracked.expr = tracked.expr + random.random() / 1000
                    tracked.first_entry_time = -1
                    tracked.final_exit_time = -1
                    tracked.waiting_time = 0
                    return tracked
            '''
            cust= self.customer_pool[selection]
            still_in_system = (cust.first_entry_time != -1)
            not_enough_patience = (self.sum_qlens() > cust.patience)
            
            
            while((still_in_system or not_enough_patience) and num_tries > 0):
                selection = random.randrange(1, self.CUSTOMER_POOL_SIZE, 1)
                cust = self.customer_pool[selection]
                still_in_system = (cust.final_exit_time != -1)
                not_enough_patience = (self.sum_qlens() > cust.patience)
                num_tries = num_tries - 1

                
            if(num_tries == 0):
                return None #no one is available

            while(sum(cust.jobs) < self.MIN_JOBS): #loop till the new customer has atleast 1 job
                for i in range(0, self.NUM_SERVER):
                    if(random.random() > 0.5):
                        cust.jobs[i] = 1
                    else:
                        cust.jobs[i] = 0

            #log for debugging
            #self.cust_log(cust)

            #increase the experience by ?
            if(cust.cust_id == self.track_id and self.track_customer and self.step < 2000):  #Remove transient
                cust.expr = cust.expr #forgive me.
            else:
                cust.expr = cust.expr + random.random() / 10
            
            #update the times
            cust.first_entry_time = -1
            cust.final_exit_time = -1
            cust.waiting_time = 0
            return cust
            

        job_arr = [0] * self.NUM_SERVER
        while(sum(job_arr) < self.MIN_JOBS): #loop till the new customer has atleast 1 job
            for i in range(0, self.NUM_SERVER):
                if(random.random() > 0.5):
                    job_arr[i] = 1
                else:
                    job_arr[i] = 0

        cust  = Customer(job_arr)
        self.customer_pool[cust.cust_id] = cust
        return cust


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


    def print_customer_pool(self):
        '''prints customer pool'''
        for cust_id in self.customer_pool.keys():
            self.customer_pool[cust_id].print_customer()


    def cust_log(self, cust):
        '''logs customer information to stdout'''
        print 'id : %d, expr : %f, entered : %f, exited : %f,  waiting time : %f' % (cust.cust_id, cust.expr, cust.first_entry_time, cust.final_exit_time, cust.waiting_time)


if __name__ == '__main__':
    b = Simulate()
