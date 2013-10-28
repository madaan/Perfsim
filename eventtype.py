#sg
class EventType:

    ARRIVAL = 0
    #Silly implementation, find a workaround
    SERVICE_FINISH_1 = 1
    SERVICE_FINISH_2 = 2
    SERVICE_FINISH_3 = 3
    
    #NOTE  : Service finish may or may not mean departure

    def type_from_num(self, number):
        if(number == 0):
            return EventType.ARRIVAL
        elif(number == 1):
            return EventType.SERVICE_FINISH_1
        elif(number == 2):
            return EventType.SERVICE_FINISH_2
        elif(number == 3):
            return EventType.SERVICE_FINISH_3

    def name(self, number):
        if(number == 0):
            return "ARRIVAL"
        elif(number == 1):
            return "SERVICE_FINISH Q1"
        elif(number == 2):
            return "SERVICE_FINISH Q2"
        elif(number == 3):
            return "SERVICE_FINISH Q3"
    name = classmethod(name)
    type_from_num = classmethod(type_from_num)
