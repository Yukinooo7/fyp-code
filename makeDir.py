import os
# 新建文件夹
def mkdir(path):
	folder = os.path.exists(path)

	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("new folder creates")
 
	else:
		print ("folder exists")

def mkDdir(file_name):
	file_path = 'C:/Users/cly/Desktop/20190821/'
	for i in range(1,13):
		file_dir = file_path+file_name+'/layer'+str(i)
		mkdir(file_dir)
	overall = file_path+file_name+'/overall'
	mkdir(overall)

if __name__ == "__main__":
	file_path = 'C:/Users/cly/Desktop/20190821/'
	file_name = '60%2179V0.51um2.5mm'

	for i in range(1,13):
		file_dir = file_path+file_name+'/layer'+str(i)
		mkdir(file_dir)
	overall = file_path+file_name+'/overall'
	mkdir(overall)
