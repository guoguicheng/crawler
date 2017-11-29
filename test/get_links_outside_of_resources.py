#encoding:utf-8
import sys,os,filetype,urllib2
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
	headers = {"Content-type":"text/html; charset=gb2312", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Encoding":"gzip,deflate,sdch","Accept-Language":"zh-CN,zh;q=0.8","Cache-Control":"max-age=0","Connection":"keep-alive" ,"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0", "Cookie": "visitkey=52562270763683935"}
	for url in data:
	    req=urllib2.Request(url.encode("utf-8"),headers =headers )
	    print url
	    try:
	        urllib2.urlopen(req)
	    except urllib2.URLError,e:
	        print("continue")
	    else:
	        print "OK"
