import MagSDK
import ctypes
from ctypes import *

MAX_CHANNELINDEX = 128
STREAM_TEMPERATURE = 2

class MagDevice(object):
	def __init__(self):
		self.__initialized = False
		self.__channelIndex = -1
		self.__recordingAvi = False
		self.__recordingMGS = False
		self.__recordingLocalAvi = False
		self.__camIPAddr = 0
		self.__camInfo = MagSDK.CamInfo()
		self.__regContent = MagSDK.CeRegContent()
		self.__camInfoEx = MagSDK.CamInfoEx()

	def Initialize(self):
		if self.__initialized:
			return True

		if (self.__channelIndex<=0 or self.__channelIndex>MAX_CHANNELINDEX):
			for i in range(1, MAX_CHANNELINDEX + 1):
				if not MagSDK.IsChannelAvailable(i):
					bSuccess = MagSDK.NewChannel(i)
					self.__channelIndex = i
					break

		if (self.__channelIndex>0 and self.__channelIndex<=MAX_CHANNELINDEX and MagSDK.IsLanConnected()):
			self.__initialized = MagSDK.Initialize(self.__channelIndex, None)

		return self.__initialized

	def Deinitialize(self):
		if MagSDK.IsInitialized(self.__channelIndex):
			MagSDK.Free(self.__channelIndex)
			self.__initialized = False

		if MagSDK.IsChannelAvailable(self.__channelIndex):
			MagSDK.DelChannel(self.__channelIndex)
			self.__channelIndex = -1


	def IsInitialized(self):
		return MagSDK.IsInitialized(self.__channelIndex)

	def IsLinked(self):
		return MagSDK.IsLinked(self.__channelIndex)

	def LinkCamera(self, intIP, intTimeoutMS):
		if not self.Initialize():
			return False

		if MagSDK.LinkCamera(self.__channelIndex, intIP, intTimeoutMS):
			self.__camIPAddr = intIP
			MagSDK.GetCamInfo(self.__channelIndex, byref(self.__camInfo), sizeof(self.__camInfo))
			MagSDK.ReadCameraRegContent(self.__channelIndex, byref(self.__regContent), MagSDK.DEFAULT_TIMEOUT, False)
			return True
		else:
			return False

	def LinkCameraEx(self, intIP, shortCmdPort, shortImgPort, charCloudUser, charCloudPwd, intCamSN, charCamUser, charCamPwd, intTimeoutMS):
		if not self.Initialize():
			return False

		if MagSDK.LinkCameraEx(self.__channelIndex, intIP, shortCmdPort, shortImgPort, charCloudUser, charCloudPwd, intCamSN, charCamUser, charCamPwd, intTimeoutMS):
			self.__camIPAddr = intIP
			MagSDK.GetCamInfo(self.__channelIndex, byref(self.__camInfo), sizeof(self.__camInfo))
			MagSDK.ReadCameraRegContent(self.__channelIndex, byref(self.__regContent), MagSDK.DEFAULT_TIMEOUT, False)
			return True
		else:
			return False

	def DisLinkCamera(self):
		if self.__recordingMGS:
			self.SDCardStorage(MagSDK.SDStorageFileType.SDFileMGS.value, 0)

		if self.__recordingAvi:
			self.SDCardStorage(MagSDK.SDStorageFileType.SDFileAVI.value, 0)

		self.__camIPAddr = 0
		MagSDK.DisLinkCamera(self.__channelIndex)
		self.Deinitialize()

	def GetCamInfo(self):
		return self.__camInfo

	def GetCamInfoEx(self):
		MagSDK.GetCamInfoEx(self.__channelIndex, byref(self.__camInfoEx), sizeof(self.__camInfoEx))
		return self.__camInfoEx

	def GetRecentHeartBeat(self):
		return MagSDK.GetRecentHeartBeat(self.__channelIndex)

	def SetReConnectCallBack(self, pCallBack, pUserData):
		return MagSDK.SetReConnectCallBack(self.__channelIndex, pCallBack, pUserData)

	def ResetCamera(self):
		if self.__recordingMGS:
			self.SDCardStorage(MagSDK.SDStorageFileType.SDFileMGS.value, 0)

		if self.__recordingAvi:
			self.SDCardStorage(MagSDK.SDStorageFileType.SDFileAVI.value, 0)

		if MagSDK.ResetCamera(self.__channelIndex):
			self.__initialized = False
			self.__channelIndex = -1

			return True
		else:
			return False

	def TriggerFFC(self):
		return MagSDK.TriggerFFC(self.__channelIndex)

	def AutoFocus(self):
		return MagSDK.SetPTZCmd(self.__channelIndex, MagSDK.PTZCmd.PTZFocusAuto.value, 0)

	def SetIoAlarmState(self, bAlarm):
		return MagSDK.SetIoAlarmState(self.__channelIndex, bAlarm)

	def SetPTZCmd(self, cmd, dwPara):
		return MagSDK.SetPTZCmd(self.__channelIndex, cmd, dwPara)

	def QueryPTZState(self, query, intValue, intTimeoutMS):
		return MagSDK.QueryPTZState(self.__channelIndex, query, intValue, intTimeoutMS)

	def SetSerialCmd(self, buff, intBufferLen):
		return MagSDK.SetSerialCmd(self.__channelIndex, buff, intBufferLen)

	def SetSerialCallBack(self, pCallBack, pUserData):
		return MagSDK.SetSerialCallBack(self.__channelIndex, pCallBack, pUserData)

	def GetCameraTemperature(self, intT, intTimeoutMS):
		return MagSDK.GetCameraTemperature(self.__channelIndex, intT, intTimeoutMS)

	def SetCameraRegContent(self, pContent):
		if not MagSDK.SetCameraRegContent(self.__channelIndex, pContent):
			MagSDK.ReadCameraRegContent(self.__channelIndex, byref(self.__regContent), MagSDK.DEFAULT_TIMEOUT, False)
			return True
		else:
			return False

	def ReadCameraRegContent2(self, pContent, intTimeoutM):
		return MagSDK.ReadCameraRegContent2(self.__channelIndex, pContent, intTimeoutM)

	def SetCameraRegContent2(self, pContent):
		return MagSDK.SetCameraRegContent2(self.__channelIndex, pContent)

	def SetUserROIs(self, pROI):
		return MagSDK.SetUserROIs(self.__channelIndex, pROI)

	def SetUserROIsEx(self, pROIs, intROINum):
		return MagSDK.SetUserROIsEx(self.__channelIndex, pROIs, intROINum)

	def SetROIReportCallBack(self, pCallBack, pUserData):
		return MagSDK.SetROIReportCallBack(self.__channelIndex, pCallBack, pUserData)

	def SetIrregularROIReportCallBack(self, pCallBack, pUserData):
		return MagSDK.SetIrregularROIReportCallBack(self.__channelIndex, pCallBack, pUserData)

	def SetIrregularROIReportExCallBack(self, pCallBack, pUserData):
		return MagSDK.SetIrregularROIReportExCallBack(self.__channelIndex, pCallBack, pUserData)

	def IsProcessingImage(self):
		return MagSDK.IsProcessingImage(self.__channelIndex)

	def StartProcessImage(self, paraOut, funcFrame, dwStreamType, pUserData):
		return MagSDK.StartProcessImage(self.__channelIndex, paraOut, funcFrame, dwStreamType, pUserData)

	def StartProcessPulseImage(self, paraOut, funcFrame, dwStreamType, pUserData):
		return MagSDK.StartProcessPulseImage(self.__channelIndex, paraOut, funcFrame, dwStreamType, pUserData)

	def TransferPulseImage(self):
		return MagSDK.TransferPulseImage(self.__channelIndex)

	def StopProcessImage(self):
		if self.__recordingLocalAvi:
			self.LocalStorageAviStop()

		return MagSDK.StopProcessImage(self.__channelIndex)

	def SetColorPalette(self, ColorPaletteIndex):
		return MagSDK.SetColorPalette(self.__channelIndex, ColorPaletteIndex)

	def SetSubsectionEnlargePara(self, intX1, intX2, byteY1, byteY2):
		return MagSDK.SetSubsectionEnlargePara(self.__channelIndex, intX1, intX2, byteY1, byteY2)

	def SetIsothermalPara(self, intLowerLimit, intUpperLimit):
		return MagSDK.SetIsothermalPara(self.__channelIndex, intLowerLimit, intUpperLimit)

	def SetEnhancedROI(self, intChannelIndex, intEnhancedRatio, x0, y0, x1, y1):
		return MagSDK.SetEnhancedROI(self.__channelIndex, intEnhancedRatio, x0, y0, x1, y1)

	def SetAutoEnlargePara(self, dwAutoEnlargeRange, intBrightOffset, intContrastOffset):
		return MagSDK.SetAutoEnlargePara(self.__channelIndex, dwAutoEnlargeRange, intBrightOffset, intContrastOffset)

	def SetEXLevel(self, ExLevel, intCenterX, intCenterY):
		return MagSDK.SetEXLevel(self.__channelIndex, ExLevel, intCenterX, intCenterY)

	def GetEXLevel(self):
		return MagSDK.GetEXLevel(self.__channelIndex)

	def SetDetailEnhancement(self, intDDE, bQuickDDE):
		return MagSDK.SetDetailEnhancement(self.__channelIndex, intDDE, bQuickDDE)

	def SetVideoContrast(self, intContrastOffset):
		return MagSDK.SetVideoContrast(self.__channelIndex, intContrastOffset)

	def SetVideoBrightness(self, intBrightnessOffset):
		return MagSDK.SetVideoBrightness(self.__channelIndex, intBrightnessOffset)

	def GetFixPara(self, pPara):
		return MagSDK.GetFixPara(self.__channelIndex, pPara)

	def SetFixPara(self, pPara, FixOption):
		return MagSDK.SetFixPara(self.__channelIndex, pPara, FixOption)

	def FixTemperature(self, intT, fEmissivity, dwPosX, dwPosY):
		return MagSDK.FixTemperature(self.__channelIndex, intT, fEmissivity, dwPosX, dwPosY)

	def GetFilteredRaw(self):
		return MagSDK.GetFilteredRaw(self.__channelIndex)

	def GetOutputBMPData(self, pData, pInfo):
		return MagSDK.GetOutputBMPdata(self.__channelIndex, pData, pInfo)

	def GetApproximateGray2TemperatureLUT(self, pLut, intBufferSize):
		return MagSDK.GetApproximateGray2TemperatureLUT(self.__channelIndex, pLut, intBufferSize)

	def GetOutputBMPData_copy(self, pBmp, intBufferSize):
		return MagSDK.GetOutputBMPdata_copy(self.__channelIndex, pBmp, intBufferSize)

	def GetOutputBMPdataRGB24(self, pBmp, intBufferSize, bOrderBGR):
		return MagSDK.GetOutputBMPdataRGB24(self.__channelIndex, pBmp, intBufferSize, bOrderBGR)

	def GetOutputColorBarData(self, pData, pInfo):
		return MagSDK.GetOutputColorBardata(self.__channelIndex, pData, pInfo)

	def GetOutputColorBarData_copy(self, pColorBar, intBufferSize):
		return MagSDK.GetOutputColorBardata_copy(self.__channelIndex, pColorBar, intBufferSize)

	def GetOutputVideoData(self, pData, pInfo):
		return MagSDK.GetOutputVideoData(self.__channelIndex, pData, pInfo)

	def GetOutputVideoData_copy(self, pBmp, intBufferSize):
		return MagSDK.GetOutputVideoData_copy(self.__channelIndex, pBmp, intBufferSize)

	def GetOutputVideoYV12(self):
		return MagSDK.GetOutputVideoYV12(self.__channelIndex)

	def GetFrameStatisticalData(self):
		return MagSDK.GetFrameStatisticalData(self.__channelIndex)

	def GetTemperatureData(self, pData, intBufferSize, bEnableExtCorrect):
		return MagSDK.GetTemperatureData(self.__channelIndex, pData, intBufferSize, bEnableExtCorrect)

	def GetTemperatureData_Raw(self, pData, intBufferSize, bEnableExtCorrect):
		return MagSDK.GetTemperatureData_Raw(self.__channelIndex, pData, intBufferSize, bEnableExtCorrect)

	def GetTemperatureProbe(self, dwPosX, dwPosY, intSize):
		return MagSDK.GetTemperatureProbe(self.__channelIndex, dwPosX, dwPosY, intSize)

	def GetLineTemperatureInfo(self, buff, intBufferSizeByte, info, x0, y0, x1, y1):
		return MagSDK.GetLineTemperatureInfo(self.__channelIndex, buff, intBufferSizeByte, info, x0, y0, x1, y1)

	def GetRectTemperatureInfo(self, x0, y0, x1, y1, info):
		return MagSDK.GetRectTemperatureInfo(self.__channelIndex, x0, y0, x1, y1, info)

	def GetEllipseTemperatureInfo(self, x0, y0, x1, y1, info):
		return MagSDK.etEllipseTemperatureInfo(self.__channelIndex, x0, y0, x1, y1, info)

	def GetRgnTemperatureInfo(self, Pos, intPosNumber, info):
		return MagSDK.GetRgnTemperatureInfo(self.__channelIndex, Pos, intPosNumber, info)

	def UseTemperatureMask(self, bUse):
		return MagSDK.UseTemperatureMask(self.__channelIndex, bUse)

	def IsUsingTemperatureMask(self):
		return MagSDK.IsUsingTemperatureMask(self.__channelIndex)

	def SaveBMP(self, dwIndex, charFilename):
		return MagSDK.SaveBMP(self.__channelIndex, dwIndex, charFilename)

	def SaveMGT(self, charFilename):
		return MagSDK.SaveMGT(self.__channelIndex, charFilename)

	def SaveDDT(self, charFilename):
		return MagSDK.SaveDDT(self.__channelIndex, charFilename)

	def SaveFIR(self, charFilename):
		return MagSDK.SaveFIR(self.__channelIndex, charFilename)

	def SaveDDT2Buffer(self, pBuffer, intBufferSize):
		return MagSDK.SaveDDT2Buffer(self.__channelIndex, pBuffer, intBufferSize)

	def LoadDDT(self, paraOut, charFilename, funcFrame, pUserData):
		if not MagSDK.IsProcessingImage(self.__channelIndex):
			if not MagSDK.LoadDDT(self.__channelIndex, paraOut, charFilename, funcFrame, pUserData):
				print(charFilename)
				return False

			MagSDK.GetCamInfo(self.__channelIndex, byref(self.__camInfo), sizeof(self.__camInfo))
			return True
		else:
			return False

	def LoadFIR(self, paraOut, charFilename, funcFrame, pUserData):
		if not MagSDK.IsProcessingImage(self.__channelIndex):
			if not MagSDK.LoadFIR(self.__channelIndex, paraOut, charFilename, funcFrame, pUserData):
				print(charFilename)
				return False

			MagSDK.GetCamInfo(self.__channelIndex, byref(self.__camInfo), sizeof(self.__camInfo))
			return True
		else:
			return False

	def LoadBufferedDDT(self, paraOut, pBuffer, intBufferSize, funcFrame, pUserData):
		if not MagSDK.IsProcessingImage(self.__channelIndex):
			if not MagSDK.LoadBufferedDDT(self.__channelIndex, paraOut, pBuffer, intBufferSize, funcFrame, pUserData):
				return False

			MagSDK.GetCamInfo(self.__channelIndex, byref(self.__camInfo), sizeof(self.__camInfo))
			return True
		else:
			return False

	def SetAsyncCompressCallBack(self, pCallBack, intQuality):
		return MagSDK.SetAsyncCompressCallBack(self.__channelIndex, pCallBack, intQuality)

	def GrabAndAsyncCompressDDT(self, pUserData):
		return MagSDK.GrabAndAsyncCompressDDT(self.__channelIndex, pUserData)

	def SDCardStorage(self, filetype, para):
		bReturn = MagSDK.SDCardStorage(self.__channelIndex, filetype, para)

		if bReturn and filetype == MagSDK.SDStorageFileType.SDFileMGS.value:
			if para == 1:
				self.__recordingMGS = True
			else:
				self.__recordingMGS = False

		if bReturn and filetype == MagSDK.SDStorageFileType.SDFileAVI.value:
			if para == 1:
				self.__recordingAvi = True
			else:
				self.__recordingAvi = False

		return bReturn

	def SDStorageMGT(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileMGT.value, 0)

	def SDStorageBMP(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileBMP.value, 0)

	def SDStorageDDT(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileDDT.value, 0)

	def SDStorageMGSStart(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileMGS.value, 1)

	def SDStorageMGSStop(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileMGS.value, 0)

	def SDStorageAviStart(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileAVI.value, 1)

	def SDStorageAviStop(self):
		return MagSDK.SDCardStorage(self.__channelIndex, MagSDK.SDStorageFileType.SDFileAVI.value, 0)

	def LocalStorageAviStart(self, charFilename, intSamplePeriod):
		self.__recordingLocalAvi = self.__recordingLocalAvi or MagSDK.LocalStorageAviStart(self.__channelIndex, charFilename, intSamplePeriod)
		return self.__recordingLocalAvi

	def LocalStorageAviStop(self):
		MagSDK.LocalStorageAviStop(self.__channelIndex)
		self.__recordingLocalAvi = False

	def Lock(self):
		return MagSDK.LockFrame(self.__channelIndex)

	def Unlock(self):
		return MagSDK.UnLockFrame(self.__channelIndex)

	# 使用二元数组
	def ConvertPos2XY(self, intPos):
		W = self.__camInfo.intFPAWidth
		if W:
			Y = intPos // W
			X = intPos - Y * W

		return (X, Y)

	def ConvertXY2Pos(self, X, Y):
		return (Y * self.__camInfo.intFPAWidth + X)
