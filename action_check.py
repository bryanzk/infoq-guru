# -*- coding: utf-8 -*-
from config import *
from action_mail import *
class WPHelper():
	def is_uid_exists(self,uid):
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		r=dbSesion.query(WPList).filter(WPList.uid==uid).all()
		if  r:
			return True
		else:
			return False
	def add_to_database(self,w):
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		r=dbSesion.query(WPCheckList).filter(WPCheckList.url==w.url).first()
		if r:
			dbSesion.delete(r)
		dbSesion.add(w)
		
		dbSesion.commit()


class WPAddView(MethodView):
	"""docstring for WPCheckView"""
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		res=dbSesion.query(WPList).all()
		dbSesion.close()
		return render_template('wp_add.html',res=res)
	def  post(self):
		name=request.form['name']
		screen_name=request.form['screen_name']
		uid=request.form['uid']
		cat=request.form['cat']
		
		u=WPList(name=name,screen_name=screen_name,uid=uid,cat=cat)
		u.name.encode('utf-8')
		u.screen_name.encode('utf-8')
		u.cat.encode('utf-8')
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		helper=WPHelper()
		if not helper.is_uid_exists(uid):
			dbSesion.add(u)
			dbSesion.commit()

		return redirect('wpadd')

class WPSend(MethodView):
	def get(self):
		return render_template('wp_mail.html')
	def post(self):
		m=MailMethod()
		content=''
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		begin=date.today()
		end=date.today()+timedelta(days=1)
		res=dbSesion.query(WPCheckList).filter(or_(WPCheckList.comment>=30,WPCheckList.retweet>=50)).order_by(desc(WPCheckList.comment)).all()
		for x in  res:
			content+=('作者：%s 评论：%d  转发：%d <br/>内容：<a href="%s">%s</a><br/><br/>'%(x.screen_name,x.comment,x.retweet,x.url,x.text))

		m._send_default(to='arthur@infoq.com',subject=(WEIBO_MAIL_SUBJECT%(str(datetime.today()))),content=content)
		return render_template('wp_mail.html',r='ok')
class WPUserAdd(MethodView):
	def get(self):
		return render_template('wpuser_add.html')
	def  post(self):
		email=request.form['email']
		comment=request.form['comment']
		retweet=request.form['retweet']
		return render_template('')
class WPCheckView(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		res=dbSesion.query(WPCheckList).order_by(desc(WPCheckList.time)).limit(20)
		return render_template('wp_check.html',res=res)
	def post(self):
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		_token = session['token']
		_expires_in = session['expires_in']
		print _token,_expires_in
		client.set_access_token(_token,_expires_in)
		db_session=sessionmaker(bind=DB)
		dbSesion=db_session()
		helper=WPHelper()
		check_list=dbSesion.query(WPList).all()
		for p in check_list:
			result=client.get.statuses__user_timeline(feature=0,uid=p.uid,count=200,page=1)
			for mm in result.statuses:
				print mm.reposts_count
				m=WPCheckList(
				url="http://api.t.sina.com.cn/"+p.uid+"/statuses/"+str(mm.id)+"?source="+APP_KEY,
				time=datetime.strptime(mm.created_at,'%a %b %d %H:%M:%S +0800 %Y'),
				screen_name=p.screen_name,
				text=mm.text,
				retweet=mm.reposts_count,
				comment=mm.comments_count)
				
				helper.add_to_database(m)
		return  redirect('wpcheck')