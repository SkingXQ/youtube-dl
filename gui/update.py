#!/usr/bin/python
#coding=utf-8
from __future__ import unicode_literals

import urllib2
from PyQt4.QtCore import QThread, SIGNAL
from threading import Thread
from youtube_dl.update import update_self
from .version import __ydlv__

UPDATE_LINK = "https://yt-dl.org/latest/version"

class test(Thread):
    def __init__(self):
        pass

class UpdateSelf(QThread):
    def __init__(self):
        super(self.__class__, self).__init__()

    def run(self):
        pass

    @classmethod
    def check_version(cls, timeout=20):
        ydlv = UpdateSelf.tuple_version(__ydlv__)     
        try: 
            get_version = urllib2.urlopen(UPDATE_LINK, timeout=timeout)
        except Exception as e:
            print e
            return -1
        now_yldv = UpdateSelf.tuple_version(get_version.read())
        if now_yldv > ydlv:
            return 1
        else:
            return 0

    @staticmethod
    def tuple_version(version):
        return tuple(map(int, version.split(".")))

