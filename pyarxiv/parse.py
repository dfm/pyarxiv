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
# parse.py
# 
# Created by Dan F-M on 2011-02-02.
#

"""
This script parses the abstracts and titles in a bibtex document and 
returns all the nouns and their relative frequencies
"""

import sys
import pickle
import numpy as np

import btparse

try:
  import pytools
except:
  pytools = False

from languagetools import *


class BibTexLibrary:
  def __init__(self,path):
    """'path' can point to either a pickle file or a .bib file"""
    try:
      # we'll see if it's a pickle file?
      self.nouns,self.freq = pickle.load(open(path,'rb'))
    except:
      self.bib = btparse.load(path)
      
      # tokenize the library
      self.nouns = []
      self.freq  = []
      if pytools:
        progress = pytools.ProgressBar("Analysing",len(self.bib))
        progress.draw()
      else:
        print 'Tokenizing library... this may take some time...'
      for ind,entry in enumerate(self.bib):
        if ('abstract' in self.bib[ind].keys()) and ('title' in self.bib[ind].keys()):
          tokens,freq = get_nouns(self.bib[ind]['abstract']+" "+self.bib[ind]['title'])
          for i,w in enumerate(tokens):
            try:
              self.freq[self.nouns.index(w)] += freq[i]
            except:
              self.nouns.append(w)
              self.freq.append(freq[i])
        
        if pytools: progress.progress()
        else:
          sys.stdout.flush()
          nmax = 50
          n = int(float(ind)/len(self.bib)*nmax)
          print "".join(['   [',('+')*(n),(' ')*(nmax-n),
                    '] %6.1f %%'])%(float(ind)/len(self.bib)*100.), "\r",
      
  def save(self,path):
    """save to a file"""
    pickle.dump((self.nouns,self.freq),open(path,'wb'),-1)


