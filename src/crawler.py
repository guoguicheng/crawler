#encoding:utf-8
import urllib2,urllib,chardet,re,os,base64
from urlparse import urljoin

class carwler:
    def getHtml(self,url):
        data1=urllib2.urlopen(url).read()
        chardit1 = chardet.detect(data1)
        text=data1.decode(chardit1['encoding']).encode("utf-8")
        return text

    def delScript(self,page_source):
        pat_script=re.compile("<script([\s\S]*?)>[\s\S]*?<\/script([\s\S]*?)>",re.S)
        pat_style=re.compile("<style([\s\S]*?)>([\s\S]*?)<\/style([\s\S]*?)>",re.S)
        s=pat_script.sub('',page_source)
        s=pat_style.sub('',s)
        return s

    def delComment(self,page_source):
        pat_comment=re.compile("<!--([\s\S]*?)-->",re.S)
        s=pat_comment.sub('',page_source)
        return s

    def getText(self,page_source):
        s=self.delScript(page_source)
        s=self.delComment(s)
        pat_null_line=re.compile(r"\s+",re.S)
        pat_html_tag=re.compile("<.+?>",re.S)
        s=pat_null_line.sub(' ',s)
        s=pat_html_tag.sub(' ',s)
        return s

    def getImgBase64Str(self,page_source):
        restr=r'<img[\s\S]+?src=[\'\"]data:(.+?)[\'\"][\s\S\>]?'
        pat=re.compile(restr,re.I)
        ds=re.findall(pat,page_source)
        return ds

    def getImageList(self,url,page_source):
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
        imgList = re.findall(htmlurl,page_source)
        return list(set([urljoin(url,Arr[0]) for Arr in imgList]))
        #return list(set(imgList))

    def getMediaList(self,url,page_source):
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
        mediaList = re.findall(htmlurl,page_source)
        return list(set([urljoin(url,Arr[0]) for Arr in mediaList]))


    def getAllScript(self,url,page_source):
        restr=ur'('
        restr+=ur'(http[s]?:\/\/)?[^\s,"]*\.css'
        restr+=ur'|(http[s]?:\/\/)?[^\s,"]*\.js'
        restr+=ur')'
        htmlurl = re.compile(restr)
        links = re.findall(htmlurl,page_source)
        return list(set([urljoin(url,Arr[0]) for Arr in links]))

class resource:
    def downloadImg(self,url,savePath,imgurl):
        imgurl=urljoin(url,imgurl,savePath)
        filepathname=str('%s/'%(savePath)+str(urllib2.unquote(imgurl).decode('utf8').split('/')[-1])).lower()
        print '[Debug] Download file :'+ imgurl+' >> '+filepathname
        urllib.urlretrieve(imgurl,filepathname)
        return filepathname

    def saveBase64Img(self,fileName,base64Str):
        file=open("%s" %(fileName),'wb')
        imgdata=base64.b64decode(base64Str)
        file.write(imgdata)
        file.close()

	
