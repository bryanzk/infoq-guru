#coding: utf-8
import config 
from config import *
class Convet_Beans(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(RssInfo).order_by(desc(RssInfo.pubdate)).filter(RssInfo.country=='en').limit(20)
		for x in results:
			if not dbSession.query(BeanList).filter(BeanList.org_guid==x.guid).all():
				b=BeanList(org_guid=x.guid,pubdate=x.pubdate)
				dbSession.add(b)
				dbSession.commit()
		return 'ok'
class BeanList(Base):
	__tablename__='bean_list'
	id=Column(String(45),primary_key=True)
	org_guid=Column(String(200))
	final_guid=Column(String(200))
	pubdate=Column(String(200))
	indate=Column(DateTime)
	outdate=Column(DateTime)
	jack=Column(DateTime)
	count=Column(Integer)
	status=Column(Integer)#0 means not pick ,1 pick ,2 done,3 review 4 re-done,9 means cancel or others
	def __init__(self,org_guid,pubdate,jack='',count=0,status=0):
		self.id=gen_id()
		self.org_guid=org_guid
		self.final_guid=''
		self.pubdate=pubdate
		self.indate=datetime.now()
		self.outdate=''
		self.jack=jack
		self.count=count
		self.status=status
class AllBeansToPick(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(BeanList,RssInfo).filter(RssInfo.guid==BeanList.org_guid).filter(BeanList.status==0).order_by(desc(BeanList.pubdate)).all()
		return render_template('beans_all_to_pick.html',res=results)
class NewsBeanToPick(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(BeanList,RssInfo).filter(RssInfo.guid==BeanList.org_guid).filter(BeanList.status==0).filter(BeanList.org_guid.like('%news%')).order_by(desc(BeanList.pubdate)).all()
		return render_template('beans_news_to_pick.html',res=results)
class ArticleBeanToPick(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(BeanList,RssInfo).filter(RssInfo.guid==BeanList.org_guid).filter(BeanList.status==0).filter(BeanList.org_guid.like("%article%")).order_by(desc(BeanList.pubdate)).all()
		return render_template('beans_article_to_pick.html',res=results)
class PickABean(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		id=request.args.get('id')
		result=dbSession.query(BeanList,RssInfo).filter(RssInfo.guid==BeanList.org_guid).filter(BeanList.id==id).filter(BeanList.status!=1).first()
		return render_template('beans_pick_one.html',x=result)
	def post(self):
		id=request.form['id']
		duedate=request.form['due']
		jack=get_user().name
		one_bean=dbSession.query(BeanList).filter(BeanList.status==0).first()
		if one_bean:
			one_bean.jack=jack
			one_bean.duedate=duedate
			one_bean.status=2
			return 'ok'



