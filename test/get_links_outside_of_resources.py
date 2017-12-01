#encoding:utf-8
import sys,os,filetype,urllib2,subprocess,shlex
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
	carw= carwler()
	text=carw.delComment(carw.delScript(carw.getHtml(url)))
	data=carw.getAllLinks(url,text)
	#print(data)
	for ur in data:
	    print("GET [%s]" %(ur))
	    ret=carw.getRealUrl(url,ur)
	    if ret['httpStatusCode']==200:
	        print(ret['currentUrl'],"OK")
	    else:
	        print(ret['currentUrl'],"Falied")
	print("total=%d" %(len(data)))