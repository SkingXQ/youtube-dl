#!/usr/bin/python
# coding=utf-8

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from .version import __version__, __help_info__, __ydlv__
from .update import UpdateSelf

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

        self.info_box = QtGui.QMessageBox()
        self.info_box.setText(info_message)
        self.info_box.setWindowTitle(title)
        self.info_box.setIcon(self.info_box.Information)
        ok_button = self.info_box.addButton("OK", QtGui.QMessageBox.AcceptRole)
        if UpdateSelf.check_version() == 1:
            update_button = self.info_box.addButton("Update", 
                                                   QtGui.QMessageBox.AcceptRole)
            self.connect(update_button, QtCore.SIGNAL("clicked()"), self.update)
        self.info_box.exec_()

    def update(self):
        password_infobox = QtGui.QMessageBox()
        password_infobox.setWindowTitle("Please Enter Your Password:")
        password_infobox.setIcon(password_infobox.Information)
        self.begin_button = password_infobox.addButton("OK", QtGui.QMessageBox.AcceptRole)
        
       
        password_box = QtGui.QLineEdit(password_infobox)
        password_box.setEchoMode(QtGui.QLineEdit.Password)
        password_box.move(100, 23)
        password_box.setMaxLength(100)
        password_infobox.connect(password_box, QtCore.SIGNAL("textChanged(QString)"),  
                                 self, QtCore.SLOT("text_changed(text)"))
        password_infobox.connect(self, QtCore.SIGNAL("passwrod_emit()"), 
                                 self, QtCore.SLOT("button_enable()"))
        password_infobox.exec_()
        return
        check = UpdateSelf()
        check.start()
   
    @QtCore.pyqtSlot()
    def text_changed(self, text):
        print "chang"
        if text is not "":
            self.emit(QtCore.SIGNAL("password_emit()"))

    @QtCore.pyqtSlot()
    def button_enable(self):
        print "helo button"

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
