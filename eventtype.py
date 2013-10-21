#sg
class EventType:

    ARRIVAL = 1
    SERVICE_FINISH = 2
    #NOTE  : Service finish may or may not mean departure

    def name(self, number):
        if(number == 1):
            return "ARRIVAL"
        elif(number == 2):
            return "SERVICE_FINISH"
    name = classmethod(name)
