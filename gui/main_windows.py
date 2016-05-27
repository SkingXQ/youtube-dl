#!/usr/bin/python
# coding=utf-8

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from .version import __version__, __help_info__, __ydlv__
from .update import UpdateSelf, test

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
        """  
        title = "About Youtube Downloader"
        info_message = self.get_helpinfo() %(self.get_ydlv(), self.get_version())

        info_box = QtGui.QMessageBox()
        info_box.setText(info_message)
        info_box.setWindowTitle(title)
        info_box.setIcon(info_box.Information)
        ok_button = info_box.addButton("OK", QtGui.QMessageBox.AcceptRole)
        check1 = test()
        if UpdateSelf.check_version() == 1:
            update_button = info_box.addButton("Update", 
                                               QtGui.QMessageBox.AcceptRole)
            check = UpdateSelf()
        info_box.exec_()

    def get_version(self):
        return __version__

    def get_helpinfo(self):
        return __help_info__

    def get_ydlv(self):
        return __ydlv__

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = YoutubeDLGui()
    main.show()
    sys.exit(app.exec_())
