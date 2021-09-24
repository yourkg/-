from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from MagDevice import MagDevice
from MagService import MagService

import ctypes

import MagSDK

import time

def NewFrame(channelIndex, cameraTemperature, ffcCounterdown, cameraState, streamType, userData):
    videoPanel = userData
    videoPanel.update()

# ==============================================================
class BITMAPINFOHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
    ('biSize', ctypes.c_uint),
    ('biWidth', ctypes.c_uint),
    ('biHeight', ctypes.c_uint),
    ('biPLanes', ctypes.c_ushort),
    ('biBitCount', ctypes.c_ushort),
    ('biCompression', ctypes.c_uint),
    ('biSizeImage', ctypes.c_uint),
    ('biXPelsPerMeter', ctypes.c_uint),
    ('biYPelsPerMeter', ctypes.c_uint),
    ('biClrUsed', ctypes.c_uint),
    ('biClrImportant', ctypes.c_uint)
    ]

# ==============================================================  



class VideoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__service = MagService()
        self.__device = MagDevice()
        self.__posX = 0
        self.__posY = 0
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        self.setMouseTracking(True)
        self.move(10, 10)


    def mouseMoveEvent(self, e):
        self.__posX = e.x()
        self.__posY = e.y()
        e.accept()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Arial", 13))

        irData = ctypes.POINTER(ctypes.c_ubyte)()
        irInfo = ctypes.POINTER(ctypes.c_ubyte)()
        isTemperatureStream = 0
        isVideoStream = 0
        image = None

        self.__device.Lock()

        isTemperatureStream = self.__device.GetOutputBMPData(irData, irInfo)
        if isTemperatureStream <= 0:
            isVideoStream = self.__device.GetOutputVideoData(irData, irInfo)
            if isVideoStream <= 0:
                self.__device.Unlock()
                return

        camInfo = self.__device.GetCamInfo()
        # construct image
        if isTemperatureStream:
            image = QImage(irData.contents, camInfo.intVideoWidth, camInfo.intVideoHeight, QImage.Format_Indexed8)
            offset = ctypes.sizeof(BITMAPINFOHEADER)
            colorTable = []
            for i in range(256):
                t = i * 4
                colorTable.append(qRgb(irInfo[offset + t + 2], irInfo[offset + t + 1], irInfo[offset + t]))
            image.setColorTable(colorTable)
        else: 
            dst = (ctypes.c_ubyte*(camInfo.intVideoWidth * camInfo.intVideoHeight * 3))()
            for i in range(camInfo.intVideoWidth * camInfo.intVideoHeight):
                j = i *3
                dst[j] = irData[j + 2]
                dst[j+1] = irData[j + 1]
                dst[j+2] = irData[j]

            image = QImage(dst, camInfo.intVideoWidth, camInfo.intVideoHeight, QImage.Format_RGB888)

        # get temperature
        fpaX = int(self.__posX * camInfo.intFPAWidth / self.width())
        fpaY = int((self.height()-1-self.__posY) * camInfo.intFPAHeight / self.height())
        temp = self.__device.GetTemperatureProbe(fpaX, fpaY, 1)
        # fix temperature
        para = MagSDK.FixPara()
        self.__device.GetFixPara(para)
        temp = self.__device.FixTemperature(temp, para.fEmissivity, fpaX, fpaY)

        self.__device.Unlock()

        painter.drawImage(0, 0, image.mirrored(False, True).scaled(self.size(), Qt.KeepAspectRatio));
        painter.drawText(self.__posX, self.__posY, str(('%.1f' % (temp*0.001))))


    def link(self, ip):
        if self.__device.IsLinked():
            return True
        if self.__device.LinkCamera(ip, 2000):
            return True
        else:
            return False


    def startService(self):
        self.__service.Initialize()
        self.__service.EnableAutoReConnect(True)


    def stopService(self):
        self.__service.EnableAutoReConnect(False)
        self.__service.Deinitialize()

        
    def startPlay(self):
        if self.__device.IsProcessingImage():
            return True
        camInfo = self.__device.GetCamInfo()
        para = MagSDK.OutputPara()
        para.dwFPAWidth = camInfo.intFPAWidth
        para.dwFPAHeight = camInfo.intFPAHeight
        para.dwBMPWidth = camInfo.intVideoWidth
        para.dwBMPHeight = camInfo.intVideoHeight
        para.dwColorBarWidth = 16
        para.dwColorBarHeight = camInfo.intVideoHeight
        self.newFrameCallback = MagSDK.MAG_FRAMECALLBACK(NewFrame)
        if self.__device.StartProcessImage(para,  self.newFrameCallback,  MagSDK.STREAM_TEMPERATURE, ctypes.py_object(self)):
            self.__device.SetColorPalette(MagSDK.ColorPalette.IronBow.value)
            return True
        else:
            return False

        
    def stopPlay(self):
        if self.__device.IsProcessingImage():
            self.__device.StopProcessImage()


    def dislink(self):
        if self.__device.IsLinked():
            self.__device.DisLinkCamera()
