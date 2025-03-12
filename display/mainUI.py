import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic
from pymodbus.transaction import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout

from data.color import Color
from display.slotUI import SlotItem
from cdrUtils.sleepWorker import SleepWorker
from PyQt5.QtCore import pyqtSlot

import socket
import threading
import select

import time


#파일의 절대 경로 정보 반환 --> exe 형태로 앱 배포 시  필요.
def getAbsResPath(relative_path:str) -> str:
    
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



# 연동할 타겟 UI 클래스 불러오기
form = getAbsResPath('mainUI.ui')
form_class = uic.loadUiType(form)[0]

class MainUI(QMainWindow, form_class):

    def __init__(self):

        super().__init__()
        
        #타겟 *.ui 파일의 UI 정보를 화면에 출력 
        self.setupUi(self)
        self.initVar()
        self.initUI()


    #변수 선언
    def initVar(self):
        self.slot_tuple = ("a","b","c","d","e")
        self.__trayNum                  :int        = 2
        
        self.slotItemList:list = []
        self.ui_slot : list = []
        self.uiCount = 0

        #UI 상태 변화 테스트용 쓰레드. 
        # 1초마다 타이머가 작동되는 SleepWorker() 쓰레드에 테스트용 함수인 self.testMonitorItemUI를 연결해준다.
        self.sleepWorker = SleepWorker()
        self.sleepWorker.start()
        self.sleepWorker.timer.connect(self.testSlotItemUI) # 시그널 슬롯 등록
        
        #self.ui_slot_A = 0
        #self.ui_slot_B = 0
        #self.ui_slot_C = 0

        self.evt = threading.Event()
        self.UI_update_thread = threading.Thread(target=self.func_UI_Update)        
        self.UI_update_thread.start()
        

    def __del__(self) :
        self.evt.set()
    
    def closeEvent(self, event):
        self.evt.set()
        print("프로그램 종료11")
        self.sleepWorker.stop()
        print("프로그램 종료22")
        self.sleepWorker.timer.disconnect()
        print("프로그램 종료33")
        
        self.UI_update_thread.join()
        print("프로그램 종료")
        QApplication.quit()
        sys.exit()
        


    #UI 초기화
    def initUI(self):    

        self.setWindowTitle("주문 알림 서비스")#앱 상단 타이틀
        #self.setFixedSize(800, 600) #창 사이즈 고정
        self.setCenterPos() #앱을 스크린의 '중앙' 위치로
        self.drawSlotItemUI()


    #앱을 스크린 좌상단에 위치
    def setLeftTop(self):
        rect = self.frameGeometry()
        self.move(rect.topLeft())       

    #화면 스크린 정중앙에 UI 위치
    def setCenterPos(self):

        rect = self.frameGeometry()
        point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(point)
        self.move(rect.topLeft())   


    # 슬롯 아이템 UI 객체의 인스턴스를 생성 -> 그리드 레이아웃에 배치 -> 배열에 저장
    def drawSlotItemUI(self):

        #row = 1
        #col = self.__trayNum#2#3
        #len = row * col

        for i in range(self.__trayNum):
            item:SlotItem = SlotItem()
            gridLayout:QGridLayout = self.gridLayout
            gridLayout.addWidget(item, int(i/self.__trayNum), i % self.__trayNum + 1)
            item.setSlotNum(' ')#(str(i))
            self.slotItemList.append(item) 
            self.ui_slot.append(None)



    # 슬롯 ui 값 변경 테스트 함수 
    @pyqtSlot()           
    def testSlotItemUI(self):        
        for i in range(self.__trayNum):
            self.setSlotUI(i,self.ui_slot[i])
        #self.setSlotUI(0,self.ui_slot_A)
        #self.setSlotUI(1,self.ui_slot_B)
       # self.setSlotUI(2,self.ui_slot_C)

    
    # def testSlotItemUI(self):
        
    #     if self.uiCount == 0:
        
    #         self.setSlotUI(0,0)
    #         self.setSlotUI(1,0)
    #         self.setSlotUI(2,0)

    #     elif self.uiCount == 1:

    #         self.setSlotUI(0,11)
    #         self.setSlotUI(1,12)
    #         self.setSlotUI(2,13)

    #     self.uiCount += 1
    #     if self.uiCount > 1 : 
    #         self.uiCount = 0
    
    def func_UI_Update(self):
        '''
        # TCP/IP Server
        recv_value : slot Number, orderId
        '''
    
        host_addr = '127.0.0.1'
        host_port = 6666
        TCP_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_Server.bind((host_addr, host_port))

        TCP_Server.listen(5)
        print(f"서버가 {host_addr}:{host_port}에서 대기 중입니다...")

        input_list = [TCP_Server]  # 서버 소켓을 추가해 클라이언트 대기

        while True:
            if self.evt.is_set():
                break

            # select()를 통해 연결 대기
            input_ready, _, _ = select.select(input_list, [], [], 1)
            for sock in input_ready:
                if sock == TCP_Server:  # 서버 소켓에서 연결 요청 대기
                    client_socket, client_address = TCP_Server.accept()
                    print(f"클라이언트 {client_address}가 연결되었습니다.")
                    self.ui_slot = [0] * len(self.ui_slot)
                    input_list.append(client_socket)  # 클라이언트 소켓을 리스트에 추가

                else:  # 클라이언트 소켓에서 데이터 수신
                    try:
                        data = sock.recv(1024).decode("utf-8")
                        if not data:  # 클라이언트 연결 종료 시
                            input_list.remove(sock)
                            sock.close()
                            print("클라이언트 연결이 끊어졌습니다.")
                            self.ui_slot = [None] * len(self.ui_slot)
                            continue

                        print(f"받은 데이터: {data}")
                        if data[0] == '$':  # 데이터 처리
                            for i in range(1, len(data)):
                                if data[i] == '%':
                                    break
                            print(data[1], data[2:i])
                            data_slot = data[1]
                            data_ordernum = int(data[2:i])

                            if data_slot in self.slot_tuple:
                                index = self.slot_tuple.index(data_slot)
                                self.ui_slot[index] = data_ordernum
                            else:
                                print('not in slot')
                                

                            time.sleep(0.3)  # 서버가 계속 실행 중인 상태로 잠시 대기
                    except Exception as e:
                        print(f"오류 발생: {e}")
                        input_list.remove(sock)
                        sock.close()

            

        # 서버 종료 전 리소스 정리
        for sock in input_list:
            if sock != TCP_Server:
                sock.close()

        TCP_Server.close()
        print("서버 종료..")


    # ======================================== UI 상태값 설정 함수 ===================================================== 
    
    def setSlotUI(self, slotNum:int, orderNum:int):
        slotItem:SlotItem = self.slotItemList[slotNum]
        #print(f'{orderNum}')
        if orderNum == None :
          slotItem.setOrderNum("ㅡㅡ")
        else :
          slotItem.setOrderNum("{0:0=3d}".format(orderNum))


