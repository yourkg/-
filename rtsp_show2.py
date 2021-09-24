import cv2
from detection_video import detection
from infraredvideo import Printimg
import numpy as np
import time
#cap = cv2.VideoCapture("rtsp://127.0.0.1:8554/test") #没密码
cap = cv2.VideoCapture("rtsp://192.168.1.60:554//camera1") #根据软件显示修改

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
while True:
    ret, frame = cap.read()
    # print(frame)   
    frameh, framew = frame.shape[0:2]
    y_s = 480/frameh
    x_s = 640/framew
    # # #cv2.INTER_CUBIC 是插值方法，一般默认为cv2.INTER_LINEAR
    suofanghou=cv2.resize(frame,None,fx= x_s,fy=y_s,interpolation=cv2.INTER_CUBIC)
    # print("frame.shape:",frame.shape)
    # print(frameh, framew)
    # frame,list1 = detection(suofanghou)
    infrare_frame = Printimg([])
    # print(infrare_frame)
    print("infrare_frame.shape:",infrare_frame.shape)
    print("infrare_frame.ndim:",infrare_frame.ndim)
    infrare_frameh, infrare_framew = infrare_frame.shape[0:2]
    print(infrare_frameh, infrare_framew)

       #定尺寸的缩放
    # height_s,width_s=suofanghou.shape[:2]
    # print("缩小：",height_s,width_s)
    cv2.imshow('suofanghou',suofanghou)
    # frameUp = np.hstack((suofanghou, infrare_frame))
    cv2.imshow("frame",infrare_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()

