# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 15:35:40 2018

@author: ibrahim
"""
import subprocess
import shlex
import ape.components.component as component
file_name = component.__file__.rstrip('c')
command = 'pyreverse -o png -p componentplain {0}'.format(file_name)
subprocess.call(shlex.split(command))