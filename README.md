log processor
===
Description
---
grab some json files, end goal being to export to csv

Instructions
---

- clone repo
- run script:
```
$ python grab.py
```
The main threaded method is parse_data(q)
Pass in the name of the queue to work from, add or remove elements as needed.
NOTE: make sure all tasks are done before the q.task_done() call as this registers back to the queue and you don't want dangling tasks

Variables
---
num_threads: each thread reads a file and outputs - adjust based on system memory
file_dir: path to directory containing the log files - include trailing /

