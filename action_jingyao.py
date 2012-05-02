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

class JingyaoList(Base):
	__tablename__='jingyao_list'
	count=Column(String(10))
	id=Column(String(20),primary_key=True)
	img=Column(String(100))
	content=Column(String(1000))
	title=Column(String(30))
	head_url=Column(String(100))
	img_url=Column(String(100))
	cat=Column(String(10))
	def  __init__(self,count,content,title,head_url,cat,img_url='',img=''):
		self.count=count
		self.id=str(datetime.now())
		self.content=content
		self.title=title
		self.head_url=head_url
		self.img_url=img_url
		self.cat=cat
		self.img=img
		
class JingyaoInput(MethodView):
	def get(self):
		return render_template('jingyao_input.html')
	def post(self):
		count=request.form['count']
		title=request.form['title']
		content=request.form['content']
		img=request.form['img']
		img_url=request.form['img_url']
		head_url=request.form['head_url']
		cat=request.form['cat']
		j=JingyaoList(count=count,content=content,title=title,img=img,head_url=head_url,img_url=img_url,cat=cat)
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		dbSession.add(j)
		dbSession.commit()
		return 'ok'
class JingyaoAds(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		count=request.args.get('count')
		jy_head=dbSession.query(JingyaoList).filter(JingyaoList.count==count).filter(JingyaoList.cat=='head').all()
		jy_down=dbSession.query(JingyaoList).filter(JingyaoList.count==count).filter(JingyaoList.cat=='down').all()
		jy_event=dbSession.query(JingyaoList).filter(JingyaoList.count==count).filter(JingyaoList.cat=='event').all()
		jy_spon=dbSession.query(JingyaoList).filter(JingyaoList.count==count).filter(JingyaoList.cat=='spon').all()
		return render_template('jingyao_ads.html',jy_head=jy_head,jy_event=jy_event,jy_down=jy_down,jy_spon=jy_spon)
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
		jy.content=dbSession.query(RssInfo).filter(or_(or_(RssInfo.guid.like(u'%articles%'),RssInfo.guid.like('%interview%')),RssInfo.guid.like(u'presentations%'))).filter(and_(RssInfo.pubdate>=last,RssInfo.pubdate<=today)).all()

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