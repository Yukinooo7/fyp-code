import makeDir
import video_capture
import largerPictures

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def case(num):
    if num == 'a':
        largerPictures.compose_all_images()
    elif num == 'c':
        file_name = input('file_name =' )
        makeDir.mkDdir(file_name)
    elif num == 'v':
        video_capture.capture_video()
    elif num == 'q':
        print("quit")
        return 'q'

helpInfo = '''
提示-按键前需要选中当前画面显示的窗口

按键L： 九合一大图
按键M： 生成文件夹
按键V： 拍照程序
'''
print(helpInfo)

number = input("Input key: ")
while(True):
    if(case(number) == 'q'):
        break
    else:
        print(helpInfo)
        number = input("Input another key: ")