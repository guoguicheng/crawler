#encoding:utf-8
import sys,os
sys.path.append(r"../src")
from crawler import *
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
	print "####################获取文本内容####################"
	
	print carw.getText(text)
	
