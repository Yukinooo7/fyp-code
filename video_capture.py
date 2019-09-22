import numpy as np
import cv2
import time
import re
import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
# import largerPictures as lp

# 新建文件夹
def mkdir(path):
	folder = os.path.exists(path)

	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("new folder creates")
 
	else:
		print ("folder exists")
# 保存格式以及保存位置，默认设为存在此py文件的同目录下，名称为当地时间月日时分秒毫秒（毫秒的前两位）
def capture_image(frame,variety):
    microsecond = datetime.datetime.now().strftime("%f")
    ms = re.findall(r'\d.',microsecond)[0]
    img_name = "./pictures/"+variety+"/{}".format(time.strftime("%m%d",time.localtime()))+"/{}.jpg".format(datetime.datetime.now().strftime("%H%M%S"+ms))
    cv2.imwrite(img_name,frame)
    print(variety+"_{}.jpg".format(datetime.datetime.now().strftime("%H%M%S"+ms))+" has been saved")

def capture_video():
## VideCapture里面的序号
# 0 : 默认为笔记本上的摄像头(如果有的话) / USB摄像头 webcam
# 1 : USB摄像头2
# 2 ：USB摄像头3 以此类推
# -1：代表最新插入的USB设备 

    #创建一个实例
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap1 = cv2.VideoCapture(2,cv2.CAP_DSHOW)
    c = 1
    print("if the camera is opened? {}".format(cap.isOpened()))

    ## 设置画面的尺寸

    # 画面宽度设为640
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    # 画面长度设为320
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
    # 设置一个名为images的窗口，窗口大小为画面大小
    cv2.namedWindow('Scaffold',cv2.WINDOW_AUTOSIZE)
    # CAP1
    # 画面宽度设为640
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    # 画面长度设为320
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
    # 设置一个名为images的窗口，窗口大小为画面大小
    cv2.namedWindow('TCone',cv2.WINDOW_AUTOSIZE)
    # 操作提醒
    helpInfo = '''
    提示-按键前需要选中当前画面显示的窗口

    按键Q： 退出程序
    按键A： 自动截图
    按键C： Capture 拍照
    '''
    print(helpInfo)
    # 新建日期文件夹
    scaffold_image_path = "./pictures/Scaffold/{}".format(time.strftime("%m%d",time.localtime()))
    tcone_image_path = "./pictures/TCone/{}".format(time.strftime("%m%d",time.localtime()))
    mkdir(scaffold_image_path)
    mkdir(tcone_image_path)
    # 视频帧计算间隔频率 调整times的数值，15以下（0.5s)
    times = 15
    # 逐帧获取摄像头画面
    while(True):
        #ret 为摄像头是否获取成功，如成功，则为True
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()
        # 若获取失败，则退出程序
        if not ret:
            print("Failed to get scream 1")
            break
        elif not ret1:
            print("Failed to get scream 2")
            break
        
        cv2.imshow('Scaffold',frame)
        cv2.imshow('TCone',frame1)
        key = cv2.waitKey(1)

        # 按q退出程序
        if key == ord('q'):
            print("-------------------------------------------------------")
            print("Video capture halts")
            break
        # 按a进入自动截图模式，每秒拍摄速率为30帧，截图时间设为60帧，也就是两秒一截图
        elif key == ord('a'):
            print("-------------------------------------------------------")
            print("Automatic capture starts")
            while ret:
                ret, frame = cap.read()
                ret, frame1 = cap1.read()
                cv2.imshow("Scaffold",frame)
                cv2.imshow("TCone",frame1)
                if(c%times == 0):
                    capture_image(frame1,"Tcone")
                    capture_image(frame,"scaffold")
                c = c + 1
                key_in = cv2.waitKey(1)

                # 按q退出程序
                if key_in == ord('q'):
                    print("-------------------------------------------------------")
                    print("Automatic capture halts")
                    break
                # 自动拍照过程中按C可以实现截图功能
                elif key_in == ord('c'):
                    capture_image(frame,"Scaffold")
                    capture_image(frame1,"TCone")
                    Scaffold_name = 'The captured scaffold image'
                    TCone_name = 'The captured taylor cone image'
                    cv2.imshow(Scaffold_name,frame)
                    cv2.imshow(Scaffold_name,frame)
                    print('Current image has been captured')
        # 按c截图保存并显示最后一张截图
        elif key == ord('c'):
            capture_image(frame,"Scaffold")
            capture_image(frame1,"TCone")
            img_name = 'The captured image'
            # img_name = "{}.jpg".format(time.strftime("%m%d%H%M",time.localtime()))
            # cv2.imwrite(img_name,frame)
            cv2.imshow(img_name,frame)
            # print("{}.jpg".format(time.strftime("%m%d%H%M",time.localtime()))+"has been saved")

        c = c + 1
    print("-------------------------------------------------------")
    print("Have a nice day")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()




