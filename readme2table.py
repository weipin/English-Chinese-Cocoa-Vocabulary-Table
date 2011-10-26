#!/usr/bin/env python
# encoding: utf-8
"""
txt2csv.py

Created by  on 2011-10-26.
Copyright (c) 2011 Weipin Xia. All rights reserved.
"""

import os
import sys
import getopt
import re

help_message = '''
[SAMPLE]
./readme2table.py -f README -o table.txt
'''   

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hf:o:", ["help", "file=", "output="])
        except getopt.error, msg:
            raise Usage(msg)
        
        path = None
        output = None
                
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-f", "--file"):
                path = value
            if option in ("-o", "--output"):
                output = value    
        
        if not path or not output:
            raise Usage(help_message)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    f = open(path, 'r')
    content = f.read()
    
    m = re.search(r"### START ###(.*)### END ###", content, re.MULTILINE | re.DOTALL)
    if m:
        content = m.group(1)
    else:
        print "Error!"
        sys.exit()
    
    f = open(output, 'w')
    f.write(content)

    
if __name__ == "__main__":
    sys.exit(main())
