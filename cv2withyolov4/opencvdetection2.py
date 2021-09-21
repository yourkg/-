import cv2 as cv
import numpy as np
import os
import area


def onMouse(event, x, y, flags, param):
    img2 = param[0].copy()
    if event == cv.EVENT_LBUTTONDOWN:  # 左键点击，选择点
        param.append((x, y))

    if len(param) >= 2 and event == cv.EVENT_RBUTTONDOWN:  # 右键点击，取消最近一次选择的点
        param.pop()
    
    if len(param) > 1:
       cv.circle(img2, param[-1], 3, (0, 0, 255), -1)
    if len(param) > 2:
        # print(pts)
        # 画线
        for i in range(1,len(param) - 1):
            cv.circle(img2, param[i], 5, (0, 0, 255), -1)  # x ,y 为鼠标点击地方的坐标
            cv.line(img2, pt1=param[i], pt2=param[i + 1], color=(255, 0, 0), thickness=2)
    cv.imshow("get_rect",img2)

        

def get_rect(param,title):
    
    cv.namedWindow(title)
    # cv.moveWindow(title, 100, 100)

    cv.setMouseCallback(title, onMouse,param)


def image_detection(image_path_list):    
    for image_path in image_path_list:
        image = cv.imread(image_path)
        h = image.shape[0]
        w = image.shape[1]
        indices,t,boxes,confidences,classIds = model_output(image,h,w)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            cv.rectangle(image, (left, top), (left+width, top+height), (0, 0, 255), 2, 8, 0)
            cv.putText(image, classes[classIds[i]], (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv.putText(image, str(round(confidences[i],2)), (left+50, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        # c = cv.waitKey(1)
        # if c == 27:
        #     break
        # cv.namedWindow('YOLOv3-Detection-Demo', 0);
        # cv.resizeWindow('YOLOv3-Detection-Demo', int(w * 0.5), int(h*0.5))       
        # cv.imshow('YOLOv3-Detection-Demo', image)
        # cv.waitKey(0)
        # cv.destroyWindow(image_path)
        filename = os.path.basename(image_path) #得到路径中的文件名
        xin_image = os.path.join(image_new_floder,filename)
        cv.imwrite(xin_image, image)
        print("ok")


def video_detection(video_path,skipFrame=1):
    c = 1
    capture = cv.VideoCapture(video_path)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    fourcc = cv.VideoWriter_fourcc(*"MJPG")
    writer = cv.VideoWriter("output.avi", fourcc=fourcc, fps=15., frameSize=(int(width), int(height)))

    while True:
        ret, image = capture.read()
        if ret is False:
            break
        if(c == skipFrame):
            print(image)
            param = [image]
            cv.imshow('get_rect', param[0])
            get_rect(param, title='get_rect')  # 鼠标画矩形框
            cv.waitKey(0)
            cv.destroyAllWindows()
            print("param[1:]",param[1:])
         
        mask = np.zeros(image.shape, np.uint8)#掩膜
        points = np.array(param[1:], np.int32)

        points = points.reshape((-1, 1, 2))
        # 画多边形
        mask = cv.polylines(mask, [points], True, (255, 255, 255), 2)
        mask2 = cv.fillPoly(mask.copy(), [points], (255, 255, 255))  # 用于求 ROI
        mask3 = cv.fillPoly(mask.copy(), [points], (0, 255, 0))  # 用于显示在桌面的图像
        show_image = cv.addWeighted(src1=image, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

        #cv2.imshow("mask", mask2)
        # cv.imshow("show_img", show_image)

        # ROI = cv2.bitwise_and(mask2, img)
        # cv2.imshow("ROI", ROI)
        

        c=2
        # image = cv.cvtColor(image , cv.COLOR_BGR2RGB)
        h, w = show_image.shape[:2]
        print(h,w)

        indices,t,boxes,confidences,classIds = model_output(show_image,h,w)
        # print("indices",indices)
        fps = 1000 / (t * 1000.0 / cv.getTickFrequency())
        label = 'FPS: %.2f' % fps
        cv.putText(show_image, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        # print("---------")
        # print(indices)
        for i in indices:

            i = i[0]
            if classIds[i] == 0:
                box = boxes[i]
                left = box[0]
                top = box[1]
                width = box[2]
                height = box[3]
                cv.rectangle(show_image, (left, top), (left+width, top+height), (0, 255, 0), 2, 8, 0)
                cv.putText(show_image, classes[classIds[i]], (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv.putText(show_image, str(round(confidences[i],2)), (left+50, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                #多边形相交的面积
                # print(param[1:])
                # print(min(param[1:])[0])
                # print(max(param[1:])[0])
                #根据多边形的定点判断哪些物体的框在范围内
                if (min(param[1:])[0]< (left+width) < max(param[1:])[0] or min(param[1:])[0] <left < max(param[1:])[0]) \
                and (min([i[1] for i in param[1:]])< (top+height) < max([i[1] for i in param[1:]]) or min([i[1] for i in param[1:]])< top < max([i[1] for i in param[1:]])):
                    ImShape=show_image.shape
                    # print("ImShape:",ImShape)
                    Polygon1= np.array([[[left, top], [left+width, top], [left+width, top+height], [left, top+height]]], dtype=np.int32)
                    Polygon2= np.array([[list(i) for i in param[1:]]], dtype=np.int32)
                    # print(Polygon2,Polygon2)
                    Im1 = area.DrawPolygon(ImShape, Polygon1, (255, 0, 0))
                    Im2 = area.DrawPolygon(ImShape, Polygon2, (0, 255, 0))

                    area_object = np.sum(np.greater(Im1, 0))
                    # cv.imshow('ColorPolygons', Im1 + Im2)#两个多边形的展示
                    IntersectArea,OverlapIm = area.Get2PolygonIntersectArea(ImShape, Polygon1, Polygon2)

                    print("IntersectArea:",IntersectArea)
                    IOU = IntersectArea/area_object
                    # print(IOU)
                    if IOU >= 0.2:
                        cv.rectangle(show_image, (left, top), (left+width, top+height), (0, 0, 255), 2, 8, 0)


            # if (top+height) < b[1]:
            #     object_tuple = (left, top)+(left+width, top+height)
            #     IOU = cal_iou(alarm_tuple,object_tuple)
            #     print("IOU:",IOU)
            #     if IOU >= 0.3:
            #         cv.rectangle(image, (left, top), (left+width, top+height), (0, 0, 255), 2, 8, 0)
        c = cv.waitKey(1)
        if c == 27:
            break
        cv.namedWindow('YOLOv4-Detection-Demo', 0);
        cv.resizeWindow('YOLOv4-Detection-Demo', int(w), int(h))
        cv.imshow('YOLOv4-Detection-Demo', show_image)
        writer.write(show_image)
    writer.release()
    capture.release()
    cv.destroyAllWindows()
    
def model_output(image,h,w):        
    # 基于多个Region层输出getUnconnectedOutLayersNames
    blobImage = cv.dnn.blobFromImage(image, 1.0/255.0, (416, 416), None, True, False);
    outNames = net.getUnconnectedOutLayersNames()
    net.setInput(blobImage)
    outs = net.forward(outNames)
    # # Put efficiency information.
    fps_t, _ = net.getPerfProfile()
    
   
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            # numbers are [center_x, center_y, width, height]
            if confidence > 0.1: 
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                width = int(detection[2] * w)
                height = int(detection[3] * h)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    return cv.dnn.NMSBoxes(boxes, confidences, 0.5 , 0.5),fps_t,boxes,confidences,classIds

if __name__ == '__main__':

    model_bin = "yolov4.weights"
    config_text = "yolov4.cfg"

    # Load names of classes
    classes = None
    with open("coco.names", 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    # load tensorflow model
    net = cv.dnn.readNetFromDarknet(config_text, model_bin)

    # 获得所有层名称与索引
    layerNames = net.getLayerNames()
    lastLayerId = net.getLayerId(layerNames[-1])
    lastLayer = net.getLayer(lastLayerId)
    # print(lastLayer.type)
    index = 0
    # 检测视频
    video_path="vtest.avi"
    video_detection(video_path)
    
    #检查图片
    # image_folder=r"F:\project\123"
    # image_new_floder = r"F:\project"
    # image_path_list = file_name(image_folder)
    # print(image_path_list)   
    # image_detection(image_path_list)
    
        


    