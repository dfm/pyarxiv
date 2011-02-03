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
# 
# __init__.py
# 
# Created by Dan F-M on 2011-02-02.
#

"""
A module for parsing the arxiv and making suggestions.
"""

from parse import *
from feed import *

import numpy as np

def check_arxiv():
  lib = BibTexLibrary('test.pkl')
  feed = ArxivFeed()
  
  prob = []
  for i in xrange(len(feed.entries)):
    nouns = feed.nouns[i]
    freq = feed.freq[i]
    freq_tmp = np.zeros(len(lib.nouns))
    for i in xrange(len(nouns)):
      try:
        freq_tmp[lib.nouns.index("".join(nouns[i]))] += freq[i]
      except:
        pass
    prob.append(np.dot(freq_tmp,lib.freq))
  
  prob = np.array(prob)
  order = np.argsort(prob)[::-1]
  print prob[order]
  
  for i in order:
    print "".join(feed.entries[i]['title'].split('(')[:-1])
    print feed.entries[i]['summary']
    print "\t",feed.entries[i]['link']
    print

