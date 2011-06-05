#!/usr/bin/env python
"""Reads in the source data file and prints out a JSON representation.

Typical usage is:

    $ ./parse_source_data.py source_data/properties6.dat.txt > data.json
"""

import sys, os, traceback, optparse
import time
import json

def parse_material(lines):
    m = {}
    try:
        # _id is, unexpectedly, actually a string
        m['_id'] = lines[0].split()[0]
        m['name'] = ""
        m['name'] = lines[1][6:].strip()
        m['type'] = lines[0][75]
        m['phase'] = lines[0][64]
        num_elements = 1
        if m['type'] in ['E', 'R']:
            m['chemical_symbol'] = lines[1].split()[0]
            num_elements = int(lines[0][67])
        else:
            num_elements = int(lines[0][67])
        m['atomic_weight'] = float(lines[0][15:].split()[0])
        m['density'] = float(lines[0][53:].split()[0])
       
        # Clean up name (it gets a bunch of junk that isn't JSON-safe...)
        while m['name'].find('#') >= 0:
            m['name'] = " ".join(m['name'].split()[:-1])
        m['name'] = m['name'].replace('=', "equals")


        # Expand type and phase chars out into full string
        m['type'] = {
            'E': "Element",
            'R': "Radioactive Element",
            'I': "Inorganic Compound",
            'O': "Organic Compound",
            'P': "Polymer",
            'M': "Mixture",
            'B': "Biological",
            ' ': "[none]" }[m['type']]
        m['phase'] = {
            'S': "Solid",
            'L': "Liquid",
            'G': "Gas",
            'D': "Diatomic Gas",
            ' ': "[none]" }[m['phase']]
        
        m['melting_point'] = None
        m['boiling_point'] = None
        m['index_of_refraction'] = None
        m['notes'] = None

        # Check for extra info and notes
        if len(lines) - num_elements > 3:
            for l in lines[3+num_elements:]:
                if l.lower().startswith("melti"):
                    # this handles some format-breaking special cases
                    if len(l) < 30:
                        m['melting_point'] = float(l[10:].split()[0])
                    else:
                        m['melting_point'] = float(l[25:].split()[0])
                elif l.lower().startswith("boili"):
                    m['boiling_point'] = float(l[25:].split()[0])
                elif l.lower().startswith("index"):
                    m['index_of_refraction'] = float(l[25:].split()[0])
                elif (l.lower().startswith("note:") or
                      l.startswith("     ")):
                    if not m['notes']:
                        m['notes'] = l[6:]
                    else:
                        m['notes'] += l[6:]
        if m['notes']:
            m['notes'] = m['notes'].replace('\\', "\\\\")
            m['notes'] = m['notes'].replace('<', "\<")
            m['notes'] = m['notes'].replace('>', "\>")
            m['notes'] = m['notes'].replace('=', "\=")
            m['notes'] = m['notes'].strip()
            m['notes'] = "Notes aren't working right now."
        
        if m['atomic_weight'] < 0:
            m['atomic_weight'] = None
    except Exception, e:
        # This program is not robust...
        print "----------------------------------------------"
        print "UNEXPECTED ERROR!\n"
        traceback.print_exc()
        sys.exit()
    
    if options.verbose:
        print m['_id']
        print m['name']
        print m['type']
        print m['phase']
        print m['atomic_weight']
        print m['density']
    
    return m

def main ():
    """Reads, parses, and dumps materials one at a time.
    """

    global options, args
    
    materials = []
    buff = []
    f = open(args[0], "r")
    for l in f.readlines():
        if l.startswith("------"):
            materials.append(parse_material(buff))
            buff = []
            continue;
        buff.append(l)
    
    if options.verbose: 
        print "----------------------------------------------"
        print "Found " + str(len(materials)) + " materials"

    # Ok, now print out in JSON format...
    print json.dumps(materials, indent=4)

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        if len(args) < 1:
            parser.error ('missing argument')
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
