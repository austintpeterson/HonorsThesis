#here to figure out spawning separate jobs
#note: probably going to try to use subprocesses from here on out

#import Queue
#multithreading is less costly than new processes
import threading

from threading import Thread
from multiprocessing import Process
from multiprocessing.dummy import Pool as ThreadPool
import time, os

#ez function to test threading
# def thread_func(x):
# 	print("Im a process %s, my father is %s"% (os.getpid(), os.getpid()))
# 	time.sleep(5)
# 	print("time sleep of 5 finished for process: "+str(x))


#simple workers to test
def worker(num):
	print("Worker: "+str(num)+" started")
	time.sleep(5)
	print("Worker: "+str(num)+" ended")
	return

def worker_2():
	print("worker 2 started")


def main():
	#thr = threading.Thread(target = thread_func())
	# for i in range(0,3):
	# 	print("starting process: "+str(i))
	# 	Process(target = thread_func(i)).start()

	# jobs = []
	# for i in range(0, 3):
	# 	p = multiprocessing.Process(target = worker, args = (i,))
	# 	jobs.append(p)
	# 	p.start()

	#q = Queue.Queue()

	for i in range(0,3):
		
		#1
		#new_thread = Thread(target = worker(i), args = (i, ))
		#new_thread.start()
		#see if I can NOT use join
		#new_thread.join()
		
		#2
		# try:
		# 	thread.start_new_thread(worker, (i, ))
		# except:
		# 	print("unable to start new thread")

		# WINNER
		t = threading.Thread(target = worker, args = (i, ))
		t.start()


	print("threads created and running")
	time.sleep(50)


	













































main()