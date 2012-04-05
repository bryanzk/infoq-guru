# -*- coding: utf-8
import config
from config import *
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
	def clear_weibo_exists(self,guid):
		db_session=sessinmaker(bind=DB)
		dbSession=db_session()
		x=dbSession.query(WeiboM).filter(WeiboM.org_url==guid).all()
		if x:
			dbSession.delete(x[0])
			dbSession.commit()
		else:
			return False
class WeiboHelper():
	def _is_article(self,text):
		_key=re.compile(u'.*By.*http://t.cn.*')
		match=_key.match(text)
		if match:
			return True
		else:
			return False
	def _get_data_with_page(self,page):
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		_token=session['token']
		_expire=session['expire']
		client.set_access_token(_token,_expire)
		result=client.get.statuses__user_timeline(feture=1,screen_name='InfoQ',count=200,page=page)
		_xx=[]
		for x in result.statuses:
			if self._is_article(x.text):
				m=MInfo()
				m.title=self._get_title(x.text)
				m.a=self._get_authro(x.text)
				m.text=x.text
				m.r=x.reposts_count
				m.c=x.comments_count
				m.t=self._get_time(x.created_at)
				m.u=self._get_org_url(x.text)
				m.i=x.id
				m.tr=''
				m.wu="http://api.t.sina.com.cn/1746173800/statuses/"+str(x.id)+"?source="+APP_KEY
				m.cat=self._get_cats(m.u)
				xx=WeiboM(title=m.title,
					url=m.wu,
					retweet=m.r,
					time=m.t,
					comment=m.c,
					text=m.text,
					org_url=m.u,
					athur=m.a,
					cat=m.cat)
				_xx.append(xx)
		return _xx
	def _get_data(self):
		return self._get_data_with_page(1)
	def _get_time(self,text):
		return datetime.strptime(text,'%a %b %d %H:%M:%S +0800 %Y')
	def _get_title(self,text):
		ms=re.findall(u'\u3010[^\u3010].*[^\u3011]\u3011', text)
		if ms:
			return (ms[0])[1:-1]
		else:
			return 'none'
	def _get_authro(self,text):
		ms = re.findall('By.*http', text)
		if ms:
			_x=(ms[0])[2:-4]
			if len(_x)<20:
				return _x
			else:
				_key=re.findall(u'By.*?\uff1a',text)
				if _key:
					return (_key[0])[2:-1]
				else:
					return _x
		else:
			return 'none'
	def _get_cats(self,text):
		if string.find(text,'/news')!=-1:
			return u'新闻'
		elif string.find(text,'/articles')!=-1:
			return u'文章'
		elif string.find(text,'/presentations')!=-1:
			return u'演讲'
		elif string.find(text,'/minibooks')!=-1:
			return u'迷你书'
		elif string.find(text,'/interviews')!=-1:
			return u'采访'
		else:
			return 'x'
	def _get_http_content(self,rurl):
		res=urllib2.urlopen(rurl)
		data=res.read()
		return data
	def _get_short_url(self,text):
		_key=re.findall('http://t.cn/[0-9a-zA-Z]{0,8}',text)
		if _key:
			return _key[0]
		else:
			return 'http://t.cn/zOcGI1F'
	def  _get_org_url(self,text):
		url="http://api.t.sina.com.cn/short_url/expand.json?source="+APP_KEY+'&url_short='+self._get_short_url(text)
		print url
		res=urllib2.urlopen(url)
		data=res.read()
		print data
		return (json.loads(data))[0]['url_long']