#!/usr/bin/python
# coding=utf-8

import os
import sys
import signal

from PyQt4 import QtGui
from PyQt4 import QtCore

from .version import __version__, __help_info__, __ydlv__
from .update import UpdateSelf
from .update import UpdatePassword
from .utils import check_internet


class YoutubeDLGui(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Setting main windows
        screen  = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width(), screen.height())
        self.setWindowTitle("Youtube Downloader")
        self.statusBar().showMessage("Ready")

        # Menubar
        menubar = self.menuBar()
        toolbar = self.addToolBar('Action')
        file_bar = menubar.addMenu("&File")
        exit = self._add_action(["Exit",
                                 QtCore.SIGNAL("triggered()"),
                                 QtCore.SLOT("close()")],
                                file_bar, toolbar)
        menubar.insertSeparator(exit)


        # Help
        self.password_infobox = None
        help_menubar = menubar.addMenu("&Help")
        help_acction = self._add_action(["About",
                                         QtCore.SIGNAL("triggered()"),
                                         self.help_messagebox],
                                        help_menubar)

    def _add_action(self, actions, menubar, toolbar=None, icon=None):
        """ Add actions for menubar
        """

        if icon:
            tmp_action = QtGui.QAction(QtGui.QIcon(icon),               
                                       actions[0], self)
        else:
            tmp_action = QtGui.QAction(actions[0], self)

        tmp_action.setShortcut("Ctrl+"+actions[0][0].upper())
        tmp_action.setStatusTip(actions[0])
        menubar.addAction(tmp_action)
        menubar.insertSeparator(tmp_action)
        if toolbar:
            toolbar.addAction(tmp_action)
        self.connect(tmp_action,
                     actions[1],
                     actions[2])
        return tmp_action
        
    def help_messagebox(self):
        """ Show informations(triggered doesn't send data)
            Bug: if messageBox add two button it won't close when click X
            Solve method: stackoverflow.com/questions/7543258/adding-detailed-text-in-qmessagebox-makes-close-x-button-disabled
           
        """  
        title = "About Youtube Downloader"
        info_message = self.get_helpinfo() %(self.get_ydlv(), self.get_version())

        self.info_box = QtGui.QMessageBox(self)
        self.info_box.setText(info_message)
        self.info_box.setWindowTitle(title)
        self.info_box.setIcon(self.info_box.Information)
        if UpdateSelf.check_version() == 1:
            update_button = self.info_box.addButton("Update", 
                                                    QtGui.QMessageBox.RejectRole)
            self.connect(update_button, QtCore.SIGNAL("clicked()"), self.update)
        ok_button = self.info_box.addButton("OK", QtGui.QMessageBox.AcceptRole)
        self.info_box.show()

    def update(self):
        """
        """
        if not self.password_infobox:
            self.password_infobox = UpdatePassword("Please Enter Your Password:",
                                                   self)
        # Make a mistake here , connect before show
            self.connect(self.password_infobox, 
                         QtCore.SIGNAL("button_signal(QString)"), 
                         self.update_thread)
        self.password_infobox.show()
        return
   
    def update_thread(self, text):
        """ Initial the update_thread
        """
        self.update_thread = UpdateSelf(self.get_preferencode(), 
                                        str(text).strip(), 
                                        self)
        self.connect(self.update_thread, QtCore.SIGNAL("reenter_password()"),
                     self.reenter_pw)
        self.connect(self.update_thread, QtCore.SIGNAL("update_begin(QString, QString)"),
                     self.update_process)
        self.connect(self.update_thread, QtCore.SIGNAL("update_end(QString, QString)"),
                     self.update_process)
        self.update_thread.start()


    def reenter_pw(self):
        self.password_infobox.setWindowTitle("Wrong Password, Pleas enter again:")
        self.password_infobox.show()

    def update_process(self, title, text):
        update_info_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                             title,
                                             text,
                                             QtGui.QMessageBox.NoButton,
                                             self)
        update_info_box.show()
         

    def get_preferencode(self):
        """ Get system preferred encode method
            TODO: get encode method from system
        """
        return "utf-8"

    def get_version(self):
        return __version__

    def get_helpinfo(self):
        return __help_info__

    def get_ydlv(self):
        return __ydlv__

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main =  YoutubeDLGui()
    main.show()
    app.exec_()

