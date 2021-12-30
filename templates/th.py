import threading
import os

def task1():
   #  print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 1: {} {}".format(threading.current_thread().name, os.getpid()))
  
# def task2():
#     print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
#     print("ID of process running task 2: {}".format(os.getpid()))
  
if __name__ == "__main__":
  
    # print ID of current process
   print("ID of process running main program: {}".format(os.getpid()))
  
    # print name of main thread
   print("Main thread name: {}".format(threading.current_thread().name))
  
    # creating threads
   threads = []

   for i in range(100):
      t = threading.Thread(target=task1, name='t'+str(i))
      threads.append(t)

   # starting threads
   for t in threads:
      t.start()

   # wait until all threads finish
   for t in threads:
      t.join()