#encoding:utf-8
import sys,os
sys.path.append(r"../src")
from selenium import webdriver
from crawler import *
url=""
if __name__ =='__main__':
	for i in range(1,len(sys.argv)):
		if(sys.argv[i]=='--url'):
			url=sys.argv[i+1]
		if(sys.argv[i]=="--h"):
			print "--url "
			quit()
	if(url==""):
		print "type --h ?"
		quit()
	browser=webdriver.PhantomJS()
	browser.get(url)
	text=browser.page_source
	browser.quit()

	print "##########################获取base64 编码图片##################################\n"
	carw=carwler()
	data=carw.getImgBase64Str(text)
	print "count=",len(data)
	#for row in data:
	#    print row
