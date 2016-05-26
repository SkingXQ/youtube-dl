#!/usr/bin/python
# coding=utf-8

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

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


        # open_action = self._add_action([""])

        # Help
        help_menubar = self.menuBar()
        help_acction = self._add_action(["Help",
                                         QtCore.SIGNAL("triggered()"),
                                         self.help_messagebox],
                                        menubar, toolbar)

    def _add_action(self, actions, menubar, toolbar=None, icon=None):
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
        """ Show informations(triggered doesn't send event)
        """  
        info_message = ""
        title = "About Youtube Downloader"
        info_box = QtGui.QMessageBox.information(self, 
                                                 title, 
                                                 info_message)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = YoutubeDLGui()
    main.show()
    sys.exit(app.exec_())
