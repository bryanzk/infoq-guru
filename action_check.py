# -*- coding: utf-8 -*-
# 获取每天的微博数据，过滤以后发送给编辑群组
from config import *
from action_mail import *
class WPHelper():
	def is_uid_exists(self,uid):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(WPList).filter(WPList.uid==uid).all()
		dbSession.close()
		if  r:
			return True
		else:
			return False
	def add_to_database(self,w):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(WPCheckList).filter(WPCheckList.url==w.url).first()
		if r:
			dbSession.delete(r)
		dbSession.add(w)
		
		dbSession.commit()
	def add_to_wp(self,w):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(WPList).filter(WPList.uid==w.uid).first()
		if r:
			dbSession.delete(r)
		dbSession.add(w)
		
		dbSession.commit()
		dbSession.close()

class WPAddView(MethodView):
	"""docstring for WPCheckView"""
	def get(self):
		
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(WPList).all()
		dbSession.close()
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
		dbSession=db_session()
		helper=WPHelper()
		if not helper.is_uid_exists(uid):
			dbSession.add(u)
			dbSession.commit()

		return redirect('wpadd')

class WPSend(MethodView):
	def get(self):
		
		token()
		return render_template('wp_mail.html')
	def post(self):
		token()
		m=MailMethod()
		content=''
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		begin=date.today()
		end=date.today()+timedelta(days=1)
		xx=dbSession.query(WPConfig).first()
		if xx.order=='retweet':
			if xx.relation=='and':
				res=dbSession.query(WPCheckList).filter(WPCheckList.time>begin).filter(WPCheckList.time<end).filter(and_(WPCheckList.comment>=xx.comment,WPCheckList.retweet>=xx.retweet)).order_by(desc(WPCheckList.retweet)).all()
			else:
				res=dbSession.query(WPCheckList).filter(WPCheckList.time>begin).filter(WPCheckList.time<end).filter(or_(WPCheckList.comment>=xx.comment,WPCheckList.retweet>=xx.retweet)).order_by(desc(WPCheckList.retweet)).all()
		else:
			if xx.relation=='and':
				res=dbSession.query(WPCheckList).filter(WPCheckList.time>begin).filter(WPCheckList.time<end).filter(and_(WPCheckList.comment>=xx.comment,WPCheckList.retweet>=xx.retweet)).order_by(desc(WPCheckList.comment)).all()
			else:
				res=dbSession.query(WPCheckList).filter(WPCheckList.time>begin).filter(WPCheckList.time<end).filter(or_(WPCheckList.comment>=xx.comment,WPCheckList.retweet>=xx.retweet)).order_by(desc(WPCheckList.comment)).all()	
		
		for x in  res:
			content+=(WEIBO_MAIL_CONTENT_BLOCK%(x.screen_name,x.comment,x.retweet,x.url,x.text))
			#content+=('作者：%s 评论：%d  转发：%d <br/>内容：<a href="%s">%s</a><br/><br/>'%(x.screen_name,x.comment,x.retweet,x.url,x.text))
		content=(WEIBO_MAIL_CONTENT_BASE1+content)
		content+=WEIBO_MAIL_CONTENT_BASE2
		m._send_default(to=WEIBO_MAIL_LIST,subject=(WEIBO_MAIL_SUBJECT%(str(datetime.today())[0:10])),content=content)
		return render_template('wp_mail.html',r='ok')
class WPConfigView(MethodView):
	def get(self):
		
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(WPConfig).first()
		dbSession.close()
		return render_template('wp_config.html',res=r)
	def post(self):
		retweet=request.form['retweet']
		comment=request.form['comment']
		order=request.form['order']
		relation=request.form['relation']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(WPConfig).all()
		r[0].retweet=retweet
		r[0].relation=relation
		r[0].comment=comment
		r[0].order=order
		dbSession.commit()
		dbSession.close()
		return redirect('wpconfig')
class WPCheckView(MethodView):
	def get(self):
		
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(WPCheckList).order_by(desc(WPCheckList.time)).limit(20)
		return render_template('wp_check.html',res=res)
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(TokenListInfo).order_by(desc(TokenListInfo.time)).all()

		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		_token = res[0].token
		_expires_in = res[0].expire
		print _token,_expires_in
		client.set_access_token(_token,_expires_in)
		
		helper=WPHelper()
		check_list=dbSession.query(WPList).all()
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