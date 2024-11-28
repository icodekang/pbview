from main import *
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QEvent, QTimer
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import time

GLOBAL_STATE = False    # max min flag
GLOBAL_TITLE_BAR = True


class UIFuncitons(MainWindow):
    # maximize window
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False: 
            GLOBAL_STATE = True
            self.showMaximized()    # maximize
            self.max_sf.setToolTip("Restore")
        else:
            GLOBAL_STATE = False
            self.showNormal()       # minimize
            self.resize(self.width()+1, self.height()+1)
            self.max_sf.setToolTip("Maximize")
    
    # window control
    def uiDefinitions(self):
        # Double-click the title bar to maximize
        def dobleClickMaximizeRestore(event):
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFuncitons.maximize_restore(self))
        self.top.mouseDoubleClickEvent = dobleClickMaximizeRestore
        
        # MOVE WINDOW / MAXIMIZE / RESTORE
        def moveWindow(event):
            if GLOBAL_STATE:                        # IF MAXIMIZED CHANGE TO NORMAL
                UIFuncitons.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:    # MOVE
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
        self.top.mouseMoveEvent = moveWindow

        # MINIMIZE
        self.min_sf.clicked.connect(lambda: self.showMinimized())
        # MAXIMIZE/RESTORE
        self.max_sf.clicked.connect(lambda: UIFuncitons.maximize_restore(self))
        # CLOSE APPLICATION
        self.close_button.clicked.connect(self.close)