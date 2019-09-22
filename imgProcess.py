import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import re

def mkdir(path):
	folder = os.path.exists(path)

	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("new folder creates")
 
	else:
		print ("folder exists")

def images_process(img_path,img_name):
    files = os.listdir(img_path)

    for file_a in files:
        img = img_path+"\\"+file_a
        img_a = re.findall(r'(.+?)\.',file_a)[0]
        file_name = img_name+img_a
        mkdir(file_name)

        scaffold = cv2.imread(img,cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(scaffold,cv2.COLOR_BGR2GRAY)
        retval2, processed_auto = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
          # 图像腐蚀
        # 设置卷积核
        kernel_np = 3
        kernel = np.ones((kernel_np,kernel_np),np.uint8)
        times = 2
        # 图像腐蚀处理
        # cv2.imshow("origin",thresh)
        erosion = cv2.erode(processed_auto, kernel,iterations = 1)
        dilation = cv2.dilate(erosion,kernel,iterations= 1)
        #gaussian_blur = cv2.GaussianBlur(gray,(3,3),0)
        # canny_gaussian = cv2.Canny(gray,50,150)

        # cv2.imshow('a',scaffold)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # print(file_name)
        img_b = file_name+"\\"+file_a
        cv2.imwrite(img_b,scaffold)
        cv2.imwrite(file_name+"\\gray.jpg",gray)
        cv2.imwrite(file_name+"\\processed_auto.jpg",processed_auto)
        cv2.imwrite(file_name+"\\erosion.jpg",erosion)
        cv2.imwrite(file_name+"\\dilation.jpg",dilation)
        #cv2.imwrite(file_name+"\\gaussian_blur.jpg",gaussian_blur)
        # cv2.imwrite(file_name+'\\canny_gaussian.jpg',canny_gaussian)
        # print(file_a)
    print("processing complete")


img_path="C:\\Users\\cly\\Desktop\\60%2895V0.91um\\layer6"
file_name = "C:\\Users\\cly\\Desktop\\20190826\\"
images_process(img_path,file_name)

