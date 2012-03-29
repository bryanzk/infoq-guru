from config import *
class UserLogin(MethodView):
	def  get(self):
		pass
	def post(self):
		user=request.form['user']
		pwd=request.form['pwd']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(UserListInfo).filter(UserListInfo.user==user).filter(UserListInfo.pwd==pwd).all()
		if res:
			session['user']=user
			return redirect('/')
		else:
			return redirect('error?msg="login error"&next=/go')
class ErrorView(MethodView):
	def get(self):
		msg=request.args.get('msg')
		next=request.args.get('next')
		return render_template('error.html',msg=msg,next=next)
class UserLogout(MethodView):
	def  get():
		pass
	def post():
		pass