#!/usr/bin/python
#coding=utf-8
from __future__ import unicode_literals
import os
import sys
import signal
import urllib2
import subprocess
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
from threading import Thread
from youtube_dl.update import update_self
from .version import __ydlv__

UPDATE_LINK = "https://yt-dl.org/latest/version"
YOUTUBE_DL = "youtube-dl"

class UpdateSelf(QThread):
    reenter_password = QtCore.pyqtSignal()
    update_begin = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    update_end = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    def __init__(self, encoding, password, *args):
        QThread.__init__(self, *args) # Why super doesn't work
        self._encoding = encoding
        self.password = password

    def run(self):
        check = subprocess.Popen(["pip list |grep %s" %YOUTUBE_DL],
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        if YOUTUBE_DL in check.stdout.read():
            self.update()
             
    def update(self):
        """ Update youtube-dl with pip command
            TODO: failure catch
        """
        self.update_begin.emit("Updating", "Updating")
        preexec = os.setsid
        update_self = subprocess.Popen(["sudo -S pip install -U %s" %YOUTUBE_DL],
                                       shell=True, 
                                       preexec_fn=preexec,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        update_self.stdin.write(self.password+"\n")
        stderr = update_self.stderr.readline()
        if "try" in stderr:
            self.reenter_password.emit()
            self.stop(update_self)
            return

        while self._proc_is_alive:
            stdout = update_self.stdout.readline().rstrip()
            stdout = stdout.decode(self._encoding, "ignore")
            if self._is_download(stdout):
                #self._emit(stdout)
                break
        update_self.wait()
        self.update_end.emit("Updated", "Updated")
    
    def stop(self, process):
        """stop subprocess pid , (proces.wait)
        """
        if self._proc_is_alive(process):
            process.terminate()
            process.wait()

    def _proc_is_alive(self, process):
        if process is None:
            return False
        return process.poll() is None   

    def _is_download(self, stdout):
        return "already" in stdout
    
    @classmethod
    def check_version(cls, timeout=30):
        ydlv = UpdateSelf.tuple_version(__ydlv__)     
        try: 
            get_version = urllib2.urlopen(UPDATE_LINK, timeout=timeout)
        except Exception as e:
            return -1
        now_yldv = UpdateSelf.tuple_version(get_version.read())
        if now_yldv > ydlv:
            return 1
        else:
            return 0

    @staticmethod
    def tuple_version(version):
        return tuple(map(int, version.split(".")))



class UpdatePassword(QtGui.QMessageBox):
    update_signal = QtCore.pyqtSignal(int)    
    button_signal = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self,title, *args):
        super(self.__class__, self).__init__(*args)
        self.display(title) 
  
    def display(self, title):
        self.setWindowTitle(title)
        self.setIcon(self.Information)
        self.begin_button = self.addButton("OK", QtGui.QMessageBox.AcceptRole)
        self.begin_button.setEnabled(False)

        self.password_box = QtGui.QLineEdit(self)
        self.password_box.setEchoMode(QtGui.QLineEdit.Password)
        self.password_box.move(100, 23)
        self.password_box.setMaxLength(100)
        self.connect(self.password_box, QtCore.SIGNAL("textChanged(QString)"),
                     self.text_changed)
        self.connect(self, QtCore.SIGNAL("update_signal(int)"),
                     self.button_enable)
        self.connect(self.begin_button, QtCore.SIGNAL("clicked()"),
                     self.button_emit)
          
    #@QtCore.pyqtSlot(str) TODO: SLOT doesn't work
    def text_changed(self, text):
        """Text Changed evoke 
           TODO: input checking
        """
        self.update_signal.emit(1 if str(text).strip() else 0)
    
    def button_enable(self, enable):
        """ Enabel the begin button
        """
        self.begin_button.setEnabled(True if enable else False)

    def button_emit(self):
        self.emit(QtCore.SIGNAL("button_signal(QString)"),
                  QtCore.QString(self.password_box.text()))

