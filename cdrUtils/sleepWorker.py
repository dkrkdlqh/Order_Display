from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal

class SleepWorker(QThread):

    timer = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.isRunning = True
        self.sleepTime = 1 # 테스트 타이머 주기 (초)

    def run(self):
        while True:
            if not self.isRunning :
                break
            self.timer.emit() # 시그널 방출
            self.sleep(self.sleepTime)   

    def stop(self):
        self.isRunning = False

#    def resume(self):
#        self.isRunning = True
