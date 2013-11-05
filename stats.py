#sg
from customer import *
class Stats:
    def average_waiting_time(self, cust_pool):
        total_waiting_time = 0
        for id in cust_pool.keys():
            total_waiting_time = total_waiting_time + cust_pool[id].waiting_time

        return 1.0 * total_waiting_time / len(cust_pool.keys())
    average_waiting_time = classmethod(average_waiting_time)
