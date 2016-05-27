#!/usr/bin/python
from __future__ import unicode_literals
import sys
import os.path

# include project directory
PATH = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(PATH)))

from gui.main_windows import YoutubeDLGui
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)
main = YoutubeDLGui()
main.show()
sys.exit(app.exec_())

