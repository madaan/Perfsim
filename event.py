#sg
from eventtype import EventType
class Event:

    def __init__(self, cust, event_type, time):
        self.customer = cust #id of the customer to which this event belongs to
        self.event_type = event_type #type of the event
        self.time = time #time of event
       

    def event_details(self):

        print 'Time : %s, Cust id : %s, Type = %s' % (self.time, self.cust.cust_id, EventType.name(self.event_type))
