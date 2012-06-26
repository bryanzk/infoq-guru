# coding: utf-8
import config 
from config import *

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