from config import *
class UserLogin(MethodView):
	def  get(self):
		session['next']=request.args.get('next')
		return render_template('user_login.html')
	def post(self):
		user=request.form['user']
		pwd=request.form['pwd']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(UserListInfo).filter(UserListInfo.user==user).filter(UserListInfo.pwd==pwd).all()
		if res:
			g.user=res[0]
			session['user']=res[0]
			flash('login ok')
			return redirect(session['next'])
		else:
			return redirect('error?msg="login error"&next=/login')
class ErrorView(MethodView):
	def get(self):
		msg=request.args.get('msg')
		next=request.args.get('next')
		return render_template('error.html',msg=msg,next=next)
class UserLogout(MethodView):
	def  get(self):
		session.clear()
		return redirect('login')
	def post():
		pass