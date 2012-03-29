# -*- coding:utf-8 -*-
import config
from config import *
from functools import wraps
from flask import g, request, redirect, url_for


class Date_Helper():
    def _get_begin_end(self):
        end=datetime.strptime((request.form['end'])+" 23:59:59",'%Y-%m-%d %H:%M:%S')
        begin=datetime.strptime((request.form['begin'])+" 00:00:00",'%Y-%m-%d %H:%M:%S')
        return begin,end
class Helper_Data():
    def is_weibo_exists(self,guid):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        if dbSession.query(WeiboM).filter(WeiboM.org_url==guid).all():
            return True
        else:

            return False
class InfoqHelper():
    def _is_trans(self,url):
        res = urllib2.urlopen(url)
        r=res.read().decode('utf-8')
        if string.find(r,u'\u8bd1\u8005')!=-1:
            return u'翻译'
        else:
            return u'原创'

class WeiboHelper():
    def _is_article(self,text):
        _key = re.compile(u'.*By.*http://t.cn.*')
        match = _key.match(text)
        if match:
            return True
        else:
            return False
    def _get_data_with_page(self,page):
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        _token = session['token']
        _expires_in = session['expires_in']
        print _token,_expires_in
        client.set_access_token(_token,_expires_in)
        result=client.get.statuses__user_timeline(feature=1,screen_name='InfoQ',count=200,page=page)
        _helper = self
        _r=[]
        _ihelper=InfoqHelper()
        _xx=[]
        for x in result.statuses:
            if _helper._is_article(x.text):
                m=MInfo()
                #m.time=x.time
                m.title=(_helper._get_title(x.text))
                m.a=_helper._get_author(x.text)
                #m.t=((x.created_at)[26:30]+(x.created_at)[3:11])
                m.text=x.text
                m.r=x.reposts_count 
                m.c=x.comments_count
                m.t=_helper._get_time(x.created_at)
                m.u=_helper._get_org_url(x.text)
                m.i=x.id
                m.tr=""#_ihelper._is_trans(m.u)
                #http://weibo.com/1746173800/y7pO7AGx8
                m.wu="http://api.t.sina.com.cn/1746173800/statuses/"+str(x.id)+"?source="+APP_KEY
                m.cat=_helper._get_cats(m.u)
                xx=WeiboM(title=m.title,url=m.wu,retweet=m.r,time=m.t,comment=m.c,
                    text=m.text,
                    org_url=m.u,athur=m.a,cat=m.cat)
                xx.title.encode('utf-8')
                xx.text.encode('utf-8')
                xx.athur.encode('utf-8')
                xx.cat.encode('utf-8')
                _xx.append(xx)
        return _xx
    def _get_data(self):
        return self._get_data_with_page(1)
    def _get_time(self,text):
        return datetime.strptime(text,'%a %b %d %H:%M:%S +0800 %Y')
        #"Tue May 31 17:46:55 +0800 2011","")
    def _get_title(self,text):
        ms = re.findall(u'\u3010[^\u3010].*[^\u3011]\u3011', text)
        if ms:
            # return ms[0]
            return (ms[0])[1:-1]
        else:
            return 'none'
    
    
    def _get_author(self,text):
        ms = re.findall('By.*http', text)
        if ms:
            _x=(ms[0])[2:-4]
            # _x=ms[0]
            if len(_x)<20:
                return _x
            else:
                # _key=re.findall(u'By[^By].*?[^\uff1a]\uff1a',text)
                _key=re.findall(u'By.*?\uff1a',text)
                if _key:
                    return (_key[0])[2:-1]
                    # return _key[0]
                else:
                    return _x
        else:
            return 'none'
    def _get_cats(self,text):
        '''
            news /cn/news
            article  /cn/articles
            pres cn/presentations
            mini /cn/minibooks/
        '''
        if string.find(text,'/news')!=-1:
            return u'新闻'
        elif string.find(text,'/articles')!=-1:
            return u'文章'
        elif string.find(text,'/presentations')!=-1:
            return u'视频'
        elif string.find(text,'/minibooks')!=-1:
            return u'迷你书'
        else :
            return 'x'
    def __get_http_content(self,url):
        res=urllib2.urlopen(url)
        data=res.read()
        return data
    def _get_the_cat(self,url):
        if string.find(self.__get_http_content(url),'译者')!=-1:
            return '翻译'
        else:
            return '原创'


    def _get_timespan(self,text):
        return 1000 * time.mktime(text.timetuple())
    def _get_org_url(self,text):
        url="http://api.t.sina.com.cn/short_url/expand.json?source="+APP_KEY+'&url_short='+self._get_short_url(text)
        res=urllib2.urlopen(url)
        data=res.read()
        return (json.loads(data))[0]['url_long']
    
    def _get_short_url(self,text):
        _key=re.findall('http://t.cn/[0-9a-zA-Z]{0,8}',text)
        
        if _key:
            return _key[0] 
        else:
            return 'http://t.cn/zOcGI1F'