#!/usr/bin/python
from __future__ import unicode_literals
import sys
import os.path

# include project directory
PATH = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(PATH)))

import gui


