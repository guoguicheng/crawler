#encoding:utf-8
import urllib2,urllib,chardet,re,os,base64,filetype,requests
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
        self.pat_link=re.compile(ur'(((src|href)[\s\=\'\"]{1,}([\.\/][a-zA-Z0-9\/\.\u4e00-\u9fa5\\x20-\\x7f]{0,})[\s\'\"]{1,})|((ftp|http[s]?)?[:\/]{0,}(localhost[\:0-9]{0,}|\d+\.\d+\.\d+\.\d+[\:0-9]{0,}|[a-zA-Z0-9\u4e00-\u9fa5\\x20-\\x7f\.]{0,}[a-zA-Z0-9\u4e00-\u9fa5\\x20-\\x7f]+\.[a-zA-Z0-9\u4e00-\u9fa5\\x20-\\x7f]+[\:0-9]{0,})[\/\.\?&\=\%a-zA-Z0-9\u4e00-\u9fa5\\x20-\\x7f]{0,}))')

        self.headers = {"Content-type":"text/html; charset=gb2312", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Encoding":"gzip,deflate,sdch","Accept-Language":"zh-CN,zh;q=0.8","Cache-Control":"max-age=0","Connection":"keep-alive" ,"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0", "Cookie": "visitkey=52562270763683935"}

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
        urls=re.findall(self.pat_link,page_source)
        return list(set([ur[0] for ur in urls]))
    def getRealUrl(self,url,currentUrl):
        domain=currentUrl.encode('utf-8')
        ret=re.findall(self.pat_link,domain)
        #print(ret)
        #print("ret:"+ret[0][2])
        #return
        print("GET [%s]" %(domain))
        result={"domain":"","currentUrl":"","httpStatusCode":0,"MIME":""}
        linkType=ret[0][2] if ret[0][2] else ret[0][5] if ret[0][5] else "http"
        #print("linkType=%s" %(linkType))
        #return
        try:
            if linkType in ["src","href"]:
                currentUrl=urljoin(url,ret[0][3])
            else:
                currentUrl=linkType+"://"+domain
            #print("TRY [%s]" %(currentUrl))
            request = requests.get(currentUrl)
            httpStatusCode = request.status_code
        except Exception, e:
            try:
                currentUrl=urljoin(url,domain)
                #print("TRY [%s]" %(currentUrl))
                request = requests.get(urljoin(url,domain))
                httpStatusCode = request.status_code
            except Exception, e:
                return result
        #print("RETURN CODE:[%d]" %(httpStatusCode))


        result["currentUrl"]=currentUrl
        findDomain=re.findall(self.pat_link,currentUrl)
        result['domain']=findDomain[0][6] if findDomain else ""
        result["httpStatusCode"]=httpStatusCode
        result["MIME"]=Utils.getMimeType(result['currentUrl'])
        return result

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

class Utils:
    @staticmethod
    def getMimeType(filename):
        filename_type = os.path.splitext(filename)[1][1:]
        type_list = {
                    'html'  :       'text/html',
                    'htm'   :       'text/html',
                    'shtml' :       'text/html',
                    'css'   :       'text/css',
                    'xml'   :       'text/xml',
                    'gif'   :       'image/gif',
                    'jpeg'  :       'image/jpeg',
                    'jpg'   :       'image/jpeg',
                    'js'    :       'application/x-javascript',
                    'atom'  :       'application/atom+xml',
                    'rss'   :       'application/rss+xml',
                    'mml'   :       'text/mathml',
                    'txt'   :       'text/plain',
                    'jad'   :       'text/vnd.sun.j2me.app-descriptor',
                    'wml'   :       'text/vnd.wap.wml',
                    'htc'   :       'text/x-component',
                    'png'   :       'image/png',
                    'tif'   :       'image/tiff',
                    'tiff'  :       'image/tiff',
                    'wbmp'  :       'image/vnd.wap.wbmp',
                    'ico'   :       'image/x-icon',
                    'jng'   :       'image/x-jng',
                    'bmp'   :       'image/x-ms-bmp',
                    'svg'   :       'image/svg+xml',
                    'svgz'  :       'image/svg+xml',
                    'webp'  :       'image/webp',
                    'jar'   :       'application/java-archive',
                    'war'   :       'application/java-archive',
                    'ear'   :       'application/java-archive',
                    'hqx'   :       'application/mac-binhex40',
                    'doc'   :       'application/msword',
                    'pdf'   :       'application/pdf',
                    'ps'    :       'application/postscript',
                    'eps'   :       'application/postscript',
                    'ai'    :       'application/postscript',
                    'rtf'   :       'application/rtf',
                    'xls'   :       'application/vnd.ms-excel',
                    'ppt'   :       'application/vnd.ms-powerpoint',
                    'wmlc'  :       'application/vnd.wap.wmlc',
                    'kml'   :       'application/vnd.google-earth.kml+xml',
                    'kmz'   :       'application/vnd.google-earth.kmz',
                    '7z'    :       'application/x-7z-compressed',
                    'cco'   :       'application/x-cocoa',
                    'jardiff'       :       'application/x-java-archive-diff',
                    'jnlp'  :       'application/x-java-jnlp-file',
                    'run'   :       'application/x-makeself',
                    'pl'    :       'application/x-perl',
                    'pm'    :       'application/x-perl',
                    'prc'   :       'application/x-pilot',
                    'pdb'   :       'application/x-pilot',
                    'rar'   :       'application/x-rar-compressed',
                    'rpm'   :       'application/x-redhat-package-manager',
                    'sea'   :       'application/x-sea',
                    'swf'   :       'application/x-shockwave-flash',
                    'sit'   :       'application/x-stuffit',
                    'tcl'   :       'application/x-tcl',
                    'tk'    :       'application/x-tcl',
                    'der'   :       'application/x-x509-ca-cert',
                    'pem'   :       'application/x-x509-ca-cert',
                    'crt'   :       'application/x-x509-ca-cert',
                    'xpi'   :       'application/x-xpinstall',
                    'xhtml' :       'application/xhtml+xml',
                    'zip'   :       'application/zip',
                    'bin'   :       'application/octet-stream',
                    'exe'   :       'application/octet-stream',
                    'dll'   :       'application/octet-stream',
                    'deb'   :       'application/octet-stream',
                    'dmg'   :       'application/octet-stream',
                    'eot'   :       'application/octet-stream',
                    'iso'   :       'application/octet-stream',
                    'img'   :       'application/octet-stream',
                    'msi'   :       'application/octet-stream',
                    'msp'   :       'application/octet-stream',
                    'msm'   :       'application/octet-stream',
                    'mid'   :       'audio/midi',
                    'midi'  :       'audio/midi',
                    'kar'   :       'audio/midi',
                    'mp3'   :       'audio/mpeg',
                    'ogg'   :       'audio/ogg',
                    'm4a'   :       'audio/x-m4a',
                    'ra'    :       'audio/x-realaudio',
                    '3gpp'  :       'video/3gpp',
                    '3gp'   :       'video/3gpp',
                    'mp4'   :       'video/mp4',
                    'mpeg'  :       'video/mpeg',
                    'mpg'   :       'video/mpeg',
                    'mov'   :       'video/quicktime',
                    'webm'  :       'video/webm',
                    'flv'   :       'video/x-flv',
                    'm4v'   :       'video/x-m4v',
                    'mng'   :       'video/x-mng',
                    'asx'   :       'video/x-ms-asf',
                    'asf'   :       'video/x-ms-asf',
                    'wmv'   :       'video/x-ms-wmv',
                    'avi'   :       'video/x-msvideo'
                    }
        if ( filename_type in type_list.keys() ):
            return  type_list[filename_type]
        else:
            return  ''
