import numpy as np
from PIL import Image

image1 = Image.open('t.jpg')
image2 = Image.open('B.png')

#====使用numpy的数组矩阵合并concatenate======

#image = np.concatenate([image1, image2],axis=1) #纵向连接=np.vstack((gray1, gray2))
#横向连接image = np.concatenate([gray1, gray2], axis=1)

#====使用pandas数据集处理的连接concat========

#df1 = pd.DataFrame(gray1)

#df2 = pd.DataFrame(gray2) # ndarray to dataframe
#df = pd.concat([df1, df2])  
#纵向连接,横向连接=pd.concat([df1, df2], axis=1)

#image = np.array(df) # dataframe to ndarray

#=============

img = Image.fromarray(np.uint8(image2))
img.save('image.png')
