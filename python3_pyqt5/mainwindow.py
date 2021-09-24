from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from videopanel import VideoPanel

import socket

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.__videoPanel.startService()

    def closeEvent(self, e):
        self.__videoPanel.stopPlay()
        self.__videoPanel.dislink()
        self.__videoPanel.stopService()
        
    def initUi(self):
        self.setObjectName("MainWindow")
        self.resize(980, 550)

        self.gridLayoutUI = QGridLayout(self)
        self.gridLayoutUI.setObjectName("gridLayoutUI")
        self.gridLayoutVideo = QGridLayout()
        self.gridLayoutVideo.setObjectName("gridLayout")

        spacerItemVideo = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayoutVideo.addItem(spacerItemVideo, 1, 0, 1, 1)
        self.horizontalLayoutControl = QHBoxLayout()
        self.horizontalLayoutControl.setObjectName("horizontalLayoutControl")
        self.gridLayoutControl = QGridLayout()
        self.gridLayoutControl.setObjectName("gridLayoutControl")

        self.__linkButton = QPushButton(self)
        sizePolicyForLink = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicyForLink.setHorizontalStretch(0)
        sizePolicyForLink.setVerticalStretch(0)
        sizePolicyForLink.setHeightForWidth(self.__linkButton.sizePolicy().hasHeightForWidth())
        self.__linkButton.setSizePolicy(sizePolicyForLink)
        self.__linkButton.setMinimumSize(QSize(0, 40))
        self.__linkButton.setObjectName("link")
        self.__linkButton.setText("连接")
        self.__linkButton.clicked.connect(self.onButtonLink)
        self.gridLayoutControl.addWidget(self.__linkButton, 4, 0, 1, 1)

        self.__dislinkButton = QPushButton(self)
        self.__dislinkButton.setEnabled(False)
        sizePolicyForDislink = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicyForDislink.setHorizontalStretch(0)
        sizePolicyForDislink.setVerticalStretch(0)
        sizePolicyForDislink.setHeightForWidth(self.__dislinkButton.sizePolicy().hasHeightForWidth())
        self.__dislinkButton.setSizePolicy(sizePolicyForDislink)
        self.__dislinkButton.setMinimumSize(QSize(0, 40))
        self.__dislinkButton.setObjectName("dislink")
        self.__dislinkButton.setText("断开连接")
        self.__dislinkButton.clicked.connect(self.onButtonDislink)
        self.gridLayoutControl.addWidget(self.__dislinkButton, 4, 1, 1, 1)

        self.__playButton = QPushButton(self)
        self.__playButton.setEnabled(False)
        sizePolicyForPlay = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicyForPlay.setHorizontalStretch(0)
        sizePolicyForPlay.setVerticalStretch(0)
        sizePolicyForPlay.setHeightForWidth(self.__playButton.sizePolicy().hasHeightForWidth())
        self.__playButton.setSizePolicy(sizePolicyForPlay)
        self.__playButton.setMinimumSize(QSize(0, 40))
        self.__playButton.setObjectName("play")
        self.__playButton.setText("播放")
        self.__playButton.clicked.connect(self.onButtonStartPlay)
        self.gridLayoutControl.addWidget(self.__playButton, 6, 0, 1, 1)

        self.__stopButton = QPushButton(self)
        self.__stopButton.setEnabled(False)
        sizePolicyForStop = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicyForStop.setHorizontalStretch(0)
        sizePolicyForStop.setVerticalStretch(0)
        sizePolicyForStop.setHeightForWidth(self.__stopButton.sizePolicy().hasHeightForWidth())
        self.__stopButton.setSizePolicy(sizePolicyForStop)
        self.__stopButton.setMinimumSize(QSize(0, 40))
        self.__stopButton.setObjectName("stop")
        self.__stopButton.setText("停止播放")
        self.__stopButton.clicked.connect(self.onButtonStopPlay)
        self.gridLayoutControl.addWidget(self.__stopButton, 6, 1, 1, 1)

        spacerItemControl = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayoutControl.addItem(spacerItemControl, 7, 0, 1, 1)

        self.ipInputLabel = QLabel(self)
        sizePolicyForInputLabel = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicyForInputLabel.setHorizontalStretch(0)
        sizePolicyForInputLabel.setVerticalStretch(0)
        sizePolicyForInputLabel.setHeightForWidth(self.ipInputLabel.sizePolicy().hasHeightForWidth())
        self.ipInputLabel.setSizePolicy(sizePolicyForInputLabel)
        self.ipInputLabel.setMinimumSize(QSize(0, 40))
        self.ipInputLabel.setAlignment(Qt.AlignCenter)
        self.ipInputLabel.setObjectName("label")
        self.ipInputLabel.setText("热像仪对应IP地址：")
        self.gridLayoutControl.addWidget(self.ipInputLabel, 1, 0, 1, 1)

        self.ipInputLine = QLineEdit(self)
        # self.ipInputLine.setText('192.168.1.14')
        self.ipInputLine.setText('192.168.1.5')
        sizePolicyForInputLine = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicyForInputLine.setHorizontalStretch(0)
        sizePolicyForInputLine.setVerticalStretch(0)
        sizePolicyForInputLine.setHeightForWidth(self.ipInputLine.sizePolicy().hasHeightForWidth())
        self.ipInputLine.setSizePolicy(sizePolicyForInputLine)
        self.ipInputLine.setMinimumSize(QSize(0, 30))
        self.ipInputLine.setAlignment(Qt.AlignCenter)
        self.ipInputLine.setObjectName("lineEdit")
        self.gridLayoutControl.addWidget(self.ipInputLine, 1, 1, 1, 1)

        self.horizontalLayoutControl.addLayout(self.gridLayoutControl)
        self.gridLayoutVideo.addLayout(self.horizontalLayoutControl, 0, 1, 1, 1)

        self.__videoPanel = VideoPanel(self)
        self.__videoPanel.setObjectName("videopanel")
        sizePolicyForVideo = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicyForVideo.setHorizontalStretch(0)
        sizePolicyForVideo.setVerticalStretch(0)
        sizePolicyForVideo.setHeightForWidth(self.__videoPanel.sizePolicy().hasHeightForWidth())
        self.__videoPanel.setSizePolicy(sizePolicyForVideo)
        self.__videoPanel.setMinimumSize(QSize(640, 480))
        self.__videoPanel.setObjectName("__videoPanel")

        self.gridLayoutVideo.addWidget(self.__videoPanel, 0, 0, 1, 1)
        self.gridLayoutUI.addLayout(self.gridLayoutVideo, 0, 0, 1, 1)

        
    def onButtonLink(self):
        ip = socket.inet_aton(self.ipInputLine.text())
        if self.__videoPanel.link(int.from_bytes(ip, byteorder='little', signed=False)):
            self.__dislinkButton.setEnabled(True)
            self.__playButton.setEnabled(True)
            self.__linkButton.setEnabled(False)
            
        
    def onButtonStartPlay(self):
        if self.__videoPanel.startPlay():
            self.__stopButton.setEnabled(True)
            self.__playButton.setEnabled(False)
            
        
    def onButtonStopPlay(self):
        self.__videoPanel.stopPlay()
        self.__playButton.setEnabled(True)
        self.__stopButton.setEnabled(False)

    def onButtonDislink(self):
        self.__videoPanel.dislink()
        self.__linkButton.setEnabled(True)
        self.__dislinkButton.setEnabled(False)
        self.__playButton.setEnabled(False)
        self.__stopButton.setEnabled(False)