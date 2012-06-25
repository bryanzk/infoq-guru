# coding: utf-8
import config
from config import *
def _me():
	return session['user']
def _all_users():
	pass
class NotifyMessage(Base):
	__tablename__='notify_list'
	id=Column(String(100),primary_key=True)
	title=Column(String(100))
	content=Column(String(200))
	status=Column(Integer)
	name=Column(String(100))
	time=Column(DateTime)
	def __init__(title,content,name):
		self.id=id_gen()
		self.title=title
		self.content=content
		self.status=0
		self.name=name
		self.time=datetime.now()
def notify(to,content,title):
	db_session=sessionmaker(bind=DB)
	dbSession=db_session()
	all_to=to.split(',')
	for x in all_to:
		n=NotifyMessage(title=title,content=content,name=x)
		dbSession.add(n)
		dbSession.commit()
	return True
class NotifyCenter(MethodView):
	def get(self):
		me=_me()
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		notifys=dbSession.query(NotifyMessage).filter(desc(NotifyMessage.time)).all()
		return render_template('notify_center.html',res=notifys)
	def post(self):
		pass
class NotifyNumber(MethodView):
	def get(self):
		me=_me()
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		notifys=dbSession.query(NotifyMessage).filter(desc(NotifyMessage.time)).filter(NotifyMessage.status==0).scalar()
		return str(notifys)

