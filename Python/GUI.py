#-*- coding: utf-8 -*-
import sys, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupWindow()
        self.setupButton()
        self.setupLabel()
        self.setupEdit()
        self.setupRadioBox()
        self.setupCheckBox()
        self.setupSpinBox()
        self.setupTableWidget()
        self.statusBar.showMessage("Initialize") # 상태 메세지
    
    def setupWindow(self): # 윈도우 특성 설정 함수
        self.setWindowTitle("Title")  # 윈도우 타이클 지정
        self.setGeometry(300, 300, 500, 400)  # 윈도우 위치, 크기 설정
        self.setWindowIcon(QIcon("D:\\Python\\myWorkspace\\Project\\GUI\\ico\\Icon Entry_6.ico"))  # 아이콘 지정
        
    def setupButton(self): # 버튼 설정 함수
        btn1=QPushButton("Button", self) # 이름
        btn1.setToolTip("ToolTip") # 툴팁
        btn1.resize(btn1.sizeHint()) # 크기
        btn1.move(10, 10) # 위치
        btn1.clicked.connect(self.btnClick) # 함수 실행

        btnLabel=QPushButton("Label", self)
        btnLabel.resize(btnLabel.sizeHint())
        btnLabel.move(10, 40)
        btnLabel.clicked.connect(self.btnLabel)

        btnLabelClear=QPushButton("LabelClear", self)
        btnLabelClear.resize(btnLabelClear.sizeHint())
        btnLabelClear.move(90, 40)
        btnLabelClear.clicked.connect(self.btnLabelClear)

        btnFile=QPushButton("File Open", self)
        btnFile.resize(btnFile.sizeHint())
        btnFile.move(250, 130)
        btnFile.clicked.connect(self.btnFile)

        btnInput=QPushButton("Input", self)
        btnInput.resize(btnInput.sizeHint())
        btnInput.move(250, 180)
        btnInput.clicked.connect(self.btnInput)
        
        btnQuit=QPushButton("Exit", self)
        btnQuit.resize(btnQuit.sizeHint()*2)
        btnQuit.move(300, 300)
        btnQuit.clicked.connect(QCoreApplication.instance().quit) # 종료

    def setupLabel(self): # 레이블 설정 함수
        self.label=QLabel("SelfLabel", self) # 이름
        self.label.move(180, 45) # 위치
        self.label.resize(100, 15) # 크기

        self.fileLabel=QLabel("File Name", self)
        self.fileLabel.move(252, 160)
        self.fileLabel.resize(500, 15)

        self.inputLabel=QLabel("Input Text", self)
        self.inputLabel.move(252, 210)
        self.inputLabel.resize(100, 15)

    def setupEdit(self): # 에디트 설정 함수
        lineEditLabel=QLabel("LineEdit : ", self)
        lineEditLabel.move(10, 73)
        lineEditLabel.resize(100, 15)
        
        self.lineEdit=QLineEdit("", self) # 초기 입력 내용
        self.lineEdit.move(70, 70) # 위치
        self.lineEdit.resize(100, 20) # 크기
        self.lineEdit.textChanged.connect(self.statusBarEdit) # 함수 실행
        
        self.statusBar=QStatusBar(self) # 상태 표시줄 설정
        self.setStatusBar(self.statusBar) 

    def setupRadioBox(self): # 라디오박스 설정 함수
        groupBox=QGroupBox("RadioBox", self) # 그룹 이름
        groupBox.move(10, 100) # 그룹 위치
        groupBox.resize(170, 60) # 그룹 크기

        self.radio1=QRadioButton("First", self) # 이름
        self.radio1.move(20, 110) # 위치
        self.radio1.setChecked(True) # 초기 상태 설정
        self.radio1.clicked.connect(self.choiceRadioBox) # 함수 실행

        self.radio2=QRadioButton("Second", self)
        self.radio2.move(20, 130)
        self.radio2.clicked.connect(self.choiceRadioBox)

        self.statusBar=QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def setupCheckBox(self): # 체크박스 설정 함수
        self.checkBox1=QCheckBox("One", self) # 이름
        self.checkBox1.move(20, 170) # 위치
        self.checkBox1.resize(50, 15) # 크기
        self.checkBox1.stateChanged.connect(self.choiceCheckBox) # 함수 실행

        self.checkBox2 = QCheckBox("Two", self)
        self.checkBox2.move(90, 170)
        self.checkBox2.resize(50, 15)
        self.checkBox2.stateChanged.connect(self.choiceCheckBox)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def setupSpinBox(self): # 스핀박스 설정 함수
        spinBoxLabel=QLabel("Number : ", self)
        spinBoxLabel.move(10, 202)
        spinBoxLabel.resize(70, 15)

        self.spinBox=QSpinBox(self) # 스핀박스
        self.spinBox.move(70, 200) # 위치
        self.spinBox.resize(100, 20) # 크기
        self.spinBox.setSingleStep(100) # 한번 내리고 올릴 때의 값
        self.spinBox.setMinimum(-10000) # 최소값
        self.spinBox.setMaximum(10000) # 최대값
        self.spinBox.setValue(777) # 초기 값
        self.spinBox.valueChanged.connect(self.spinBoxFunc) # 함수 실행

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def setupTableWidget(self): # 테이블위젯 설정 함수
        self.tableWidget=QTableWidget(self) # 테이블위젯
        self.tableWidget.move(250, 20) # 위치
        self.tableWidget.resize(220, 90) # 크기
        self.tableWidget.setRowCount(2) # 행
        self.tableWidget.setColumnCount(2) # 열
        self.tableWidgetData()

    def btnClick(self):
        QMessageBox.information(self, "MsgBox", "Button Click")

    def btnLabel(self):
        self.label.setText("BtnLabel")

    def btnLabelClear(self):
        self.label.clear()
        self.label.setText("SelfLabel")

    def btnFile(self):
        fname=QFileDialog.getOpenFileName(self)
        self.fileLabel.setText(fname)

    def btnInput(self):
        text, okButton=QInputDialog.getInt(self, "InputBox", "Input Value : ")
        if(okButton):
            self.inputLabel.setText(str(text))
    
    def statusBarEdit(self):
        self.statusBar.showMessage("Input : "+self.lineEdit.text())

    def choiceRadioBox(self):
        statusBarMessage=""
        if(self.radio1.isChecked()):
            statusBarMessage="First"
        elif(self.radio2.isChecked()):
            statusBarMessage="Second"
        self.statusBar.showMessage(self.radioBoxFunc(statusBarMessage))

    def radioBoxFunc(self, statusBarMessage):
        QMessageBox.information(self, "MsgBox", statusBarMessage+" Choiced")
        return statusBarMessage+" Choiced"

    def choiceCheckBox(self):
        statusBarMessage=""
        statusOne=""
        statusTwo=""
        if(self.checkBox1.isChecked()==True):
            statusOne="One Checked"
        else:
            statusOne="One Not Checked"
            
        if(self.checkBox2.isChecked()==True):
            statusTwo="Two Checked"
        else:
            statusTwo="Two Not Checked"
        statusBarMessage=statusOne+" & "+statusTwo
        self.statusBar.showMessage(self.checkBoxFunc(statusBarMessage))

    def checkBoxFunc(self, statusBarMessage):
        QMessageBox.information(self, "MsgBox", statusBarMessage)
        return statusBarMessage

    def spinBoxFunc(self):
        num=self.spinBox.value()
        self.statusBar.showMessage("Input : "+str(num))

    def tableWidgetData(self):
        self.tableWidget.setItem(0, 0, QTableWidgetItem("(0,0)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("(0,1)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("(1,0)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("(1,1)"))
    
def main():
    app=QApplication(sys.argv)
    gui=MyWindow()
    gui.show() # 윈도우 화면에 표시
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
