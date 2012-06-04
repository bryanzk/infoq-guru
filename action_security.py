# coding: utf-8
# this is for security
import config
from functools import wraps


class SecurityList(Base):
	__tablename__='security_list'
	name=Column(String(100),primary_key=True)
	type=Column(String(45))
	pwd=Column(String(45))
	def __init__(self,name,type,pwd):
		self.name=name
		self.type=type
		self.pwd=pwd
# 登陆
class SecurityLogin(MethodView):
	def get(self):
		return render_template('security_login.html')
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(SecurityList).filter(_and(SecurityList.name==name,SecurityList.pwd=pwd)).all
		if results:
			g.user=results[0]
		else:
			g.user=None
			flash('login error')
		return redirect(request.form['next'])
# 权限不足
class SecurityAuthNot(MethodView):
	def get(self):
		return '权限不足'
