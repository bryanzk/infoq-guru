# coding:  utf-8
from config import *
# 导入数据到这个数据库的价格数目表
class FeeHelper():
	def add_new_fee(self,z):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(FeeList).filter(FeeList.guid==z.guid).all()
		if res:
			dbSession.delete(res[0])
			dbSession.commit()
			dbSession.add(z)
			dbSession.commit()
		else:
			dbSession.add(z)
			dbSession.commit()
		return 'ok'
		
class FeeArticleWeibo(MethodView):
	def get(self):
		guid=request.args.get('guid')
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(FeeList).filter(FeeList.guid==guid).all()
		return render_template('fee_weibo.html',x=res[0])
class ImportDataToArticles(MethodView):
	def get(self):
		begin=date.today()-timedelta(days=1)
		end=date.today()
		db_session=sessionmaker(bind=DB)
		helper=FeeHelper()
		dbSession=db_session()
		res=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country=='ch').filter(RssInfo.pubdate<end).order_by(RssInfo.pubdate).all()		
		for x in res:
			z=FeeList(title=x.title,guid=x.guid,pubdate=x.pubdate,img='',desc=x.description,
				c1author='',c1cat='',c1count=0,
				c2author='',c2cat='',c2count=0)
			helper.add_new_fee(z)
		return 'ok'
	def post(self):
		begin=date.today()-timedelta(days=1)
		end=date.today()
		db_session=sessionmaker(bind=DB)
		helper=FeeHelper()
		dbSession=db_session()
		res=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country=='ch').filter(RssInfo.pubdate<end).filter(RssInfo.country=='ch').order_by(RssInfo.pubdate).all()
		for x in res:
			z=FeeList(title=x.title,guid=x.guid,pubdate=x.pubdate,img='',desc=x.description,
				c1author='',c1cat='',c1count=0,
				c2author='',c2cat='',c2count=0)
			helper.add_new_fee(z)
		return 'ok'
class FeeArticleList(MethodView):
	def get(self):
		return render_template('fee_articles.html',res='')
	def post(self):
		end=datetime.strptime((request.form['end'])+" 23:59:59",'%Y-%m-%d %H:%M:%S')
		begin=datetime.strptime((request.form['begin'])+" 00:00:00",'%Y-%m-%d %H:%M:%S')
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(FeeList).filter(and_(FeeList.pubdate>=begin,FeeList.pubdate<=end)).all()
		dbSession.close()
		return render_template('fee_articles.html',res=res)

class ShowArticleData(MethodView):
	def  get(self):
		guid=request.args.get('guid')
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(FeeList).filter(FeeList.guid==guid).all()
		return render_template('fee_ashow.html',x=res[0])
		
	def post(self):
		helper=FeeHelper()
		guid=request.form['guid']
		title=request.form['title']
		pubdate=request.form['pubdate']
		img=request.form['img']

		desc=request.form['desc']
		c1author=request.form['c1author']
		c1cat=request.form['c1cat']
		c1count=request.form['c1count']

		c2author=request.form['c2author']
		c2cat=request.form['c2cat']
		c2count=request.form['c2count']
		z=FeeList(title=title,guid=guid,pubdate=pubdate,img=img,desc=desc,
				c1author=c1author,c1cat=c2cat,c1count=c1count,
				c2author=c1author,c2cat=c2cat,c2count=c2count)
		helper.add_new_fee(z)
		flash('ok')
		return redirect('flist')
class FeeList(Base):
	__tablename__='fee_list'
	title=Column(String(100))
	guid=Column(String(200),primary_key=True)
	pubdate=Column(DateTime)
	img=Column(String(300))
	desc=Column(String(400))

	c1author=Column(String(100))
	c1cat=Column(String(200))
	c1count=Column(Integer)

	c2author=Column(String(100))
	c2cat=Column(String(200))
	c2count=Column(Integer)
	def  __init__(self,title,guid,pubdate,
		c1author,c1cat,desc,
		c2author,c2cat,c1count=0,c2count=0,img=''):
		self.title=title
		self.guid=guid
		self.pubdate=pubdate
		self.desc=desc
		self.c1author=c1author
		self.c1count=c1count
		self.c1cat=c1cat

		self.c2count=c2count
		self.c2cat=c2cat
		self.c2author=c2author

