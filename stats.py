#sg
from customer import *
class Stats:
    def average_waiting_time(self, cust_pool):
        '''Average amount of time that any customer has to wait'''
        total_waiting_time = 0
        for id in cust_pool.keys():
            total_waiting_time = total_waiting_time + cust_pool[id].waiting_time

        return 1.0 * total_waiting_time / len(cust_pool.keys())

    def average_response_time(self, cust_pool):
        '''Average amount of time that it takes for a customer to enter
        the system and exit it'''
        total_response_time = 0
        total_finished = 0 #the number of users who have finished
        for id in cust_pool.keys():
            if(cust_pool[id].final_exit_time != -1):
                total_response_time = total_response_time + (cust_pool[id].final_exit_time - cust_pool[id].first_entry_time)
                total_finished = total_finished + 1
        #Must be in try etc
        try:
            return 1.0 * total_response_time / total_finished
        except:
            print 'DIV by 0 in average_response_time'
            return float("inf")
    def throughput(self, cust_pool, start_time, end_time):
        if(end_time - start_time == 0):
            print 'Error in throughput, check the parameters'
            return float("inf")
        total_finished = 0
        for id in cust_pool.keys():
            if(cust_pool[id].final_exit_time != -1):
                total_finished = total_finished + 1

        return 1.0 * total_finished / (end_time - start_time)


    #Declare the methods as classmethods. Seems better for some reason
    average_waiting_time = classmethod(average_waiting_time)
    average_response_time = classmethod(average_response_time)
    throughput = classmethod(throughput)
