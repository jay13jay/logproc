#!/usr/bin/env python
import json
with open ('test.json') as data_file:
    data = json.load(data_file)

additional_info_j = data["additional_info"]["imports"]
res1 = data["additional_info"]["imports"]
sha_j = data['sha256']

print "Additional_info imports:\n", json.dumps(res1, indent=2, sort_keys=True)
print "SHA256:\t", sha_j
