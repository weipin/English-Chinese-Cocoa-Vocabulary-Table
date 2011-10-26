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
from collections import defaultdict

help_message = '''
[SAMPLE]
./txt2csv.py -f table.txt -o output.csv
'''

def processTableFile(f):
    CommentPattern = re.compile(r"^#\s*(.*)")
    TypePattern = re.compile(r"^([~!@#$%^&*()_+])$")
    BlankLinePattern = re.compile(r"^\s*$")
    
    inSection = False
    sectionGroups = defaultdict(list)
    section = None
    
    for line in f:
        isBlank = BlankLinePattern.search(line)
        if isBlank:
            if inSection:
                sectionType = section.get('Type', '~')              
                sectionGroup = sectionGroups[sectionType]
                sectionGroup.append(section)                
                
                inSection = False
                section = None
                
        else:
            if not inSection:
                inSection = True
                section = {}
                
            # type
            m = TypePattern.search(line)
            if m:
                section['Type'] = m.group(1)
            # comment
            m = CommentPattern.search(line)
            if m:
                section['Comment'] = m.group(1).strip()
            # English & Chinese
            if 'English' not in section and 'Chinese' not in section:
                section['English'] = line.strip()
            elif 'English' in section and 'Chinese' not in section:
                section['Chinese'] = line.strip()
            else:
                pass    
            
    return sectionGroups    

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
    sectionGroups = processTableFile(f)
    
    OrderedTypes = tuple("~!@#$%^&*()_+")
    content = ""
    
    for i in OrderedTypes:
        group = sectionGroups.get(i, None)
        if not group:
            continue
        
        for j in group:
            content += "%s, %s, %s\r\n" % (j.get("English", ""), j.get("Chinese", ""), j.get("Comment", ""))
            
        content += " ,  ,  \r\n\r\n\r\n"
    
    f = open(output, 'w')
    f.write(content)

    
if __name__ == "__main__":
    sys.exit(main())
