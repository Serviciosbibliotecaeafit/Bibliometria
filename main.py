import sys
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

"""
    UI usando PyQt6 y QtQml.

    Update Notes:
    - v0.1.0: UI básica con la única base de datos registrada hasta el momento,
    esta incluye las siguientes características en forma de señales Qml->PyQt6:
        * Boton logo EAFIT
        * Boton de main_process que pasa 5 str
        * Boton de exportacion de obtenidos
        * Boton de exportacion de backup que pasa 2 str

    Señales PyQt6->Qml:
        * updated: Pasa el registro de funcionamiento de Selenium
        * progress: Pasa el progreso de obtencion de datos
        * finishedSearching: Detiene threads cuando la busqueda termina

    Estas ultimas tres señales funcionan bajo el mismo deamon thread que ejecuta _bootUp
"""

class Window(QObject):
    def __init__(self):
        super().__init__()
        self.proccessing = False # True cuando se está realizando la obtencion de data


    @pyqtSlot()
    def webpage(self):
        # Boton logo EAFIT
        webbrowser.open('https://www.eafit.edu.co')


    @pyqtSlot(str, str)
    def exportBackup(self, dataBase, outputFolder):
        # Boton de exportacion de backup
        Export_Backup(dataBase, outputFolder.split("///")[1])


    @pyqtSlot(str, str, str, str, str)
    def main_process(self, inputFile, data_base, outputFolder, email, password,):
        """
            Pasa todos los inputs necesarios para realizar la obtencion y normalizacion de datos.

            Variables:
            - inputFile: Path al archivo de urls para la obtencion
            - data_base: Nombre de la base de datos de los datos
            (hasta el momento el usuario no puede seleccionar bases de datos no registradas, tener cuidado)
            - outputFolder: Path al directorio de salida de los datos
            - email: Primera credencial para acceder a la pagina web, tambien podría ser un nombre de usuario en otras bases de datos
            - password: Segunda credencial de acceso (!TENER CUIDADO CON LA PRIVACIDAD DEL USUARIO!)
        """
        self.filename = inputFile.split("///")[1]
        self.dataBase = data_base
        self.outputFolder = outputFolder.split("///")[1]
        self.credentials = {
            'email': email,
            'password': password
        }
        self.ResetLogs() # Reseteamos el registro de actividad de Selenium
        self.proccessing = True
        self.bootUp() # Ejecutamos el deamon thread para registro de actividad y procesos secundarios
        main_thread = threading.Thread(target=self._main_process)
        main_thread.start()


    def _main_process(self):
        # main thread
        self.obtainedData = Search_Data(self.dataBase, self.filename, self.credentials)


    @pyqtSlot()
    def export(self):
        # Exportacion de datos obtenidos
        Export(self.obtainedData, self.outputFolder)

    
    # Registros
        # Registro de actividad
    updated = pyqtSignal(str, arguments=['updater']) # type: ignore
        # Registro de progreso
    progress = pyqtSignal(float, arguments=['progress_Bar']) # type: ignore
        # Registro de finaliazion
    finishedSearching = pyqtSignal(bool, arguments=['finished']) # type: ignore


    # Emision de señales
    def updater(self, data_log):
        # Actividad
        self.updated.emit(data_log)
    def progress_Bar(self, progressValue):
        # Progreso
        self.progress.emit(progressValue)
    def finished(self, finished):
        # Finalizacion    
        self.finishedSearching.emit(finished)


    # Thread secundario de registros
    def bootUp(self):
        # Ejecucion
        log_thread = threading.Thread(target=self._bootUp)
        log_thread.daemon = True
        log_thread.start()
    def _bootUp(self):
        # Thread secundario
        while self.proccessing:
            # Actividad
            log_file = open("./selenium_outputs/log.out", "r")
            # Progreso
            progress_file = open("./selenium_outputs/progress.out", "r")

            data_log = log_file.read()
            progress_read = progress_file.read()

            progressValue = float(progress_read) # Conversion str to float

            log_file.close()
            progress_file.close()
            
            # Emision
            self.updater(data_log)
            self.progress_Bar(progressValue)

            # Verificacion de finalizacion
            if progressValue > 100:
                self.finished(True)
                self.proccessing = False
                
            sleep(1) # puede variar para mejorar rendimiento
    
    def ResetLogs(self):
        # Reseteo de registros de actividad y progreso
        log_file = open("./selenium_outputs/log.out", "w")
        progress_file = open("./selenium_outputs/progress.out", "w")

        progress_file.write('0.0')

        log_file.close()
        progress_file.close()


# Inicializacion de UI con una unica pagina
app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

window = Window()

engine.rootContext().setContextProperty("window", window)

engine.load('./UI/main.qml')

sys.exit(app.exec())
