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
	text=carw.getHtml(url)
	print "##########################获取base64 编码图片##################################\n"
	data=carw.getImgBase64Str(text)
	print "count=",len(data)
	res=resource()
	for row in data:
		restr=r'(.+)/(.+);(.+),(.+)'
		pat=re.compile(restr,re.I)
		ds=re.match(pat,row)
		name=random.randint(10000,999999)
		res.saveBase64Img('./base64/%s.%s' %(name,ds.group(2)),ds.group(4))
