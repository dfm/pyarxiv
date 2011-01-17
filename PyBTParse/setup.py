#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup
from distutils.extension import Extension
import numpy.distutils.misc_util
import subprocess
import os

btparse_dir = '/usr/local'
base_dir = os.getcwd()
os.chdir('btparse/src/')
subprocess.Popen(['./configure','--prefix=%s'%btparse_dir]).wait()

# os.environ['CFLAGS'] = '-m32'

subprocess.Popen(['make']).wait()
subprocess.Popen(['make','install']).wait()
os.chdir(base_dir)

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

