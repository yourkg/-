import os
import cv2
import numpy as np
 

def DrawPolygon(ImShape,Polygon,Color):
    Im = np.zeros(ImShape, np.uint8)
    try:
        cv2.fillPoly(Im, Polygon, Color)  # 只使用这个函数可能会出错，不知道为啥
    except:
        try:
            cv2.fillConvexPoly(Im, Polygon, Color)
        except:
            print('cant fill\n')
 
    return Im
 
 
def Get2PolygonIntersectArea(ImShape,Polygon1,Polygon2):
    Im1 =DrawPolygon(ImShape[:-1],Polygon1,122)#多边形1区域填充为122
    Im2 =DrawPolygon(ImShape[:-1], Polygon2, 133)#多边形2区域填充为133
    Im = Im1 + Im2
    print(Im is None)
    # if Im is not None:
    ret, OverlapIm = cv2.threshold(Im, 200, 255, cv2.THRESH_BINARY)#根据上面的填充值，因此新图像中的像素值为255就为重叠地方
    IntersectArea=np.sum(np.greater(OverlapIm, 0))#求取两个多边形交叠区域面积

    #下面使用opencv自带的函数求取一下，最为对比
    # contours, hierarchy = cv2.findContours(OverlapIm,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # contourArea=cv2.contourArea(contours[0])
    # print('contourArea={}\n'.format(contourArea))
    # perimeter = cv2.arcLength(contours[0], True)
    # print('contourPerimeter={}\n'.format(perimeter))
    # RealContourArea=contourArea+perimeter
    # print('RealContourArea={}\n'.format(RealContourArea))
    return IntersectArea,OverlapIm
 
 
# if __name__ == '__main__':
    
#     Polygon1= np.array([[[20, 20], [60, 20], [60, 60], [20, 60]]], dtype=np.int32) 
#     Polygon2= np.array([[[30, 30], [70, 30], [70, 70], [30, 70]]], dtype=np.int32)
#     ImShape=(200,200,3)
#     Im1 = DrawPolygon(ImShape, Polygon1, (255, 0, 0))
#     Im2 = DrawPolygon(ImShape, Polygon2, (0, 255, 0))
    
#     cv2.imshow('ColorPolygons', Im1 + Im2)#两个多边形的展示
 
#     IntersectArea,OverlapIm=Get2PolygonIntersectArea(ImShape, Polygon1, Polygon2)
#     print('IntersectArea={}\n'.format(IntersectArea))
#     cv2.imshow('OverlapIm', OverlapIm) # 两个多边形相交的面积展示
#     cv2.waitKey(0)
