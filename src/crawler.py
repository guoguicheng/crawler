#encoding:utf-8
import urllib2,urllib,chardet,re,os,base64
from urlparse import urljoin

class carwler:
    def __init__(self,imgExt=None,mediaExt=None,scriptExt=None):
        if not imgExt:
            imgExt=['jpg','jpeg','png','gif','bmp','ico']
        if not mediaExt:
            mediaExt=['mp3','mp4','avi','rmvb','mkv','rm','mpg','mpeg','wmv','vob','swf']
        if not scriptExt:
            scriptExt=['js','css']

        self.pat_script_content=re.compile("<script([\s\S]*?)>[\s\S]*?<\/script([\s\S]*?)>",re.S)
        self.pat_style_content=re.compile("<style([\s\S]*?)>([\s\S]*?)<\/style([\s\S]*?)>",re.S)
        self.pat_comment=re.compile("<!--([\s\S]*?)-->",re.S)
        self.pat_null_line=re.compile(r"\s+",re.S)
        self.pat_html_tag=re.compile("<.+?>",re.S)
        self.pat_base64Str=re.compile(r'<img[\s\S]+?src=[\'\"]data:(.+?)[\'\"][\s\S\>]?',re.I)
        reg_image_str=ur'('
        tag=""
        for ext in imgExt:
            reg_image_str+=ur'%s(http[s]?:\/\/)?[^\s,"]*\.%s' %(tag,ext)
            tag="|"
        reg_image_str+=ur')'
        self.pat_image = re.compile(reg_image_str,re.I)
        reg_media_str=ur'('
        tag=""
        for ext in mediaExt:
            reg_media_str+=ur'%s(http[s]?:\/\/)?[^\s,"]*\.%s' %(tag,ext)
            tag="|"
        reg_media_str+=ur')'
        self.pat_media = re.compile(reg_media_str)
        reg_script_str=ur'('
        tag=""
        for ext in scriptExt:
            reg_script_str+=ur'%s(http[s]?:\/\/)?[^\s,"]*\.%s' %(tag,ext)
            tag="|"
        reg_script_str+=ur')'
        self.pat_script = re.compile(reg_script_str)
        self.pat_all_link=re.compile(ur'((http[s]?:\/\/)?([a-zA-Z0-9\.]+\.)?[a-zA-Z0-9]+\.[a-zA-Z0-9]+[\/]?[\/\?&\=\%a-zA-Z0-9\u4e00-\u9fa5\\x20-\\x7f]+)')

    def getHtml(self,url):
        data1=urllib2.urlopen(url).read()
        chardit1 = chardet.detect(data1)
        text=data1.decode(chardit1['encoding']).encode("utf-8")
        return text

    def delScript(self,page_source):
        s=self.pat_script_content.sub('',page_source)
        s=self.pat_style_content.sub('',s)
        return s

    def delComment(self,page_source):
        s=self.pat_comment.sub('',page_source)
        return s

    def getText(self,page_source):
        s=self.delScript(page_source)
        s=self.delComment(s)
        s=self.pat_null_line.sub(' ',s)
        s=self.pat_html_tag.sub(' ',s)
        return s

    def getImgBase64Str(self,page_source):
        ds=re.findall(self.pat_base64Str,page_source)
        return ds

    def getImageList(self,url,page_source):
        imgList = re.findall(self.pat_image,page_source)
        return list(set([urljoin(url,Arr[0]) for Arr in imgList]))
        #return list(set(imgList))

    def getMediaList(self,url,page_source):
        mediaList = re.findall(self.pat_media,page_source)
        return list(set([urljoin(url,Arr[0]) for Arr in mediaList]))

    def getAllScript(self,url,page_source):
        links = re.findall(self.pat_script,page_source)
        return list(set([urljoin(url,Arr[0]) for Arr in links]))

    def getAllLinks(self,url,page_source):
        page_source=page_source.decode('utf8')
        urls=re.findall(self.pat_all_link,page_source)
        return list(set([urljoin(url,ur[0])  for ur in urls]))

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

	
