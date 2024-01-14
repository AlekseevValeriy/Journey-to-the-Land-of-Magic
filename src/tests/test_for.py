# importing the modules 
from threading import *
import time

# creating thread instance where count = 3 
my_obj = Semaphore(1)


# creating instance
def show():
    my_obj.acquire()
    time.sleep(1)
    print(1)
    my_obj.release()


thread_1 = Thread(target=show)
thread_2 = Thread(target=show)
thread_3 = Thread(target=show)
thread_4 = Thread(target=show)
thread_5 = Thread(target=show)
thread_6 = Thread(target=show)

# calling the threads  
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()
thread_5.start()
thread_6.start()