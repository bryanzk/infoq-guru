# -*- coding: utf-8 -*-
import os
if 'SERVER_SOFTWARE' in os.environ:
    # Local
	from config import *
	from sae.mail import send_mail
	from helper_data import WeiboHelper
	from email.mime.text import MIMEText
	class MailView(MethodView):
		def get(self):
			
			return render_template("mailresult.html",r='')
		def post(self):
			country=request.form['country']
			if country=='en':
				x=MailEnView()
				return x.post()
			elif country=='ch':
				x=MailChView()
				return x.post()

	class MailEnView(MethodView):
		def post(self):
			m=MailMethod()
			m._en()

			return render_template('mailresult.html',r='ok')
	class MailChView(MethodView):
		def post(self):
			m=MailMethod()
			m._ch()

			return render_template('mailresult.html',r='ok')
	class MailMethod():
		def _send_default(self,to,subject,content):
			m = EmailMessage()
			m.to = to
			m.subject =subject
			m.html = content
	               # m.FromName=u'渡鸦'
			m.smtp = (MAIL_SMTP, 25,MAIL_FROM,MAIL_PWD, False)
			m.send()
			return True
		def _send(self,country):
			begin=date.today()-timedelta(days=1)
			end=date.today()
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country==country).filter(RssInfo.pubdate<end).order_by(RssInfo.pubdate).all()
			#content=u'<strong>更新内容</strong><br>'
			content=(Clue_Pre%(str(date.today()-timedelta(days=1)),'中文站更新'))
	                for  x in res:
				content+=Clue_Body%(x.guid,x.title,str(x.pubdate),'o_o','^_^',x.description)
	                        #content+=u"时间：%s<br>标题：%s <br> 地址：<a href='%s'>%s</a><br><br>" % (x.pubdate,x.title,x.guid,x.guid)
			#content+=u"深度内容列表：<a href='http://gege.baihui.com/docview.do?docid=95416000000004001'>http://gege.baihui.com/docview.do?docid=95416000000004001</a> "
			content+=Clue_End
	                mails=dbSession.query(MailListInfo).filter(MailListInfo.country==country).all()
			mail_to=u''
			for x in mails:
				mail_to+=(x.email+';')
			subject='InfoQ中文站更新%s'%str(datetime.today())[0:10]
			self._send_default(mail_to,subject,content=content)
			return 'ok'
		def _send_en(self,country):
			begin=date.today()-timedelta(days=1)
			end=date.today()
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country==country).filter(RssInfo.pubdate<end).order_by(RssInfo.pubdate).all()
			#content=u'<strong>更新内容</strong><br><br>'
			content=(Clue_Pre%(str(date.today()-timedelta(days=1)),"英文站更新"))
	                _news=0
			_articles=0
			_pres=0
			_minis=0
			_inter=0
			for  x in res:
				_h=WeiboHelper()
				if _h._get_cats(x.guid)==u'新闻':
					_news+=1
				elif _h._get_cats(x.guid)==u'文章':
					_articles+=1
				elif _h._get_cats(x.guid)==u'演讲':
					_pres+=1	
				elif _h._get_cats(x.guid)==u'采访':
					_inter+=1
				elif _h._get_cats(x.guid)==u'迷你书':
					_minis+=1	
				_category=""
				_cc=x.category.split(',')
				for xx in _cc:
					if xx in CATEGORY_LIST:
							_category+=" "+xx
				if _h._get_cats(x.guid)!=u'演讲':
					content+=Clue_Body%(x.guid,x.title,str(x.pubdate),_h._get_cats(x.guid),_category,x.guid)
	                                #content+=u"%s<br>%s <br><a href='%s'>%s</a><br>所属社区：%s<br><br>" % (_h._get_cats(x.guid),x.title,x.guid,x.guid,_category)
			#content+=u"新闻列表：<a href='http://gege.baihui.com/open.do?docid=95416000000003001'>http://gege.baihui.com/open.do?docid=95416000000003001</a><br/><br/>"
			#content+=u"深度内容列表：<a href='http://gege.baihui.com/docview.do?docid=95416000000004001'>http://gege.baihui.com/docview.do?docid=95416000000004001</a> "
			content+=Clue_End
	                mails=dbSession.query(MailListInfo).filter(MailListInfo.country==country).all()
			mail_to=u''
			for x in mails:
				mail_to+=(x.email+';')
			
			subject= MAIL_SUBJECT % (begin,_news,_articles,_inter)
			self._send_default(mail_to,subject,content=content)
			return True
		def _en(self):

			self._send_en('en')
		def _ch(self):
			self._send('ch')
	class MailDeleteView(MethodView):
		def get(self):
	        	db_session=sessionmaker(bind=DB)
	                dbSession=db_session()
			res=dbSession.query(MailListInfo).all()
			return render_template('maildel.html',r='ok',res=res)
		def post(self):
		 	email=request.form['email']
			country=request.form['country']
	                db_session=sessionmaker(bind=DB)
	                dbSession=db_session()
			x=dbSession.query(MailListInfo).filter(MailListInfo.email==email).filter(MailListInfo.country==country).all()
			for _x in x:
				dbSession.delete(_x)
			dbSession.commit()
			return redirect('maildel')
	class MailAddView(MethodView):
		def get(self):
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(MailListInfo).all()

			return render_template('mailadd.html',r='',res=res)
		def post(self):
			email=request.form['email']
			country=request.form['country']
			id=country+":"+email
			x=MailListInfo(id=id,email=email,country=country)
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			dbSession.add(x)
			dbSession.commit()
			return redirect('mailadd')
