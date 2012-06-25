# coding: utf-8
import config 
from config import *
try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urllib2
import logging

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o
class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value
class CountWeibo_List(Base):
	__tablename__='count_weibo_list'
	guid=Column(String(200),primary_key=True)
	short_url=Column(String(200))
	click=Column(Integer)
	count_share=Column(Integer)
	count_comment=Column(Integer)
	indate=Column(DateTime)
	def __init__(self,guid,short_url,click=0,count_comment=0,count_share=0):
		self.guid=guid
		self.short_url=short_url
		self.click=click
		self.count_comment=count_comment
		self.count_share=count_share
		self.indate=date.today()
class CountWeibo_Convert(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').order_by(desc(RssInfo.pubdate)).limit(30)
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		_token=session['token']
		_expire=session['expire']
		client.set_access_token(_token,_expire)
		for x in results:
			if not dbSession.query(CountWeibo_List).filter(CountWeibo_List.guid==x.guid).all():
				results=client.get.short_url__shorten(url_long=x.guid)
				c=CountWeibo_List(guid=x.guid,short_url=results.urls[0].url_short)
				dbSession.add(c)
				dbSession.commit()
		return 'ok'

class CountWeibo_Get(MethodView):
	def get(self):
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		_token=session['token']
		_expire=session['expire']
		client.set_access_token(_token,_expire)
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(CountWeibo_List).order_by(desc(CountWeibo_List.indate)).limit(10)
		
		for x in results:
			click=client.short_url__clicks(url_short=x.short_url).urls[0].clicks
			count_share=client.short_url__share__counts(url_short=x.short_url).urls[0].share_counts
			count_comment=client.short_url__comment__counts(url_short=x.short_url).urls[0].comment_counts
			x.click=click
			x.count_share=count_share
			x.count_comment=count_comment
			dbSession.commit()
		return 'ok'
		'''
		urls="&url_short=".join(x.short_url for x in results)
		new_urls='https://api.weibo.com/2/short_url/clicks.json?source=570026225&url_short='+urls
		data_all_clicks=urllib2.urlopen(new_urls)

		all_clicks = json.loads(data.read(), object_hook=_obj_hook)
		#all_clicks=client.get.short_url__clicks(url_short=urls)
		#all_count_share=client.get.short_url__share__counts(url_short=urls,source=APP_KEY)
		#all_count_comment=client.get.short_url__comment__counts(url_short=urls,source=APP_KEY)
		y=''
		for x in all_clicks.urls:
			y=dbSession.query(CountWeibo_List).filter(CountWeibo_List.guid==x.url_long).first()
			y.click=x.clicks
			dbSession.commit()
		for x in all_count_comment.urls:
			y=dbSession.query(CountWeibo_List).filter(CountWeibo_List.guid==x.url_long).first()
			y.count_comment=x.comment_counts
			dbSession.commit()
		for x in all_count_share.urls:
			y=dbSession.query(CountWeibo_List).filter(CountWeibo_List.guid==x.url_long).first()
			y.count_share=x.share_counts
			dbSession.commit()'''







