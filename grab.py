#!/usr/bin/env python
import json,thread,Queue

# create a queue by reading in log files
def create_queue(filename):
    q = Queue.Queue()
    q.put(filename)
    
def parse_data(file):    
  with open (file) as data_file:
    data = json.load(data_file)

  info_j = data["additional_info"]["imports"]
  sha_j = data['sha256']

  print "Additional_info imports:\n", json.dumps(info_j, indent=2, sort_keys=True)
  print "SHA256:\t", sha_j

parse_data('files/test.json')
