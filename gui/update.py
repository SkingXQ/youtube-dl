#!/usr/bin/python
#coding=utf-8
from __future__ import unicode_literals
import sys
import urllib2
import subprocess
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
from threading import Thread
from youtube_dl.update import update_self
from .version import __ydlv__

UPDATE_LINK = "https://yt-dl.org/latest/version"
YOUTUBE_DL = "youtube-dl"

class UpdateSelf(Thread):
    def __init__(self):
        Thread.__init__(self) # Why super doesn't work
        self._encoding = "utf-8"

    def run(self):
        print "update"
        #password_box = QtGui.QMessageBox()
        #password_label = QtGui.QLabel(password_box)
        password_text = QtGui.QLineEdit()
        password_text.setText("Please Enter your password:")
        #password_box.exec_()
        print "line text"
        return
        check = subprocess.Popen(["pip list |grep %s" %YOUTUBE_DL],
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        if YOUTUBE_DL in check.stdout.read():
            self.update()
             
    def update(self):
        print "begin"
        update_self = subprocess.Popen(["sudo -S pip install -U %s" %YOUTUBE_DL],
                                 shell=True, 
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        print update_self.stderr.read()
        print  update_self.stdout.read()
        return
        if "sudo" in update_self.stdout.read():
            password = "sking"
            update_self.stdin.write(password+"\n")
        while self._proc_is_alive:
            stdout = update_self.stdin.readline().rstrip()
            stdout = stdout.decode(self._encoding, "ignore")
            print stdout
            if self._is_successful(stdout):
                self._emit(stdout)
                break
        print "shi"     
    
    def stop():
        pass

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
    def __init__(self,):
        super(self.__class__, self).__init__()
        self.display()
   
    def display(self):
        self.setWindowTitle("Please Enter Your Password:")
        self.setIcon(self.Information)
        self.begin_button = self.addButton("OK", QtGui.QMessageBox.AcceptRole)


        password_box = QtGui.QLineEdit(self)
        password_box.setEchoMode(QtGui.QLineEdit.Password)
        password_box.move(100, 23)
        password_box.setMaxLength(100)
        self.connect(password_box, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SLOT("text_changed(str)"))
       # password_infobox.connect(self, QtCore.SIGNAL("passwrod_emit()"),
            #                     self, QtCore.SLOT("button_enable()"))
       # password_infobox.exec_()
    @QtCore.pyqtSlot(str)
    def text_changed(self, text):
        print "chang"
        if text is not "":
            self.emit(QtCore.SIGNAL("password_emit()"))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main =  UpdatePassword()
    main.show()
    app.exec_()

        
