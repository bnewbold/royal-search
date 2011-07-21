#!/usr/bin/env python
"""Reads in the source data file and prints out a JSON representation.

Typical usage is:

    $ ./parse_source_data.py metadata/########.txt > data.json
"""

import sys, os, traceback, optparse
import time
import json

from datetime import datetime

def parse_meta(name, lines):
    p = {}
    if name.startswith("metadata/"):
        p['_id'] = name[9:].split('.')[0] # strip tailing ".txt"
    else:
        p['_id'] = name.split('.')[0] # strip tailing ".txt"
    p['authors'] = []
    for l in lines:
        if l.startswith('T1'):
            p['title'] = l[5:].strip()
        elif l.startswith('JF'):
            p['journal_name'] = l[5:].strip()
        elif l.startswith('VL'):
            p['volume'] = int(l[5:].strip())
        elif l.startswith('SP'):
            try:
                p['start_page'] = int(l[5:].strip())
            except ValueError:
                pass
        elif l.startswith('EP'):
            try:
                p['end_page'] = int(l[5:].strip())
            except ValueError:
                pass
        elif l.startswith('PY'):
            # UGH, python pre-1900 issues are infuriating
            #p['date'] = datetime.strptime(l[5:].strip(), '%Y/%m/%d/')
            the_date = datetime.strptime(l[5:].strip(), '%Y/%m/%d/')
            p['date_year'] = the_date.year
            p['date_month'] = the_date.month
        elif l.startswith('UR'):
            p['doi_url'] = l[5:].strip()
        elif l.startswith('M3'):
            p['doi'] = l[5:].strip()
        elif l.startswith('AU'):
            p['authors'].append(l[5:].strip())

    if p.get('start_page') and p.get('end_page'):
        p['page_length'] = p['end_page'] - p['start_page']
    return p

def main ():
    """Reads, parses, and dumps a paper metadata file
    """

    global options, args

    papers = []
    for filename in args:
        with open(filename, "r") as f:
            paper_meta = parse_meta(filename, f.readlines())
            papers.append(paper_meta)
    print json.dumps(papers)

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        if len(args) < 1:
            parser.error ('missing filename(s) argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN SECONDS:',
        if options.verbose: print (time.time() - start_time)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
