#encoding:utf-8
import sys,os
sys.path.append(r"../src")
from crawler import *
import random
from selenium import webdriver
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
	carw=carwler()
	browser=webdriver.PhantomJS()
	browser.get(url)
	text=browser.page_source
	browser.quit()

	print "##########################获取base64 编码图片##################################\n"
	data=carw.getImgBase64Str(text)
	print "count=",len(data)
	res=resource()
	restr=r'(.+)/(.+);(.+),(.+)'
	pat=re.compile(restr,re.I)
	#print data[0]==data[1]
	for row in range(0,len(data)):
	#    print data[row]
	    ds=re.match(pat,data[row])
	    name=random.randint(10000,999999)
	    res.saveBase64Img('./base64/%s.%s' %(name,ds.group(2)),ds.group(4))
	    print(row,ds.group(2))