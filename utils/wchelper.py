# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import jieba
import jieba.analyse
from optparse import OptionParser
import PIL
import numpy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

"""
wordcloud
分词
print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
如果/放到/post/中将/出错/o

指定ttfpath,或者把中文字体文件拷入$\Python27\Lib\site-packages\wordcloud
wc.generate(txt)  不能识别中文
所以用jieba生成词组分词字典（列表会报错）
wc.generate_from_frequencies(txtFreq)

中文无效
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simkai']
mpl.rcParams['axes.unicode_minus'] = False
"""


class WCHelper(object):
    def __init__(self, bgimage=r"D:\temp\V8.PNG", ttfpath=r"simfang.ttf",inputfile=r"d:\temp\test.txt", outimage=r"d:\temp\test.jpg"):
        self.bgimage = bgimage
        self.ttfpath = ttfpath
        self.inputfile = inputfile
        self.outimage = outimage

    #从文本中生成词组权重字典
    def GetTagsDict(self,file_name=r"d:\temp\test.txt"):
        tagsdict = {}
        content = open(file_name, 'rb').read()
        tags = jieba.analyse.extract_tags(content, topK=50, withWeight=True)
        for tag in tags:
            tagsdict[tag[0]] = tag[1]
            print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))
        return tagsdict

    #生成标签云的函数
    def GenerateCloud(self):
        # The pil way (if you don't have matplotlib)
        #image = wordcloud.to_image()
        #image.show()
        #coloring = imread(r"d:\temp\V8.png")             # 读取背景图片
        mask=numpy.array(PIL.Image.open(self.bgimage))
        fontname = self.ttfpath
        wc = WordCloud(background_color="white", # 背景颜色max_words=2000,# 词云显示的最大词数
                       mask=mask,            # 设置背景图片
                      # stopwords=STOPWORDS,      # 停止词
                       font_path=fontname,       # 兼容中文字体
                       max_font_size=150)        # 字体最大值

        #计算好词频后使用generate_from_frequencies函数生成词云
        #错误list：txtFreq例子为[('词a', 100),('词b', 90),('词c', 80)]
        #正确dict：txtFreq={u'空气龙':0.9,u'出行地图':0.7}
        #不能识别中文

        #wc.generate(text)
        #txtFreq = self.GetTagsDict(self.inputfile)
        #wc.generate_from_frequencies(txtFreq)

        # 生成图片
        plt.imshow(wc)
        plt.axis("on")
        # 绘制词云
        plt.figure()
        # 保存词云
        wc.to_file(self.outimage)
        print '生成图片 ：',self.bgimage
