import scipy
from glob import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random


class DataLoader():
    def __init__(self, dataset_name, img_res=(256, 256)):
        self.dataset_name = dataset_name
        self.img_res = img_res
        
    def load_logo(self):
        adidas = self.imread('./datasets/font/logo/adidas.jpg')
        adidas = scipy.misc.imresize(adidas, self.img_res)
        adidas = np.expand_dims(adidas, axis=2) 
        
        nike = self.imread('./datasets/font/logo/nike.jpg')
        nike = scipy.misc.imresize(nike, self.img_res)
        nike = np.expand_dims(nike, axis=2) 
        
        huawei = self.imread('./datasets/font/logo/huawei.jpg')
        huawei = scipy.misc.imresize(huawei, self.img_res)
        huawei = np.expand_dims(huawei, axis=2) 
        
        img_cont = self.imread('./datasets/font/BASE/Roman.png')
        h, w = img_cont.shape
        _w = int(w/26)
        
        imgs, adidas_, huawei_, nike_ = [], [], [], []
        for letter in range(26):
            cut = letter + 1
            img = img_cont[:, _w*letter:_w*cut]
            img = scipy.misc.imresize(img, self.img_res)
            img = np.expand_dims(img, axis=2) 
            
            imgs.append(img) 
            adidas_.append(adidas) 
            nike_.append(nike) 
            huawei_.append(huawei) 
            
        imgs = np.array(imgs)/127.5 - 1.
        adidas_ = np.array(adidas_)/127.5 - 1.
        nike_ = np.array(nike_)/127.5 - 1.
        huawei_ = np.array(huawei_)/127.5 - 1.
        
        return imgs, adidas_, huawei_, nike_ 
        
        
    def load_data(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "test"
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))

        batch_images = np.random.choice(path, size=batch_size)
        

        imgs_A = []
        imgs_B = []
        imgs_cycle = []
        imgs_Base = []
        
        for img_path in batch_images:
            img = self.imread(img_path)
            
            #载入基础字形         
            img_cont = self.imread('./datasets/%s/BASE/Roman.png'% (self.dataset_name))
            
            h, w = img.shape
            _w = int(w/26)
            
            #准备输入噪音img_A
            #随机截取一个字母作为logo
            rand = random.randint(0,25)
            rand_b = rand + 1
            img_A = img[:, _w*rand:_w*rand_b]
            img_cycle = img_cont[:, _w*rand:_w*rand_b]
            
            # If training => do random flip
            if not is_testing and np.random.random() > 0.5:
                img_A = np.flipud(img_A)
                img_cycle = np.flipud(img_cycle)
                
            #准备输出目标img_B 和 内容img_Base
            cont = random.randint(0,25)
            if cont == rand and cont < 25:
                cont += 1
            elif cont == rand :
                cont -= 1
            cont_b = cont + 1
            img_B = img[:, _w*cont:_w*cont_b]
            img_Base = img_cont[:, _w*cont:_w*cont_b]
            

            img_A = scipy.misc.imresize(img_A, self.img_res)
            img_B = scipy.misc.imresize(img_B, self.img_res)
            img_Base = scipy.misc.imresize(img_Base, self.img_res)
            img_cycle = scipy.misc.imresize(img_cycle, self.img_res)
            
            img_A = np.expand_dims(img_A, axis=2) 
            img_B = np.expand_dims(img_B, axis=2) 
            img_Base = np.expand_dims(img_Base, axis=2) 
            img_cycle = np.expand_dims(img_cycle, axis=2) 

            imgs_A.append(img_A)
            imgs_B.append(img_B)
            imgs_Base.append(img_Base)
            imgs_cycle.append(img_cycle)

        imgs_A = np.array(imgs_A)/127.5 - 1.
        imgs_B = np.array(imgs_B)/127.5 - 1.
        imgs_Base = np.array(imgs_Base)/127.5 - 1.
        imgs_cycle = np.array(imgs_cycle)/127.5 - 1.

        return imgs_A, imgs_B, imgs_Base, imgs_cycle

    def load_batch(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "val"
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))

        self.n_batches = int(len(path) / batch_size)

        img_back = self.imread('./datasets/%s/BASE/0.png'% (self.dataset_name))
        for i in range(self.n_batches-1):
            batch = path[i*batch_size:(i+1)*batch_size]
            
            #载入基础字形         
            img_cont = self.imread('./datasets/%s/BASE/Roman.png'% (self.dataset_name))
            
            imgs_A, imgs_B ,imgs_Base, imgs_cycle= [], [], [], []
            for img in batch:
                img = self.imread(img)
                
                h, w = img.shape
                cut_w = int(w/26)
                
                #随机截取一个字母作为输入img_A
                rand =  random.randint(0,25)
                rand_b = rand + 1
                img_A = img[:, cut_w*rand:cut_w*rand_b]
                img_cycle = img_cont[:, cut_w*rand:cut_w*rand_b]

                
                #通过随机翻转和添加噪音增大泛化性，弱化结构的影响
                if not is_testing and np.random.random() > 0.5:
                    img_A = np.flipud(img_A)
                    img_A = np.fliplr(img_A)
                    img_cycle = np.flipud(img_cycle)
                    img_cycle = np.fliplr(img_cycle)
                    
                if not is_testing and np.random.random() < 0.3:    #有一定概率双型相加                        
                    if rand >= 2:
                        rand_d = rand - 2
                        rand_u = rand - 1 
                        img_add = img[:, cut_w*rand_d:cut_w*rand_u]
                        img_A = np.add(img_A,img_add)
                        
                        img_cycadd = img_cont[:, cut_w*rand_d:cut_w*rand_u]
                        img_cycle = np.add(img_cycle,img_cycadd)
             
                    
                if not is_testing and np.random.random() > 0.7:
                    img_bg = img_back[:, cut_w*rand:cut_w*rand_b]
                    img_A = np.add(img_A,img_bg)
                    img_cycle = np.add(img_cycle,img_bg)
                    
                    
                #准备输出目标img_B 和 内容img_Base
                cont = random.randint(0,25)
                if cont == rand and cont < 25:
                    cont += 1
                elif cont == rand :
                    cont -= 1
                cont_b = cont + 1
                img_B = img[:, cut_w*cont:cut_w*cont_b]
                img_Base = img_cont[:, cut_w*cont:cut_w*cont_b]

                img_A = scipy.misc.imresize(img_A, self.img_res)
                img_B = scipy.misc.imresize(img_B, self.img_res)
                img_Base = scipy.misc.imresize(img_Base, self.img_res)
                img_cycle = scipy.misc.imresize(img_cycle, self.img_res)
                 
                img_A = np.expand_dims(img_A, axis=2) 
                img_B = np.expand_dims(img_B, axis=2) 
                img_cycle = np.expand_dims(img_cycle, axis=2) 
                img_Base = np.expand_dims(img_Base, axis=2) 

                imgs_A.append(img_A)
                imgs_B.append(img_B)
                imgs_Base.append(img_Base)
                imgs_cycle.append(img_cycle)
                

            imgs_A = np.array(imgs_A)/127.5 - 1.
            imgs_B = np.array(imgs_B)/127.5 - 1.
            imgs_Base = np.array(imgs_Base)/127.5 - 1.
            imgs_cycle = np.array(imgs_cycle)/127.5 - 1.

            yield imgs_A, imgs_B, imgs_Base, imgs_cycle 


    def imread(self, path):
        return scipy.misc.imread(path, mode='L').astype(np.float)
    
    
    #用逐个替换白点方式拼接图片
    def getWhiteArray(shape, n_high, n_wide):
        new_shape = np.asarray((shape[0] * n_high, shape[1] * n_wide,shape[2]))
        black_array = np.zeros(new_shape)
        white_array = black_array
        for i in range(black_array.shape[0]):
            for j in range(black_array.shape[1]):
                white_array[i][j] = 255
        return white_array
