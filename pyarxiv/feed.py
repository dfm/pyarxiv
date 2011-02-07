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
# feed.py
# 
# Created by Dan F-M on 2011-02-02.
#

import sys

import feedparser

from languagetools import *

default_url = ["http://arxiv.org/rss/astro-ph","http://arxiv.org/rss/cs"]
# default_url = "astro-ph"

class ArxivFeed:
  def __init__(self,url=None):
    if url == None:
      url = default_url
    
    self.nouns = []
    self.freq  = []
    
    print "Analyzing new articles... this may take a while..."
    # get feeds...
    try:
      self.entries = []
      for u in url:
        for e in feedparser.parse(u)['entries']:
          self.entries.append(e)
    except:
      self.entries = feedparser.parse(url)['entries']
    
    for ind,e in enumerate(self.entries):
      nouns,freq = get_nouns(e['summary']+" "+e['title'])
      self.nouns.append(nouns)
      self.freq.append(freq)
      
      # progress bar
      sys.stdout.flush()
      nmax = 50
      n = int(float(ind+1)/len(self.entries)*nmax)
      print "".join(['   [',('+')*(n),(' ')*(nmax-n),
                '] %6.1f %%'])%(float(ind+1)/len(self.entries)*100.), "\r",

