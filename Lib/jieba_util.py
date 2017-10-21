# coding=UTF-8
import jieba
import os

class jieba_util(object):
    def __init__(self):
        print os.path.join(os.getcwd(), 'Lib', 'car_dict.text')
        self.car_series = {}
        for line in open(os.path.join(os.getcwd(),'Lib','car_dict.text')):
            line = line.replace("\n", "")
            arr = line.split(',')
            self.car_series[arr[0]] = arr[1]
        jieba.load_userdict(os.path.join(os.getcwd(),'Lib','car_series.text'))



    def getKeyWord(self,content):
        seg_list = jieba.lcut(content)
        for word in seg_list:
            word = word.encode('utf-8')
            if  self.car_series.has_key(word):
                word = self.car_series[word]
                break
            else:
                word = ''
        return word