else:
	from config import *
	import smtplib
	from helper_data import WeiboHelper
	from email.mime.text import MIMEText
	class MailView(MethodView):
		def get(self):
			
			return render_template("mailresult.html",r='')
		def post(self):
			country=request.form['country']
			if country=='en':
				x=MailEnView()
				return x.post()
			elif country=='ch':
				x=MailChView()
				return x.post()

	class MailEnView(MethodView):
		def post(self):
			m=MailMethod()
			m._en()

			return render_template('mailresult.html',r='ok')
	class MailChView(MethodView):
		def post(self):
			m=MailMethod()
			m._ch()

			return render_template('mailresult.html',r='ok')
	class MailMethod():
		def _send_default(self,to,subject,content):
			msg=MIMEText(content.encode('utf8'),'html')
			msg['Subject']=subject
			msg['To']=to
			msg['From']=u" InfoQ 渡鸦 "
			msg['Nick']=u'InfoQd渡鸦'
			s=smtplib.SMTP()
			s.connect(MAIL_SMTP)
			s.login(MAIL_FROM,MAIL_PWD)
			s.sendmail(MAIL_FROM, to, msg.as_string())
			s.close()
			return True
		def _send(self,country):
			begin=date.today()-timedelta(days=1)
			end=date.today()
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country==country).filter(RssInfo.pubdate<=end).order_by(RssInfo.pubdate).all()
			content=u'<strong>更新内容</strong><br>'
			for  x in res:
				content+=u"时间：%s<br>标题：%s <br> 地址：<a href='%s'>%s</a><br><br>" % (x.pubdate,x.title,x.guid,x.guid)
			content+=u"深度内容列表：<a href='http://gege.baihui.com/docview.do?docid=95416000000004001'>http://gege.baihui.com/docview.do?docid=95416000000004001</a> "
			mails=dbSession.query(MailListInfo).filter(MailListInfo.country==country).all()
			mail_to=u''
			for x in mails:
				mail_to+=(x.email+';')
			msg = MIMEText(content.encode('utf-8'),'html')
			msg['Subject'] =  MAIL_SUBJECT % (begin,_news,_articles,_pres)
			msg['From'] = u"InfoQ 渡鸦<notice@magicshui.com>"
			msg['To'] = mail_to
			s = smtplib.SMTP()
			s.connect(MAIL_SMTP)
			s.login(MAIL_FROM,MAIL_PWD)
			s.sendmail(MAIL_FROM, mail_to, msg.as_string())
			s.close()
		def _send_en(self,country):
			begin=date.today()-timedelta(days=1)
			end=date.today()
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country==country).filter(RssInfo.pubdate<=end).order_by(RssInfo.pubdate).all()
			content=u'<strong>更新内容</strong><br><br>'
			_news=0
			_articles=0
			_pres=0
			_minis=0
			_inter=0
			for  x in res:
				_h=WeiboHelper()
				if _h._get_cats(x.guid)==u'新闻':
					_news+=1
				elif _h._get_cats(x.guid)==u'文章':
					_articles+=1
				elif _h._get_cats(x.guid)==u'演讲':
					_pres+=1	
				elif _h._get_cats(x.guid)==u'采访':
					_inter+=1
				elif _h._get_cats(x.guid)==u'迷你书':
					_minis+=1	
				_category=""
				_cc=x.category.split(',')
				for xx in _cc:
					if xx in CATEGORY_LIST:
							_category+=" "+xx
				if _h._get_cats(x.guid)!=u'演讲':
					content+=u"%s<br>%s <br><a href='%s'>%s</a><br>所属社区：%s<br><br>" % (_h._get_cats(x.guid),x.title,x.guid,x.guid,_category)
			content+=u"新闻列表：<a href='http://gege.baihui.com/open.do?docid=95416000000003001'>http://gege.baihui.com/open.do?docid=95416000000003001</a><br/>"
			content+=u"深度内容列表：<a href='http://gege.baihui.com/docview.do?docid=95416000000004001'>http://gege.baihui.com/docview.do?docid=95416000000004001</a> "
			mails=dbSession.query(MailListInfo).filter(MailListInfo.country==country).all()
			mail_to=u''
			for x in mails:
				mail_to+=(x.email+';')
			msg = MIMEText(content.encode('utf-8'),'html')
			msg['Subject'] =  MAIL_SUBJECT % (begin,_news,_articles,_inter)
			msg['From'] =u"InfoQ 渡鸦<notice@magicshui.com>"
			msg['To'] = mail_to
			s = smtplib.SMTP()
			s.connect(MAIL_SMTP)
			s.login(MAIL_FROM,MAIL_PWD)
			s.sendmail(MAIL_FROM, mail_to, msg.as_string())
			s.close()		
		def _en(self):

			self._send_en('en')
		def _ch(self):
			self._send('ch')
	class MailDeleteView(MethodView):
		def get(self):
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(MailListInfo).all()
			return render_template('maildel.html',r='ok',res=res)
		def post(self):
		 	email=request.form['email']
			country=request.form['country']
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			x=dbSession.query(MailListInfo).filter(MailListInfo.email==email).filter(MailListInfo.country==country).all()
			for _x in x:
				dbSession.delete(_x)
			dbSession.commit()
			return redirect('maildel')
	class MailAddView(MethodView):
		def get(self):
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			res=dbSession.query(MailListInfo).all()

			return render_template('mailadd.html',r='',res=res)
		def post(self):
			email=request.form['email']
			country=request.form['country']
			id=country+":"+email
			x=MailListInfo(id=id,email=email,country=country)
			db_session=sessionmaker(bind=DB)
			dbSession=db_session()
			dbSession.add(x)
			dbSession.commit()
			return redirect('mailadd')