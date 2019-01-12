import numpy as np
from PIL import Image

threshold = 120

def getMatrix(n):
    ori_unit = np.zeros((n, n), int);
    r = (n + 1)/2
    for i in range(n):
        for j in range(n):
            if(((i - r)**2 + (j - r)**2)** 0.5 <=r):
                ori_unit[i][j] = 1
    return ori_unit

def getWhiteArray(shape):
    black_array = np.zeros(shape)
    white_array = black_array
    for i in range(black_array.shape[0]):
        for j in range(black_array.shape[1]):
            white_array[i][j] = 255
    return white_array

class ImageProcess:
    def __init__(self, threshold, img, unit_size):
        self.image = img
        self.unit = getMatrix(unit_size)
        self.convert(threshold)
        self.pad_size = int((unit_size - 1)/2)
        self.ori_array = np.asarray(self.binary)
        self.aim_array = getWhiteArray(self.ori_array.shape)
    
    def convert(self, threshold):
        lim = self.image.convert( 'L')
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        bim = lim.point(table, '1')
        self.binary = bim

    def erosion(self):
        self.pad_array = np.pad(self.ori_array,((self.pad_size, self.pad_size)),'constant')  
        for i in range(self.pad_array.shape[0]):
            if(i < self.pad_size or i >= self.pad_array.shape[0]-self.pad_size):
                continue
            for j in range(self.pad_array.shape[1]):
                if(j < self.pad_size or j >= self.pad_array.shape[1]-self.pad_size):
                    continue
                if(self.pad_array[i][j] >= 1):
                    continue
                covered = True
                for m in range(len(self.unit)):
                    for n in range(len(self.unit)):
                        if(self.unit[m][n] == 1 and self.pad_array[i-self.pad_size+m][j-self.pad_size+n] >= 1):
                            covered = False
                if(covered == True):
                    self.aim_array[i-self.pad_size][j-self.pad_size] = 0
        img = Image.fromarray(np.uint8(self.aim_array))
        img.save('erosion.jpg')
        
    def dilation(self):
        self.pad_array = np.pad(self.ori_array,((self.pad_size, self.pad_size)),'constant')  
        for i in range(self.pad_array.shape[0]):
            if(i < self.pad_size or i >= self.pad_array.shape[0]-self.pad_size):
                continue
            for j in range(self.pad_array.shape[1]):
                if(j < self.pad_size or j >= self.pad_array.shape[1]-self.pad_size):
                    continue
                if(self.pad_array[i][j] >= 1):
                    continue
                for m in range(len(self.unit)):
                    for n in range(len(self.unit)):
                        if(self.unit[m][n] == 1):
                            if(i-2*self.pad_size+m >= self.ori_array.shape[0] or j-2*self.pad_size+n >= self.ori_array.shape[1]):
                                continue
                            self.aim_array[i-2*self.pad_size+m][j-2*self.pad_size+n] = 0
        img = Image.fromarray(np.uint8(self.aim_array))
        img.save('dilastion.jpg')

    def open(self):
        self.erosion()
        self.ori_array = self.aim_array
        self.dilation()
        img = Image.fromarray(np.uint8(self.aim_array))
        img.save('open.jpg')

    def close(self):
        self.dilation()
        self.ori_array = self.aim_array
        self.erosion()
        img = Image.fromarray(np.uint8(self.aim_array))
        img.save('close.jpg')

def process():
    try:
        image_path = input("请输入图片路径：\n")
        unit_size_str = input("请输入单元大小：\n")
        process_choice = input("请选择进行膨胀/腐蚀操作（输入1）或者开/闭操作（输入2）：\n")
        unit_size = int(unit_size_str)
        image = Image.open(image_path)
    except FileNotFoundError:
        print("Error：图片不存在\n")
        process()
    except ValueError:
        print("Error：单元大小/操作选择必须为数字\n")
        process()
    else:
        process_choice = int(process_choice)
        if(process_choice != 1 and process_choice != 2):
            print("Error：操作选择必须为1/2\n")
            process()
        imageProcess = ImageProcess(threshold, image, unit_size)
        print("读取成功，图像处理中……\n")
        if(process_choice == 1):
            imageProcess.erosion()
            print("腐蚀操作成功完成，结果图像已保存\n")
            imageProcess.dilation()
            print("膨胀操作成功完成，结果图像已保存\n")
            process()
        if(process_choice == 2):
            imageProcess.open()
            print("开操作成功完成，结果图像已保存\n")
            imageProcess.close()
            print("闭操作成功完成，结果图像已保存\n")
            process()
    
def main():
    process()

main()
