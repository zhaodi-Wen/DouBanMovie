#!/usr/bin/evn python
#-*-coding: utf-8 -*-
'''
Created on 2017Äê8ÔÂ17ÈÕ

@author: WZD06
'''

from bs4 import BeautifulSoup
import urllib2
from mylog import MyLog as mylog
import sys
from saveExcel3 import saveDouBanMovie

reload(sys)
sys.setdefaultencoding('utf-8')
'''这两句是为了避免 UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1: ordinal not in range(128), 的错误'''
'''这是因为 python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。'''

class DouBanItem(object):
	"""docstring for DouBanItem"""
	
	name = None
	point = None
	director = None
	staring = None
	type = None
	country = None
	year = None
	#detail = None

class GetDouBanMovie(object):
	"""docstring for GetDouBanMovie"""
	def __init__(self):
		self.urls = []
		self.log = mylog()
		self.getUrls()
		self.items = self.spider(self.urls)
		self.piplines(self.items)
		self.log.info(u'begin to save the data to excel...\r\n')
		saveDouBanMovie(self.items)
		self.log.info(u'already saved the data to excel...\r\n')

	def getUrls(self):
		pages = 12
		for i in xrange(pages):
			url = r'https://www.douban.com/doulist/240962/?start='+str(i*25)+'&sort=seq&sub_type='
			self.urls.append(url)
			self.log.info(u'添加URL：%s成功 \r\n'%url)

	def getResponseContent(self,url):
		try:
			response = urllib2.urlopen(url.encode('utf8'))
		except :
			self.log.error(u'获取url:%s失败\r\n'%url)
		else:
			self.log.info(u'获取url:%s成功\r\n'%url)
			return response.read()

	def spider(self,urls):
		items = []
		for url in urls:
			htmlcontent = self.getResponseContent(url)
			soup = BeautifulSoup(htmlcontent,'lxml')
			tags = soup.find_all('div',attrs={'class':"bd doulist-subject"})
			for tag in tags:
				item = DouBanItem()
				item.name = tag.find('div',attrs={'class':"title"}).a.get_text().strip()
				item.point = tag.find('div',attrs={'class':"rating"}).find('span',attrs={'class':"rating_nums"}).get_text().strip()
				content = tag.find('div',attrs={'class':"abstract"})
				details = content.get_text()
				details = details.replace(' ','').split()
				item.director = details[0].split(':')[1]
				item.staring = details[1].split(':')[1]
				item.type = details[2].split(':')[1]
				item.country = details[3].split(':')[1]
				item.year = details[4].split(':')[1]
				items.append(item)
				self.log.info(self.log.info(u'获取名字为%s 数据成功'%(item.name)))
		return items
		
	def piplines(self,items):
		filename = 'Douban.txt'
		ranking = 1
		for item in items:
			with open(filename,'a') as fp:
				fp.write("排名 ：			  %d\n"%ranking)
				fp.write("电影名字：        %s\n"%item.name)
				fp.write("评分：            %s\n"%item.point)
				fp.write("导演:             %s\n"%item.director)
				fp.write("主演:             %s\n"%item.staring)
				fp.write("类型:             %s\n"%item.type)
				fp.write("制片国家/地区:    %s\n"%item.country)
				fp.write("年份：            %s\n"%item.year)
				fp.write('-'*25+'\n')
				self.log.info(u'保存电影名字为%s成功'%(item.name))
				ranking +=1

if __name__ == '__main__':
	Douban = GetDouBanMovie()






		
		