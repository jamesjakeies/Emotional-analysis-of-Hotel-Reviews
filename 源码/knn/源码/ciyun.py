# encoding=utf-8
import csv
import time

import jieba
from wordcloud import WordCloud, get_single_color_func
import numpy as np
from PIL import Image
import re
from PIL import Image

def GetJB(content):  # 读取字符串使用结巴分词并将分词结果保存到list中
	stop = set()
	with open('stop.txt') as f:
		for line in f:
			stop.add(line.strip().decode('gbk'))
	tt = jieba.cut(content)
	results = []
	for i in tt:
		p1 = re.compile(u'[\u4e00-\u9fa5]{2,}')
		t0 = re.findall(p1, i)
		if len(t0) > 0 and i not in stop:
			results.append(i)
	return results

football = np.array(Image.open("111.jpg"))
text1 = ''
with open('data.csv','rU') as f:
	tmp = csv.reader(f)
	for i in tmp:
		text1 = text1 + '' + i[4].decode('gbk')
print u'数据加载成功,开始分词'
time.sleep(10)
ss = GetJB(text1)
print u'分词完毕，开始生产词云'
time.sleep(10)
a1 = {}
s1 = []
for i in ss:
	if i not in s1:
		s1.append(i)
		a1[i] = 1
	else:
		a1[i] += 1
bb = sorted(a1.items(), key=lambda x: x[1], reverse=True)
cc = [[x[0].encode('gbk', 'ignore'), str(x[1])] for x in bb]
with open('results_ciping.csv', 'w') as f:
	writer = csv.writer(f, lineterminator='\n')
	writer.writerows(cc)
# a1 = {u'你好': 13, u'再见': 8, u'滚蛋': 3}
a1 = {}
with open('results_ciping.csv') as f:
	tmp = csv.reader(f)
	for i in tmp:
		if len(i[1]) > 0:
			a1[i[0].decode('gbk')] = int(i[1])
for i in a1:
	print i + '|' + str(a1[i])
wc = WordCloud(background_color='white', max_words=1000, mask=football, color_func=get_single_color_func('black'),
               font_path="FZLTZHUNHJW.TTF", min_font_size=10,
               max_font_size=150, width=600)
wc.fit_words(a1)
picture_name = 'results.png'
wc.to_file(picture_name)
img = Image.open(picture_name)
img.show()
print u'词云生产完毕'