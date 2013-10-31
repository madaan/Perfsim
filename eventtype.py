#sg
from configuration import Config
class EventType:

    ARRIVAL = -1
    #Silly implementation, find a workaround
    SERVICE_FINISH = []
    config = Config('perfsim.config')
    NUM_SERVER = config.NUM_SERVER
    for i in range(0, NUM_SERVER):
        SERVICE_FINISH.append(i)
    #NOTE  : Service finish may or may not mean departure

    def type_from_num(self, queue_number):
        #This function will always be called with queue number

        #For zeroth row, the event is SERVICE_FINISH[1]

        return EventType.SERVICE_FINISH[queue_number]

    def queue_from_event(self, etype):
        '''
        Right now, the enumeration is simple. The queue associated with
        SERVICE_FINISH[i] is i - 1
        '''
        return etype

    def name(self, number):
        if(number == -1):
            return "ARRIVAL"
        else:
            return "SERVICE_FINISH Q" + str(number)

    name = classmethod(name)
    type_from_num = classmethod(type_from_num)
    queue_from_event = classmethod(queue_from_event)
