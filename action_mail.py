# -*- coding: utf-8 -*-
from config import *
import smtplib
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
		msg['Subject'] = MAIL_SUBJECT % (date.today(),country)
		msg['From'] = MAIL_FROM
		msg['To'] = mail_to
		s = smtplib.SMTP()
		s.connect(MAIL_SMTP)
		s.login(MAIL_FROM,MAIL_PWD)
		s.sendmail(MAIL_FROM, mail_to, msg.as_string())
		s.close()
		
	def _en(self):

		self._send('en')
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
		x=MailListInfo(email=email,country=country)
                db_session=sessionmaker(bind=DB)
                dbSession=db_session()
		dbSession.add(x)
		dbSession.commit()
		return redirect('mailadd')