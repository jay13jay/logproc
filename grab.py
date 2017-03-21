#!/usr/bin/env python3
import json,queue,glob
from threading import Thread


num_threads = 2 
file_queue = queue.Queue()
threads = []

# include trailing / - adds files in directory to queue
def get_files(directory,q):
    path = directory + '*'
    files = glob.glob(path)
    count = 0
    for f in files:
        q.put(f)
        count += 1
    return count

# pass 'file' - a JSON encoded filepath - print out needed values
def parse_data(q):
    while not q.empty():
        f = q.get()
        try:
            with open (f) as data_file:
                data = json.load(data_file)
                data_file.close()

            info_j = data["additional_info"]["imports"]
            sha_j = data['sha256']

            #
            # print "Additional_info imports:\n", json.dumps(info_j, indent=2, sort_keys=True)
            print("SHA256:\t", sha_j)
            q.task_done()
        except:
            print("unable to open file!", f)
            q.task_done()


def build_threads(q,batch):
    for i in range(batch):
        worker = Thread(target=parse_data,args=(q,))
        worker.setDaemon(True)
        threads.append(worker)

def start_threads():
    count = 0
    for i in range(len(threads)):
        threads[i].start()
        count += 1

def main():
    thread_count = 0
    # get_files populates queue, returns an integer of amount of items put in queue
    num_files = get_files('files/',file_queue)
    #while not file_queue.empty():
        # set up threads
    if num_threads <= num_files:
        build_threads(file_queue,num_threads)
    elif num_threads > num_files:
        build_threads(file_queue,num_files)
    print("total threads:", len(threads))
    start_threads()
    # join threads
    thread_count = 0
    for i in range(len(threads)):
        threads[i].join()
            


print("Starting main loop")
main()
print("passed main, joining queue")
file_queue.join()
print("done!")
