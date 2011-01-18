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

from distutils.core import setup
from distutils.extension import Extension
import numpy.distutils.misc_util
import subprocess
import os

btparse_dir = '/usr/local'
# base_dir = os.getcwd()
# os.chdir('btparse/src/')
# subprocess.Popen(['./configure','--prefix=%s'%btparse_dir]).wait()
# 
# os.environ['CFLAGS'] = '-m32'
# 
# subprocess.Popen(['make']).wait()
# subprocess.Popen(['make','install']).wait()
# os.chdir(base_dir)

setup(name='btparse',
        version='1.0',
        description='btparse',
        author='Daniel Foreman-Mackey',
        author_email='danfm@nyu.edu',
        package_dir={'btparse':'btparse'},
        packages=['btparse'],
        ext_modules = [Extension(name='btparse._C_btparse', sources=['btparse/btparse.c'],
                        libraries=['btparse'],library_dirs=['%s/lib'%(btparse_dir)])],
        include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs()+['%s/include'%(btparse_dir)],
      )

