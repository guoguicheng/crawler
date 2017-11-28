#encoding:utf-8
import sys,os
sys.path.append(r"../src")
from crawler import *
url=""

if __name__ =='__main__':
	
	carw=carwler()
	res=resource()
	#text=carw.delComment(carw.delScript(carw.getHtml(url)))
	url=""
	for i in range(1,21):
		url="http://cs.stanford.edu/people/karpathy/convnetjs/demo/mnist/mnist_batch_%d.png" %(i)
		#print(url)
		#continue
		res.downloadImg(url,'./images',url)
