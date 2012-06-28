# coding: utf-8
import config
from config import *
class SesameList(Base):
	__tablename__='sesame_list'
	id=Column(String(45),primary_key=True)
	title=Column(String(200))
	content=Column(String(800))
	final_guid=Column(String(200))
	cat=Column(String(45))
	brown=Column(String(45))
	duedate=Column(DateTime)
	indate=Column(DateTime)
	outdate=Column(DateTime)
	jack=Column(DateTime)
	count=Column(Integer)
	pickdate=Column(DateTime)
	status=Column(Integer)#0 means not pick ,1 pick ,2 done,3 review 4 re-done,9 means cancel or others
	def __init__(self,title,content,cat,brown='',jack='',count=0,status=0,pickdate=''):
		self.id=gen_id()
		self.title=title
		self.content=content
		self.cat=cat
		self.final_guid=''
		self.brown=brown

		self.indate=datetime.now()
		self.outdate=''
		self.duedate=''

		self.jack=jack
		self.count=count
		self.status=status
		self.pickdate=pickdate
class DeleteASesame(MethodView):
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		id=request.form['id']
		results=dbSession.query(SesameList).filter(SesameList.id==id).filter(SesameList.status==0).order_by(desc(SesameList.indate)).all()
		try:
			dbSession.delete(results[0])
			dbSession.commit()
			notify_m(content='删除线索')
			return 'ok'
		except:
			return 'fail'
class AddASesame(MethodView):
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		title=request.form['title']
		content=request.form['content']
		Cat_List={'yy':'语言 & 开发','gc':'过程 & 时间','qy':'企业架构','yw':'运维 & 基础架构','jg':'架构&设计'}

		cat=Cat_List[request.form['cat']]
		brown=get_user().user
		s=SesameList(title=title,content=content,cat=cat,brown=brown)
		try:
			dbSession.add(s)
			dbSession.commit()
			notify_m(content='添加线索:'+title,to='admin,core,gof,editor')
			return 'ok'
		except:
			return 'fail'
class AllSesameToPick(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(SesameList).filter(SesameList.status==0).order_by(desc(SesameList.indate)).all()
		return render_template('sesame_all_to_pick.html',res=results)
class SesameToPick(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(SesameList).filter(SesameList.status==0).order_by(desc(SesameList.indate)).all()
		return render_template('sesame_to_pick.html',res=results)

class PickASesame(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		id=request.args.get('id')
		result=dbSession.query(SesameList).filter(SesameList.id==id).filter(SesameList.status!=1).first()
		return render_template('Sesame_pick_one.html',x=result)
	@login(wtype='admin,core,editor,gof')
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		id=request.form['id']
		duedate=request.form['due']
		jack=get_user().user

		one_bean=dbSession.query(SesameList).filter(SesameList.id==id).filter(SesameList.status==0).first()
		if one_bean:
			one_bean.jack=jack
			one_bean.duedate=striptime(duedate)
			one_bean.status=1
			one_bean.pickdate=datetime.now()
			dbSession.commit()

			notify_m(content='领取线索')
			return str('ok')
		else:
			return 'picked'
class SesameToDone(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(SesameList).filter(SesameList.status==1).order_by(desc(SesameList.indate)).all()
		return render_template('sesame_to_done.html',res=results)
class DoneASesame(MethodView):
	@login(wtype='admin,core,editor,gof')
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		id=request.form['id']
		count=request.form['count']
		final_guid=request.form['guid']
		jack=get_user().user
		one_sesame=dbSession.query(SesameList).filter(SesameList.id==id).filter(SesameList.status==1).first()
		if one_sesame:
			one_sesame.final_guid=final_guid
			one_sesame.status=2
			one_sesame.count=count
			one_sesame.outdate=datetime.now()
			dbSession.commit()
			notify_m(content='完成线索')
			return 'ok'
class SesamePending(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(SesameList).filter(SesameList.status==1).order_by(desc(SesameList.indate)).all()
		return render_template('sesame_pending.html',res=results)
