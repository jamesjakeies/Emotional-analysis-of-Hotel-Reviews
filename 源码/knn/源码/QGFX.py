# -*- coding: utf-8 -*-
# 此程序用来抓取 的数据
import requests
import time
import random
import re
from multiprocessing.dummy import Pool
import csv
import json
import sys
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

class Spider(object):
	
	def get_cixing(self, s):  # 分析词性
		print(1)
		if len(s) == 0:
			return ''
		print s
		s1 = SnowNLP(s)
		t = s1.sentiments
		# print t
		if t < 0.3:
			result = u'消极'
		elif t > 0.7:
			result = u'积极'
		else:
			result = u'中性'
		print result
		return result
	
	def get_detail(self): # 获取情感分析结果
		ss = []
		with open('data.csv') as f:
			tmp = csv.reader(f)
			for i in tmp:
				tt = []
				tt.extend(i[:5])
				tt.append(self.get_cixing(i[4].decode('gbk')).encode('gbk'))
				tt.extend(i[5:])
				ss.append(tt)
		with open('results.csv','w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerows(ss)

	def get_color(self,x, y):
		"""对销量不同的区段标为不同的颜色"""
		color = []
		for i in range(len(x)):
			
			if y[i] < 1000:
				color.append("green")
			elif y[i] < 2000:
				color.append("lightseagreen")
			elif y[i] < 4000:
				color.append("gold")
			else:
				color.append("coral")
		return color
	
	def draw_pic(self): # 画情感折线图
		x = [u'积极',u'中性',u'消极']
		y = [0,0,0]
		with open('results.csv','rU') as f:
			tmp = csv.reader(f)
			for i in tmp:
				try:
					t = i[5].decode('gbk')
				except:
					continue
				if t == u'积极':
					y[0] += 1
				elif t == u'中性':
					y[1] += 1
				else:
					y[2] += 1
		plt.bar(x, y,  color=self.get_color(x, y), tick_label=x)
		
		for a, b in zip(x, y):
			plt.text(a, b + 0.1, b, ha='center', va='bottom')

		plt.legend(loc="upper left")
		plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
		plt.ylabel(u'数量')
		plt.xlabel(u'情感')
		plt.rcParams['savefig.dpi'] = 300  # 图片像素
		plt.rcParams['figure.dpi'] = 300  # 分辨率
		plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
		plt.title(u"knn分析酒店情感分布")
		plt.savefig('result_qinggan.png')
		plt.show()


if __name__ == "__main__":
	spider = Spider()
	print u'knn开始分析评论情感'
	time.sleep(5)
	spider.get_detail()
	print u'评论情感分析完毕'
	print u'开始绘制情感柱状图'
	spider.draw_pic()
	print u'情感柱状图绘制完毕'
	
	
