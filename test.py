#encoding:utf-8
import sys,os
from src.crawler import *
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
	carw=carwler();
	print "####################获取文本内容####################"
	text=carw.getHtml(url)
	print carw.del_tags(text)
	print "##########################获取base64 编码图片##################################\n"
	data=carw.getImgBase64Str(text)
	print data
