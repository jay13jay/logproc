#!/usr/bin/env python
import json,Queue,glob
from threading import Thread

num_threads = 2 
file_queue = Queue.Queue()
threads = []

# include trailing / - adds files in directory to queue
def get_files(directory,q):
    path = directory + '*.json'
    files = glob.glob(path)
    print files
    count = 0
    for f in files:
        q.put(f)
        count += 1
    return count

# pass 'file' - a JSON encoded filepath - print out needed values
def parse_data(q):
    with not q.empty():
        f = q.get()
    with open (f) as data_file:
        data = json.load(data_file)

    info_j = data["additional_info"]["imports"]
    sha_j = data['sha256']

#    print "Additional_info imports:\n", json.dumps(info_j, indent=2, sort_keys=True)
    print "SHA256:\t", sha_j

def build_threads(q,batch):
    for i in range(batch):
        worker = Thread(target=parse_data,args=(q,))
        worker.setDaemon(True)
        threads.append(worker)

def start_threads(count):
    for t in threads:
        print "Starting thread: ", count
        t.start()

def main():
    thread_count = 0
    # get_files populates queue, returns an integer of amount of items put in queue
    num_files = get_files('files/',file_queue)
    while not file_queue.empty():
        # set up threads
        if num_threads <= num_files:
            build_threads(file_queue,num_threads)
        elif num_threads > num_files:
            build_threads(file_queue,num_files)
        # print thread count
        print "total threads:", len(threads)
        # Start threads
        start_threads(thread_count)
        # join threads
        thread_count = 0
        for t in threads:
            t.join()
            print "LOT:",len(threads)
            threads.pop(thread_count)
            thread_count += 1
            print "LOT:",len(threads)



main()
