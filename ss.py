#!-*- coding:utf-8 -*-
import chardet

f3 = open(file="WM紫卡表.json",mode='rb') # 以二进制模式读取文件
data = f3.read() # 获取文件内容
print(data)
f3.close() # 关闭文件

result = chardet.detect(data) # 检测文件内容
print(result) # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}