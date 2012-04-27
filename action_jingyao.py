# -*- coding: utf-8 -*-
import config 
from datetime import timedelta
from config import *
class JingyaoContent(object):
	yuyan=''
	jiagou=''
	guocheng=''
	yunwei=''
	qiye=''

class JingyaoNews(object):
	yuyan=''
	jiagou=''
	guocheng=''
	yunwei=''
	qiye=''

class Jingyao(object):
	content=JingyaoContent()
	news=JingyaoNews()
	cdate=''
	date=''
	def __init__(self):
		pass
class JingyaoOut(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		today=datetime.datetime(2012, 4, 24, 23, 59)
		last=today-timedelta(days=7)
		jy=Jingyao()
		jy.count=123
		jy.cdate=''
		jy.date=''
		jy.content.yuyan=dbSession.query(RssInfo).filter(or_(or_(RssInfo.guid.like(u'%articles%'),RssInfo.guid.like('%interview%')),RssInfo.guid.like(u'presentations%'))).filter(RssInfo.category.like(u'%语言 & 开发%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.content.jiagou=dbSession.query(RssInfo).filter(or_(or_(RssInfo.guid.like(u'%articles%'),RssInfo.guid.like('%interview%')),RssInfo.guid.like(u'presentations%'))).filter(RssInfo.category.like(u'%架构 & 设计%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.content.guocheng=dbSession.query(RssInfo).filter(or_(or_(RssInfo.guid.like(u'%articles%'),RssInfo.guid.like('%interview%')),RssInfo.guid.like(u'presentations%'))).filter(RssInfo.category.like(u'%过程 & 实践%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.content.yunwei=dbSession.query(RssInfo).filter(or_(or_(RssInfo.guid.like(u'%articles%'),RssInfo.guid.like('%interview%')),RssInfo.guid.like(u'presentations%'))).filter(RssInfo.category.like(u'%运维 & 基础架构%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.content.qiye=dbSession.query(RssInfo).filter(or_(or_(RssInfo.guid.like(u'%articles%'),RssInfo.guid.like('%interview%')),RssInfo.guid.like(u'presentations%'))).filter(RssInfo.category.like(u'%企业架构%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)


		jy.news.yuyan=dbSession.query(RssInfo).filter(RssInfo.guid.like(u'%news%')).filter(RssInfo.category.like(u'%语言 & 开发%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.news.jiagou=dbSession.query(RssInfo).filter(RssInfo.guid.like(u'%news%')).filter(RssInfo.category.like(u'%架构 & 设计%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.news.guocheng=dbSession.query(RssInfo).filter(RssInfo.guid.like(u'%news%')).filter(RssInfo.category.like(u'%过程 & 实践%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.news.yunwei=dbSession.query(RssInfo).filter(RssInfo.guid.like(u'%news%')).filter(RssInfo.category.like(u'%运维 & 基础架构%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)
		jy.news.qiye=dbSession.query(RssInfo).filter(RssInfo.guid.like(u'%news%')).filter(RssInfo.category.like(u'%企业架构%')).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).limit(5)

		return render_template('jingyao_output.html',jy=jy)