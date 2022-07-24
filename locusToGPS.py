#!/usr/bin/env python


# Generate JSON from a LOCUS log file
# (c) 2013 Don Coleman 

import locus
import json
import datetime
import os
coords = locus.parseFile('sample.log')

# filter out bad data
coords = [c for c in coords if c.fix > 0 and c.fix < 5] 

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, locus.Coordinates):
            return obj.__dict__

        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S%z")

        return json.JSONEncoder.default(self, obj)
#print(coords[1]'latitude')
#print(dir(coords[0]))
#print(type(coords[0]))
#print(coords[0].longitude)
#print( json.dumps(coords, cls = Encoder, sort_keys=True, indent=4))
#print(os.getcwd())
for i in range(len(coords)):
    print(coords[i].latitude,',',coords[i].longitude)
