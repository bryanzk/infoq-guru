#coding: utf-8
from config import *
class UserLogin(MethodView):
	def  get(self):
		try:
			user=session['user']
			check_list={'admin':'go',"core":"core-index",'gof':'gof-index','editor':'editor-index'}	
                        try:
				return redirect(session['next'] or check_list[user.cat])
                        except:
                        	return redirect(check_list[user.cat])
		except:
			session['next']=request.args.get('next')
			return render_template('user_login.html')
	def post(self):
		user=request.form['user']
		pwd=request.form['pwd']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(UserListInfo).filter(UserListInfo.user==user).filter(UserListInfo.pwd==md5(pwd)).all()
		if res:
			g.user=res[0]
			session['user']=res[0]
			flash('login ok')
			check_list={'admin':'go',"core":"core-index",'gof':'gof-index','editor':'editor-index'}
			notify_m(hey='',content='登陆系统')
			try:
				return redirect(session['next'] or check_list[g.user.cat])
                        except:
                        	return redirect(check_list[g.user.cat])
		else:
			return redirect('error?msg="login error"&next=/login')
class ErrorView(MethodView):
	def get(self):
		msg=request.args.get('msg')
		next=request.args.get('next')
                return redirect('/login')
		return render_template('error.html',msg=msg,next=next)
class Logout(MethodView):
	def  get(self):
		session.clear()
		return redirect('login')
	def post():
		pass