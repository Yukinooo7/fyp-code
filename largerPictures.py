import PIL.Image as Image
import os
import cv2
import time
import re
 
# IMAGES_PATH = './pictures/scaffold/images/'  # 图片集地址
IMAGES_PATH = 'C:/Users/cly/Desktop/test/'
IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
IMAGE_SIZE = 256  # 每张小图片的大小
IMAGE_ROW = 3  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 3  # 图片间隔，也就是合并成一张图后，一共有几列
# IMAGE_SAVE_PATH = './pictures/scaffold/9_images/{}.jpg'.format(time.strftime("%d%H%M%S",time.localtime()))  # 图片转换后的地址
# img_name = "./pictures/"+variety+"/{}".format(time.strftime("%m%d",time.localtime()))+"/{}.jpg".format(time.strftime("%H%M%S",time.localtime()))
    
 

# image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
#                os.path.splitext(name)[1] == item]

# 定义图像拼接函数
def image_compose(file_path,image_save_path):
    # 获取图片集地址下的所有图片名称
    image_names = [name for name in os.listdir(file_path) for item in IMAGES_FORMAT if 
    os.path.splitext(name)[1] == item]

    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
        raise ValueError(file_path+"合成图片的参数和要求的数量不能匹配！")
    
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
    
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(file_path + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (IMAGE_SIZE, IMAGE_SIZE),Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
    # to_image.show()
    file_name = re.findall(r'layer+\d*',file_path)[0]
    to_image.save(image_save_path) # 保存新图
    print(file_name+' composite image has been saved')

def compose_all_images():
    files = os.listdir(IMAGES_PATH)
    for file in files:
        # print(file)
        file_path = IMAGES_PATH+file+'/'
        # print(file_path)
        # for pictures in file_a:
        # picture_path = file_path+pictures+'/'
        image_save_path = IMAGES_PATH+'overall/'+file+'.jpg'
        # print(image_save_path)
        if file != 'overall':
            image_compose(file_path,image_save_path)
        # for image in file_a:
        #     pictures = os.listdir(image)
        #     print(image)
        #     image_names = [name for name in os.listdir(pictures) for item in IMAGES_FORMAT if 
        #     os.path.splitext(name)[1] == item]
        #     image_save_path = 'C:/Users/cly/Desktop/'+file+'/composed.jpg'
        # image_compose(image_names,image_save_path)
                

# image_compose() #调用函数
if __name__ == "__main__":
    compose_all_images()