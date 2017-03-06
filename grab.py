#!/usr/bin/env python
import json,Queue,glob
from threading import Thread

num_threads = 2 
file_queue = Queue.Queue()
threads = []

# pass list of filenames
def add_items(files,q):
    for f in files:
        q.put(f)

# include trailing / - adds files in directory to queue
def get_files(directory):
    path = directory + '*.json'
    files = glob.glob(path)
    add_items(files,file_queue)

# pass 'file' - a JSON encoded filepath - print out needed values
def parse_data(q):
    while not q.empty():
        f = q.get()
        print f
        with open (f) as data_file:
            data = json.load(data_file)

    info_j = data["additional_info"]["imports"]
    sha_j = data['sha256']

    print "Additional_info imports:\n", json.dumps(info_j, indent=2, sort_keys=True)
    print "SHA256:\t", sha_j

def build_threads(q,batch):
    for i in range(batch):
        worker = Thread(target=parse_data,args=(q,))
        worker.setDaemon(True)
        threads.append(worker)

def start_threads():
    count = 0
    for t in threads:
        print "Starting thread: ", count
        t.start()
        count += 1

def main():
    # retrive files
    get_files('files/')
    # set up threads
    build_threads(file_queue,num_threads)
    # print thread count
    print len(threads)
    # Start threads
    start_threads()
    # join threads
    for t in threads:
        print t
        t.join()




file_queue.join()

main()
