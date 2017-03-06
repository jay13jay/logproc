#!/usr/bin/env python
import json,thread,Queue,glob

num_threads = 2

file_queue = Queue.Queue()
# pass list of filenames
def add_items(files,q):
    for f in files:
        q.put(f)

# pass name of queue, returns item from queue
def get_item(q):
    if not q.empty():
        return q.get()
    
# pass a directory containg json encoded files - include trailing /
def get_files(directory):
    path = directory + '*.json'
    files = glob.glob(path)
    add_items(files,file_queue)

# pass 'file' - a JSON encoded filepath - print out needed values
def parse_data(q):
    while not q.empty():
        f = get_item(q)
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
        worker.start()


build_threads(file_queue,num_threads)
