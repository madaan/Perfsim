#sg
import event
class Event:

    int customer #id of the customer to which this event belongs to
    int event_type #type of the event
    int time #time of event
    def __init__(self, cust, event_type, time):
        self.cust = cust
        self.event_type = event_type
        self.time = time




