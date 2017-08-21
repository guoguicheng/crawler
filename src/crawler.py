#encoding:utf-8
import urllib2
import urllib
import chardet
import re
from urlparse import urljoin
import base64
class carwler:
    def getHtml(self,url):
        data1=urllib2.urlopen(url).read()
        chardit1 = chardet.detect(data1)
        text=data1.decode(chardit1['encoding']).encode("utf-8")
        return text

    def del_tags(self,str):
        pat_script=re.compile("<script([\s\S]*?)>[\s\S]*?<\/script([\s\S]*?)>",re.S)
        pat_style=re.compile("<style([\s\S]*?)>([\s\S]*?)<\/style([\s\S]*?)>",re.S)
        pat_zhushi=re.compile("<!--([\s\S]*?)-->",re.S)
        pat_html_tag=re.compile("<.+?>",re.S)
        pat_null_line=re.compile(r"\s+",re.S)
        s=pat_script.sub('',str)
        s=pat_style.sub('',s)
        s=pat_zhushi.sub('',s)
        s=pat_html_tag.sub(' ',s)
        s=pat_null_line.sub(' ',s)
        return s

    def getImgBase64Str(self,str):
        pat=re.compile("<img[\s\S]+src=[\'\"]data:image/(.+?)[\'\"][\s\S]?>",re.I)
        ds=re.findall(pat,str)
        return ds

    def getImageList(self,html):
        restr=ur'('
        restr+=ur'(http[s]?:\/\/)?[^\s,"]*\.jpg'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.jpeg'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.png'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.gif'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.bmp'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.jpeg'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.png'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.gif'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.bmp'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.ico'
        restr+=ur')'
        htmlurl = re.compile(restr,re.I)
        imgList = re.findall(htmlurl,html)
        return list(set([Arr[0] for Arr in imgList]))
        #return list(set(imgList))

    def getMediaListByExt(self,html):
        restr=ur'('
        restr+=ur'(http[s]?:\/\/)?[^\s,"]*\.mp3'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.mp4'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.avi'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.rmvb'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.mkv'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.rm'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.mpg'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.mpeg'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.wmv'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.vob'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.swf'
        restr+=ur')'
        htmlurl = re.compile(restr)
        mediaList = re.findall(htmlurl,html)
        return list(set([Arr[0] for Arr in mediaList]))
        #return list(set(mediaList))
    def getAllScript(self,html):
        restr=ur'('
        restr+=ur'(http[s]?:\/\/)?[^\s,"]*\.css'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.js'
        restr+=ur')'
        htmlurl = re.compile(restr)
        links = re.findall(htmlurl,html)
        return list(set([Arr[0] for Arr in links]))
        #return list(set(links))
    def getAllLinks(self,html):
        restr=ur'('
        restr+=ur'http[s]?:\/\/[^\s,"]*'
        restr+=ur')'
        htmlurl = re.compile(restr)
        links = re.findall(htmlurl,html)
        return list(set(links))
    def download(self,imgList, page):
        x = 1
        for imgurl in imgList:
            imgurl=urljoin(url,imgurl)
            filepathname=str('D:/tmp/python/dimg/pic_%09d_%010d'%(page,x)+str(os.path.splitext(urllib2.unquote(imgurl).decode('utf8').split('/')[-1])[1])).lower()
            print '[Debug] Download file :'+ imgurl+' >> '+filepathname
            urllib.urlretrieve(imgurl,filepathname)
            x+=1

    def downImageNum(self,pagenum):
        page = 1
        pageNumber = pagenum
        while(page <= pageNumber):
            html = getHtml(url)
            imageList = getImageList(html)
            download(imageList,page)
            page = page+1
    def saveBase64Img(self,fileName,strs):
        imgdata=base64.b64decode(strs)
        file=open(fileName,'wb')
        file.write(imgdata)
        file.close()

	
