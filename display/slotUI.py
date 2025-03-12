import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

from data.color import Color


#파일의 절대 경로 정보 반환 --> exe 형태로 앱 배포 시 필요.
def getAbsResPath(relative_path:str) -> str:
    
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    

# 연동할 타겟 UI 클래스 불러오기
form = getAbsResPath('slotUI.ui')
widgetForm, baseClass= uic.loadUiType(form)


class SlotItem(baseClass, widgetForm):

    def __init__(self, parent=None):

        super(SlotItem, self).__init__(parent)
        self.setupUi(self)
        self.initUI()


    def initUI(self):
        self.slotLabel.setText("xxx")
        self.orderLabel.setText("000")


    def setSlotNum(self, text:str):
        self.slotLabel.setText(text)


    def setOrderNum(self, text:str):
        self.orderLabel.setText(text)
    

    # ========================================================================================================== 
    #라벨 텍스트 색상 설정하기
    def setLabelColor(self, label:QLabel, color:Color):

        styleSheet:str = ""
        if color == Color.WHITE:
            styleSheet = "color: rgb(255,255,255);"
        elif color == Color.BLACK:
            styleSheet = "color: rgb(0,0,0);"
        elif color == Color.RED:
            styleSheet = "color: rgb(194,23,29);"
        elif color == Color.GREEN:
            styleSheet = "color: rgb(29,168,77);"
        elif color == Color.BLUE:
            styleSheet = "color: rgb(31,90,194);"

        label.setStyleSheet(styleSheet)


    
    def setStateLabelFocus(self, label:QLabel, focusColor:Color):

        styleSheet:str = "color:rgb(255,255,255); border-style:none; border-radius:5px;"
        
        if  focusColor == Color.NONE:
            styleSheet += "background-color: rgba(0,0,0,0);"
        elif focusColor == Color.WHITE:
            styleSheet += "background-color: rgb(255,255,255);"
        elif focusColor == Color.BLACK:
            styleSheet += "background-color: rgb(0,0,0);"
        elif focusColor == Color.RED:
            styleSheet += "background-color: rgb(194,23,29);"
        elif focusColor == Color.GREEN:
            styleSheet += "background-color: rgb(29,168,77);"
        elif focusColor == Color.BLUE:
            styleSheet += "background-color: rgb(31,90,194);"

        label.setStyleSheet("QLabel{" + styleSheet + "}")