#!/bin/env python
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

import pyarxiv

class Article:
  def __init__(self, arxivid=None):
    if arxivid:
      self.setarxivid(arxivid)

  def setarxivid(self, arxivid):
    self.arxivid = arxivid
    self.fillfeilds()

  def fillfeilds(self):
    self.metadata = pyarxiv.metadata(self.arxivid)
    self.references, extrameta = pyarxiv.references(self.arxivid, self.metadata["bibcode"])
    self.metadata.update(extrameta)
    self.citations,extrameta = pyarxiv.citations(self.arxivid, self.metadata["bibcode"])
    self.metadata.update(extrameta)

  def __str__(self):
    return "arXiv article %s:\n\tmeta: %s\n\trefs: %s\n\tcits: %s"%(self.arxivid, self.metadata, self.references, self.citations)

def dfs(aid,agraph,pgraph,parent=None,max_depth=-1):
  article = Article(aid)
  print "\t"*(5-max_depth),"Found %s"%article.metadata["title"]

  # this quick hack doesn't support unicode so screw foreign 
  # authors :p... so we just "try" and reject entries giving 
  # errors
  try:
    pgraph.add_node(article.metadata["title"])
    agraph.add_node(article.metadata["author"])
    if parent:
      pgraph.add_edge(parent.metadata["title"], article.metadata["title"])
      agraph.add_edge(parent.metadata["author"], article.metadata["author"])
  
    if max_depth == 0:
      return
  
    for i in article.references:
      dfs(i, agraph, pgraph, parent=article, max_depth=max_depth-1)
  except:
    return

if __name__ == "__main__":
  import sys
  import pygraphviz as pgv
  agraph = pgv.AGraph(strict=False, directed=True)
  pgraph = pgv.AGraph(strict=False, directed=False)

  dfs(sys.argv[1], agraph, pgraph, max_depth=5)
  pgraph.write("papers.dot")
  pgraph.layout('dot')
  pgraph.draw("papers.png")
  agraph.write("authors.dot")
  agraph.layout('dot')
  agraph.draw("authors.png")
