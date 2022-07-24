#!/bin/python3
import os
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from subprocess import check_output

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(490, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelSetDevice = QtWidgets.QLabel(self.centralwidget)
        self.labelSetDevice.setGeometry(QtCore.QRect(20, 30, 260, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.labelSetDevice.setFont(font)
        self.labelSetDevice.setObjectName("labelSetDevice")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(20, 100, 450, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.runButton.setFont(font)
        self.runButton.setObjectName("runButton")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(20, 170, 450, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.refreshButton.setFont(font)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.reScanDevice)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(300, 35, 170, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem('')
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.listDevicesStart()
        self.runButton.clicked.connect(self.startingProgramm)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Flash cleaner"))
        self.labelSetDevice.setText(_translate("MainWindow", "Выберите устройство:"))
        self.runButton.setText(_translate("MainWindow", "Очистить"))
        self.refreshButton.setText(_translate('MainWindow', 'Обновить список устройств'))

    def reScanDevice(self):
        self.comboBox.clear()
        self.comboBox.addItem('')
        self.listDevices()

    def listDevicesStart(self):
        import shlex
        scanDisc = check_output("pkexec fdisk -l | grep \"Disk /dev/\" |grep -v \"Disk /dev/loop\"", shell=True)
        listDisc = scanDisc.decode('utf-8')
        listDisc = listDisc.replace(':','')
        #listDisc = listDisc.replace(',','')
        listDisc = shlex.split(listDisc)
        i = 0
        a = 1
        b = 4
        c = int(len(listDisc)/8)
        for i in range(c):
            setText = ' '.join(listDisc[a:b])
            self.comboBox.addItem(setText)
            i = i + 1
            a = a + 8
            b = b + 8
        a=1
        b=4

    def listDevices(self):
        import shlex
        scanDisc = check_output("sudo fdisk -l | grep \"Disk /dev/\" |grep -v \"Disk /dev/loop\"", shell=True)
        listDisc = scanDisc.decode('utf-8')
        listDisc = listDisc.replace(':','')
        #listDisc = listDisc.replace(',','')
        listDisc = shlex.split(listDisc)
        i = 0
        a = 1
        b = 4
        c = int(len(listDisc)/8)
        for i in range(c):
            setText = ' '.join(listDisc[a:b])
            self.comboBox.addItem(setText)
            i = i + 1
            a = a + 8
            b = b + 8
        a=1
        b=4

    def saveFile(self):
        import shlex
        pathDevice = self.comboBox.currentText()
        pathDevice = shlex.split(pathDevice)
        pathDevice = ''.join(pathDevice[0])
        dumpDevice = check_output('sudo dd if='+pathDevice+' of=/dev/null bs=64', shell=True)

    def startingProgramm(self):
        self.errorMessageWindow = QtWidgets.QErrorMessage()
        self.errorMessageWindow.setWindowTitle("Внимание!")
        self.errorMessageWindow.setGeometry(QtCore.QRect(0, 0, 496, 200))
        self.doneMessageWindow = QtWidgets.QErrorMessage()
        self.doneMessageWindow.setWindowTitle("Выполненое")
        self.doneMessageWindow.setGeometry(QtCore.QRect(0, 0, 496, 200))
        pathDevice = self.comboBox.currentText()
        if pathDevice == '':
            self.errorMessageWindow.showMessage("Ошибка! Вы не выбрали устройство")
            return 1
        else:
            self.saveFile()
            self.doneMessageWindow.showMessage("Информация с "+''.join(dumpDevice[0])+" уничтожена!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
