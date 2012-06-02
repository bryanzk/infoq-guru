# coding: utf-8
import config
from config import *

class CountContents(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		_results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').all()
		_results_week=dbSession.query(RssInfo).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).all()
		_results_month=dbSession.query(RssInfo).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).all()		
		
		_results_week_news=dbSession.query(RssInfo).filter(RssInfo.guid.like('%cn/news')).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).all()
		_results_month_news=dbSession.query(RssInfo).filter(RssInfo.guid.like('%cn/news')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).all()		
		raise
	def post(self):
		pass
class CountHelper():
	def convert_to_detail_count(self,all):
		pass
class CountEditors(MethodView):
	def get(self):
		pass