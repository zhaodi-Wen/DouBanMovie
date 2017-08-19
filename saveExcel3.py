#!/usr/bin/evn python
#-*-coding: utf-8 -*-
'''
Created on 2017年8月17日

@author: WZD06
'''
import xlwt

class saveDouBanMovie(object):
	"""docstring for saveDouBanMovie"""
	def __init__(self,items):
		self.items = items
		self.run(self.items)

	def run(self,items):
		filename = u'豆瓣电影.xls'.encode('GBK')
		book = xlwt.Workbook(encoding='utf8')
		sheet = book.add_sheet('movie',cell_overwrite_ok=True)
		sheet.write(0,0,u'电影名字'.encode('utf8'))
		sheet.write(0,1,u'评分'.encode('utf8'))
		sheet.write(0,2,u'导演'.encode('utf8'))
		sheet.write(0,3,u'主演'.encode('utf8'))
		sheet.write(0,4,u'类型'.encode('utf8'))
		sheet.write(0,5,u'制片国家/地区'.encode('utf8'))
		sheet.write(0,6,u'年份'.encode('utf8'))
		i = 1
		while (i<=len(items)):
			item = items[i-1]
			sheet.write(i,0,item.name)
			sheet.write(i,1,item.point)
			sheet.write(i,2,item.director)
			sheet.write(i,3,item.staring)
			sheet.write(i,4,item.type)
			sheet.write(i,5,item.country)
			sheet.write(i,6,item.year)
			i+=1
		book.save(filename)

if __name__ == '__main__':
	pass