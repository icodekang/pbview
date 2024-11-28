# -*- coding: utf-8 -*-

import os
import sys
import json
import queue
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDesktopServices
from ui.home import Ui_MainWindow
from UIFunctions import *
import pb.pb_parser as pbParser

class ConsumerThread(QThread):
    updateSignal = Signal(str)

    def setParam(self, pbQue):
        self.pbQue = pbQue

    def run(self):
        while True:
            pbContent = self.pbQue.get()
            if pbContent is None:
                self.updateSignal.emit(f"finish")
                break
            self.updateSignal.emit(pbContent)
            self.pbQue.task_done()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # basic interface
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)  # rounded transparent
        self.setWindowFlags(Qt.FramelessWindowHint)  # Set window flag: hide window borders
        UIFuncitons.uiDefinitions(self)

        self.pbFileName = None
        self.bStartParse = False
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.upload_button.clicked.connect(self.uploadPbFile)
        self.run_button.clicked.connect(self.startParsePbFile)
        self.src_file_button.clicked.connect(self.openCurDir)

    def mousePressEvent(self, event):
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos

    def openCurDir(self):
        curDir = os.getcwd()
        QDesktopServices.openUrl(QUrl.fromLocalFile(curDir))

    def uploadPbFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择PB数据文件", "", "所有文件 (*)")
        if filename:
            self.tip_name.setText(f"文件:")
            self.file_name.setText(f"{filename}")
            self.pbFileName = filename
        else:
            self.pbFileName = None
            self.setTips(f"Get file info failed!")
        self.progress_bar.setValue(0)

    def startParsePbFile(self):
        self.pb_content.clear()
        self.progress_bar.setValue(0)
        if not self.pbFileName:
            self.setTips(f"Please upload file first!")
            self.run_button.setChecked(False)
        else:
            self.bStartParse = True
            self.run_button.setChecked(True)
            self.pbQue = queue.Queue(maxsize=1024)
            self.producerThread = threading.Thread(target=pbParser.pbParseThread, args=(self.pbFileName, self.pbQue), daemon=True)
            self.consumerThread = ConsumerThread()
            self.consumerThread.updateSignal.connect(self.updatePbText)
            self.consumerThread.setParam(self.pbQue)
            self.producerThread.start()
            self.consumerThread.start()

    def updatePbText(self, text):
        if text == f"finish":
            self.progress_bar.setValue(100)
            self.run_button.setChecked(False)
        else:
            self.pb_content.append(text)
            self.pb_content.append("\r\n")
            jsonData = json.loads(text)
            self.progressValue = jsonData['progress']
            self.progress_bar.setValue(self.progressValue)

    def setTips(self, tip):
        self.tip_name.setText(f"提示:")
        self.file_name.setText(tip)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Home = MainWindow()
    Home.show()
    sys.exit(app.exec())  