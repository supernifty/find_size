#!/usr/bin/env python

import argparse
import os
import collections
import logging
import re
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

def find(dir, include, exclude):
    extensions = collections.defaultdict(int)
    extensions_count = collections.defaultdict(int)
    total = 0
    count = 0
    skipped = 0

    for path, dirs, files in os.walk(dir):
       for filename in files:
           # add file size to the extension dictionary item, instead of add 1 
           try:
               if include is not None and re.search(include, filename) is None:
                   skipped += 1
                   continue
               if exclude is not None and re.search(exclude, filename) is not None:
                   skipped += 1
                   continue

               file_size = os.path.getsize(os.path.join(path,filename))
               extensions[os.path.splitext(filename)[-1].lower()] += file_size
               extensions_count[os.path.splitext(filename)[-1].lower()] += 1
               total += file_size
               count += 1
               if count % 1000 == 0:
                   logging.debug('%i files processed. Total size %s. Skipped %i', count, human(total), skipped)

           except OSError as e:
               logging.warn("%s", e)

    sys.stdout.write('Extension,Size,Count\n')
    for key, value in sorted(extensions.items(), key=lambda item: (item[1], item[0])):
        sys.stdout.write('%s,%s,%i\n' % (key, human(value), extensions_count[key]))

    sys.stdout.write('TOTAL,%s,%i\n' % (human(total), count))

def main():
    parser = argparse.ArgumentParser(description='find total file sizes by extension')
    parser.add_argument('--dir', default='.', help='')
    parser.add_argument('--include', required=False, help='only include files matching pattern')
    parser.add_argument('--exclude', required=False, help='exclude files matching pattern')
    parser.add_argument('--verbose', action='store_true', default=False, help='more logging')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    find(args.dir, args.include, args.exclude)

if __name__ == '__main__':
    main()
