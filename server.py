#sg
from Queue import *
class Server:
    '''The class which models a server'''
    def __init__(self, fatigue_cap, break_time):
        self.Q = Queue(0) #service_queue
        self.fatigue_cap = fatigue_cap #to model interrupts
        self.served = 0 #number of users served
        self.break_time = break_time
        self.SERVER_BUSY = False


