#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2011 Daniel Foreman-Mackey and Michael Gorelick
# 
# This is part of pyarxiv.
# 
# pyarxiv is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# 
# pyarxiv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyarxiv.  If not, see <http://www.gnu.org/licenses/>.
#

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

