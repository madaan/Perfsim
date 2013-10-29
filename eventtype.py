#sg
class EventType:

    ARRIVAL = 0
    NUM_QUEUES = 4
    #Silly implementation, find a workaround
    SERVICE_FINISH = []
    for i in range(0, NUM_QUEUES):
        SERVICE_FINISH.append(i)
    #NOTE  : Service finish may or may not mean departure

    def type_from_num(self, queue_number):
        #This function will always be called with queue number

        '''
        if(queue_number == 0):
            return EventType.SERVICE_FINISH[queue_number]
        elif(queue_number == 1):
            return EventType.SERVICE_FINISH_1
        elif(queue_number == 2):
            return EventType.SERVICE_FINISH_2
        elif(queue_number == 3):
            return EventType.SERVICE_FINISH_3
        '''
        return EventType.SERVICE_FINISH[i]

    def name(self, number):
        if(number == 0):
            return "ARRIVAL"
        elif(number == 1):
            return "SERVICE_FINISH Q0"
        elif(number == 2):
            return "SERVICE_FINISH Q1"
        elif(number == 3):
            return "SERVICE_FINISH Q2"

    name = classmethod(name)
    type_from_num = classmethod(type_from_num)
