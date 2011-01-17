#!/usr/bin/env python
# encoding: utf-8
"""
bibparser.py

Created by Dan F-M on 2011-01-16.
"""

import re

class BibTex:
  def __init__(self,fn):
    self.fn = fn
    self.parse()
  
  def parse(self):
    f = open(self.fn)
    self.bib = []
    entry = None
    
    for line in f:
      if line[0] == '@':
        if entry != None:
          self.bib.append(entry)
        entry = {}
      else:
        c = line.split('=')
        if len(c) >= 2 and entry != None:
          entry[c[0].capitalize().strip().strip(',{}')] = c[1].strip().strip(',{}')
    
    self.bib.append(entry)
    # print 'Parsed %d entries in %s'%(len(self.bib),self.fn)

if __name__ == "__main__":
  import sys
  bib = BibTex(sys.argv[1])

