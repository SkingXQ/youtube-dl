#!/usr/bin/python
#coding=utf-8
from __future__ import unicode_literals


import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """checking internet situation
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        pass
    return False
