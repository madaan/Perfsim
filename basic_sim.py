#sg
from eventtype import EventType
from customer import Customer
from event import Event
import random
from heapq import *
from Queue import *
#import matplotlib.pyplot as plt
import numpy as np


class BasicSimulate:
	current_time = 0
	next_event_time = 0
	ARRIVAL_RATE = .40      #lambda
	SERVICE_RATE = .50        #mu
	SERVER_BUSY = False #This is required to ensure that a process does not enter the queue if there is no one else in the system
	
	def __init__(self):
		'''The constructor'''
		self.customer_pool = {}  #should be a class variable, saving typing
		self.timeline = []  #to be used as a heap or a priority queue
		
		self.service_queue = Queue(0)  #infinite queue
		self.sim_start()
		self.timeline_processor()

	def sim_start(self):
		'''Initialize the system when no process is there'''
		#decide the time at which the first arrival will happen
		#create a customer which will arrive first
		cust = self.create_customer()
		#cust.print_customer()
		#Add the customer to pool

        #Now create an event with this customer and add it to the timeline
        atime = self.create_arrival_event(self.current_time, cust)
        #heappush(self.timeline, (first_arrival_time, event))

        self.create_finish_event(atime + self.current_time, cust)
        #heappush(self.timelinec, (first_service_time, event))
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
#		return Customer(job_arr)

	def print_timeline(self):
		'''A function to print the timeline'''
        print
        for (time,event) in self.timeline:
            print '(%f, %s) <- ' % (time, EventType.name(event.event_type)),
        print 'X'


	def timeline_processor(self):
		'''The function which pulls out events from the timeline and processes them'''

        #log_file = open('log', 'wb')
        '''
        #Code to plot the queue length with steps

        fig=plt.figure()
        plt.axis([0,10000,0,1000])
        plt.ion()
        plt.show()
        plt.xlabel('Step')
        plt.ylabel('Number of jobs')
        plt.title('Number of jobs vs Step')

        '''
        qlen = []

        step = 0
        while(len(self.timeline) > 0 and step < 25000): 

            step = step + 1
            print 'Finished : ', step
            #import os
            #os.system('clear')

            #self.print_timeline()
            (self.current_time, next_event) = heappop(self.timeline)
            #print '\nTime  : %f \n' % self.current_time
            #print 'Event : ', self.current_time, EventType.name(next_event.event_type)
            #print
            if(next_event.event_type == EventType.ARRIVAL):
                #print 'After Processing Arrival :\n'
                self.handle_arrival(next_event)

            elif(next_event.event_type == EventType.SERVICE_FINISH):
                #print 'After Processing Service finish :\n'
                self.handle_service_finish(next_event)
            #Code to plot the queue length with steps


            l = self.service_queue.qsize()
            qlen.append(l)
            '''
            if(step % 1000 == 0):
                x = np.array([i for i in range(0, len(qlen))])
                plt.text(730, 200,'Q length : '  + str(self.service_queue.qsize()), style='italic',
                bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})
                plt.plot(x, qlen)
                plt.draw()
            '''
            #self.printQ()
            #self.print_timeline()
            #log_file.write('%d\n' % (self.service_queue.qsize()))
            #raw_input('\n\n\n[ENTER] to continue')

        #log_file.close()

        '''
        x = np.array([i for i in range(0, len(qlen))])
        #plotQ(qlen)
        plt.text(430, 215,'Average Q length : '  + str(float(sum(qlen)) / len(qlen)), style='italic',
		bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})

			plt.plot(x, qlen)
			plt.draw()
			raw_input('.')

			'''


#		print 'Average queue length = %f' % (float(sum(qlen)) / len(qlen))


	def handle_arrival(self, arrive_event):
		'''Handles the arrival event'''

			#Schedule another arrival

        #Create the customer that will arrive next
        next_cust = self.create_customer() #random customer

        self.create_arrival_event(self.current_time, next_cust)


        #----------------------------------------------------------------
			#Process current arrival

        #Get the customer related to the event
        cust = arrive_event.cust

        #Add the customer to the customer pool
        self.customer_pool[cust.cust_id] = cust

        #TODO : Add this customer to one of the queues
        #For now, add this customer to the only service queue that is present
        if(self.SERVER_BUSY): 
            self.add_to_queue(self.service_queue, cust)
        else: #No need to add to queue, but should mark the server as busy
            self.SERVER_BUSY = True


	def add_to_queue(self, Q, cust):
		'''Add customer to given service queue'''

        Q.put(cust)
        #A departure cannot be scheduled right now because you don't really know how long you'll have to wait


	def printQ(self):
		'''Prints the service queue'''

        print
        for ele in self.service_queue.queue:
            print '||  ',ele.cust_id,'  || <- ',
        print 'X'


	def handle_service_finish(self, finish_event):
		'''Handle service finish event'''

        self.remove_from_queue(self.service_queue)

        if(self.service_queue.qsize() >= 1): 
            #need to schedule a departure
            #get the next customer
            next_customer = self.service_queue.queue[0]
            self.create_finish_event(self.current_time, next_customer)

        if(self.service_queue.qsize() == 0):  #need to schedule an arrival and dept
            self.SERVER_BUSY = False
#            print 'Queue Empty'
            if(len(self.timeline) == 0): #There is no event
                self.sim_start()

            else: 
                #The queue is empty but there is an event on the timeline, thus the event can only be an arrival.
                #Schedule a departure for the arrival
                (time_arrival, event) = self.timeline[0] #heap :)
                self.create_finish_event(time_arrival, event.cust)


	def remove_from_queue(self, Q):

		'''Removes the top most executing process from the queue. Also schedules the next departure'''

        if(Q.qsize() > 0):
            Q.get()

	def create_arrival_event(self, time_from, customer):
		'''Put an arrival event given the parameters on the timeline and return the event time'''

        #Time of next arrival
        next_arrival_time = random.expovariate(self.ARRIVAL_RATE) + time_from;


        #create an event with the next customer and arrival time
        event =  Event(customer, EventType.ARRIVAL,next_arrival_time)

		heappush(self.timeline, (next_arrival_time, event))
		return next_arrival_time

	def create_finish_event(self, time_from, customer):

		'''Put a departure event given the parameters on the timeline and return the event time'''
        service_finish_time = float(time_from) + random.expovariate(self.SERVICE_RATE)
        event =  Event(customer, EventType.SERVICE_FINISH, service_finish_time)
        heappush(self.timeline, (service_finish_time, event))

        return service_finish_time







if __name__ == '__main__':
    b = BasicSimulate()
