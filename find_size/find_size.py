#!/usr/bin/env python

import os
import collections
import sys

def human(s):
    if s < 1e3:
        return s
    elif s < 1e6:
        return '{:.1f}kB'.format(s / 1e3)
    elif s < 1e9:
        return '{:.1f}MB'.format(s / 1e6)
    elif s < 1e12:
        return '{:.1f}GB'.format(s / 1e9)
    else:
        return '{:.1f}TB'.format(s / 1e12)

extensions = collections.defaultdict(int)
total = 0

for path, dirs, files in os.walk('.'):
   for filename in files:
       # add file size to the extension dictionary item, instead of add 1
       try:
           file_size = os.path.getsize(os.path.join(path,filename))
           extensions[os.path.splitext(filename)[-1].lower()] += file_size
           total += file_size
       except OSError as e:
           sys.stderr.write("ERROR: {}\n".format(e))

for key, value in sorted(extensions.items(), key=lambda item: (item[1], item[0])):
    sys.stdout.write('%s,%s\n' % (key, human(value)))

sys.stdout.write('TOTAL,%s\n' % (human(total)))
