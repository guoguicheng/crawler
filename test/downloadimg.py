#encoding:utf-8
import sys,os
sys.path.append(r"../src")
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
	carw=carwler()
	text=carw.delComment(carw.delScript(carw.getHtml(url)))
	print "##########################获取base64 编码图片##################################\n"
	data=carw.getImageList(url,text)
	res=resource()
	
	print "count=",len(data)
	for row in data:
	    res.downloadImg(url,'./images',row)
