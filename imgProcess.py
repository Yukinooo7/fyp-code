import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import re
import math


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

def get_image_entropy(img):
  tmp = []
  for i in range(256):
      tmp.append(0)
  val = 0
  k = 0
  res = 0
  # image = cv2.imread(img,0)
  imgg = np.array(img)
  for i in range(len(imgg)):
      for j in range(len(img[i])):
          val = imgg[i][j]
          tmp[val] = float(tmp[val] + 1)
          k =  float(k + 1)
  for i in range(len(tmp)):
      tmp[i] = float(tmp[i] / k)
  for i in range(len(tmp)):
      if(tmp[i] == 0):
          res = res
      else:
         res -= float(tmp[i] * np.log2(tmp[i]))

  return res

def get_entropy(image):
  entropy = []
  img = image
  hist = cv2.calcHist([img],[0],None,[256],[0,255])
  total_pixel = img.shape[0] * img.shape[1]

  for item in hist:
    probability = item / total_pixel
    if probability ==0:
      en = 0
    else:
      en = -1 * probability * (np.log2(probability))
    entropy.append(en)
  
  sum_en = np.sum(entropy)
  return sum_en

def incremental(layer_path):
  # img_a = layer_path+"\\134937.jpg"
  # image_a =cv2.imread(img_a,cv2.IMREAD_UNCHANGED)
  files = os.listdir(layer_path)
  ifFirst = True
  incremental_list=[]
  image_list = []
  for file in files:
    if ifFirst:
      file_image=cv2.imread(layer_path+"\\"+file,cv2.IMREAD_UNCHANGED)
      prev = np.zeros(file_image.shape,np.uint8)
      incremental_part = cv2.subtract(file_image,prev)
      # incremental_list.append(incremental_part)
      # value = get_entropy(incremental_part)
      # incremental_list.append(value[0])
      prev = file_image
      ifFirst = False
    else:
      file_image=cv2.imread(layer_path+"\\"+file,cv2.IMREAD_UNCHANGED)
      incremental_part = cv2.subtract(file_image,prev)
      prev = file_image
      image_list.append(incremental_part)
      value = get_entropy(incremental_part)
      incremental_list.append(value[0])
  # for image in image_list:
  #     cv2.imshow("image",image)
  #     cv2.waitKey()
  #     cv2.destroyAllWindows()
  y = incremental_list
  size = len(incremental_list)
  layer_list = []
  for i in range(size):
    layer_list.append(i)
  # print(layer_list)
  x  = layer_list

  plt.figure()
  plt.plot(x,y)
  plt.xlabel("Incremental Layer")
  plt.ylabel("Entropy")
  plt.title("Incremental entropy of each two layers")
  plt.savefig(layer_path+"\\incremental_result.jpg")
  plt.show()


def drawContour(url):
    img = cv2.imread(url)

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图处理
    ret, thresh = cv2.threshold(imgray, 100, 255, 0)  # 二值化处理，参数需要调整
    '''
    cv2.findContours(image, mode, method[, contours[, hierarchy[, offset ]]])

    第一个参数是寻找轮廓的图像；

    第二个参数表示轮廓的检索模式，有四种（本文介绍的都是新的cv2接口）：
        cv2.RETR_EXTERNAL表示只检测外轮廓
        cv2.RETR_LIST检测的轮廓不建立等级关系
        cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
        cv2.RETR_TREE建立一个等级树结构的轮廓。

    第三个参数method为轮廓的近似办法
        cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
        cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
        cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
    '''

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_NONE)
    '''
    返回值：
    (OpenCV 3版本会返回3个值)

    1. Binary: 不知道
    2. Contours：Numpy列表，存着所有的contours，需要用循环读取所有的contour
    3. Hierarchy：轮廓的层次结构，基本不用
    '''
    
    # 获取面积
    # Cycle through contours and add area to array
    areas = []
    for c in contours:
        areas.append(cv2.contourArea(c))
    # print(areas)
    # 参数一：需要排序的数组
    # 参数二：排序规则，根据x的相对应的面积进行排序，输入x，返回x的面积
    # 参数三：顺序还是反序
    sortedContors = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    # (image to draw, contours(一个NP数组), 第几个contour, color, thickness)
    # for i in range(1):
    #     cv2.drawContours(img, sortedContors, i, (0, 255 - (2 * i), 0), 5) 

    # cv2.imshow('Image', img)
    # cv2.imshow('Gray', thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return sortedContors

if __name__ == "__main__":
  img_path="C:\\Users\\cly\\Desktop\\60%2741V0.71um\\layer12"
  file_name = "C:\\Users\\cly\\Desktop\\test\\"
  # images_process(img_path,file_name)
  image_path = 'C:\\Users\\cly\\Desktop\\test\\th\\gray.jpg'
  # imggg = './pictures/Scaffold/0927'
  imggg = '../24layers/60%2.35kV1.60um0.3mm'
  # imgggg= imggg+'/15031913.jpg'
  # print(drawContour(imgggg))
  files = os.listdir(imggg)
  for file_a in files:
      img = imggg+"/"+file_a
      # print(drawContour(img))
      # if(drawContour(img)<70):
      #   if(drawContour(img)>50):
      # print(drawContour(img))
      # print(drawContour(img)[0])
      # show_image = cv2.imread(img)
      # cv2.imshow('a',show_image)
      # cv2.waitKey()
      # cv2.destroyAllWindows()
  # print(get_entropy(image_path))
  # print(get_image_entropy(image_path))
  layer_path = "C:\\Users\\cly\\Desktop\\24layers\\1011\\2342V1.60"
  incremental(layer_path)

