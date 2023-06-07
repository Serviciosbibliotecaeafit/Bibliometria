import sys
import os
import webbrowser
import threading
from time import sleep

from main_program import Search_Data, Export, Export_Backup
import selenium_methods as sm
import norm_methods as norm
import pandas as pd

from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication

class Window(QObject):
    def __init__(self):
        super().__init__()
        self.proccessing = False

    @pyqtSlot()
    def webpage(self):
        webbrowser.open('https://www.eafit.edu.co')

    @pyqtSlot(str, str)
    def exportBackup(self, dataBase, outputFolder):
        Export_Backup(dataBase, outputFolder.split("///")[1])

    @pyqtSlot(str, str, str, str, str)
    def main_process(self, inputFile, data_base, outputFolder, email, password,):
        self.filename = inputFile.split("///")[1]
        self.dataBase = data_base
        self.outputFolder = outputFolder.split("///")[1]
        self.credentials = {
            'email': email,
            'password': password
        }
        self.ResetLogs()
        self.proccessing = True
        self.bootUp()
        main_thread = threading.Thread(target=self._main_process)
        #main_thread.daemon = True
        main_thread.start()
        
    def _main_process(self):
        self.obtainedData = Search_Data(self.dataBase, self.filename, self.credentials)

    @pyqtSlot()
    def export(self):
        Export(self.obtainedData, self.outputFolder)
    
    updated = pyqtSignal(str, arguments=['updater']) # type: ignore
    progress = pyqtSignal(float, arguments=['progress_Bar']) # type: ignore
    finishedSearching = pyqtSignal(bool, arguments=['finished']) # type: ignore

    def updater(self, data_log):
        self.updated.emit(data_log)
    
    def progress_Bar(self, progressValue):
        self.progress.emit(progressValue)
    
    def finished(self, finished):
        self.finishedSearching.emit(finished)

    def bootUp(self):
        log_thread = threading.Thread(target=self._bootUp)
        log_thread.daemon = True
        log_thread.start()
    
    def _bootUp(self):
        while self.proccessing:
            log_file = open("./selenium_outputs/log.out", "r")
            progress_file = open("./selenium_outputs/progress.out", "r")
            data_log = log_file.read()
            progress_read = progress_file.read()
            progressValue = float(progress_read)
            log_file.close()
            progress_file.close()
            self.updater(data_log)
            self.progress_Bar(progressValue)
            if progressValue > 100:
                self.finished(True)
                self.proccessing = False
            sleep(1)
    
    def ResetLogs(self):
        log_file = open("./selenium_outputs/log.out", "w")
        progress_file = open("./selenium_outputs/progress.out", "w")
        progress_file.write('0.0')
        log_file.close()
        progress_file.close()

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

window = Window()

engine.rootContext().setContextProperty("window", window)

engine.load('./UI/main.qml')

#window.bootUp()

sys.exit(app.exec())
