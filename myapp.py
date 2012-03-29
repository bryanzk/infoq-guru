# -*- coding: utf-8 -*-
from flask import Flask
from action_rss import *
from action_weibo import *
from action_editor import *
from action_static import *
from action_user import *
from action_mail import *
from action_task import *
from config import *
from md5 import md5
app = Flask(__name__)
app.debug=True
app.secret_key='fakdfakjbdfjasdfa&fasdfa'

app.add_url_rule('/rss',view_func=RssFetchRefresh.as_view('rss'))
app.add_url_rule('/taskadd',view_func=TaskAddNew.as_view('taskadd'))
app.add_url_rule('/taskstep',view_func=TaskToStep.as_view('taskstep'))
app.add_url_rule('/taskstepinfo',view_func=TaskStepInfo.as_view('taskstepinfo'))
app.add_url_rule('/tasksubmit',view_func=TaskSubmit.as_view('tasksubmit'))
app.add_url_rule('/rsssearch',view_func=RssNew.as_view('newrss'))
app.add_url_rule('/rssen',view_func=EnRssRefresh.as_view('rssen'))
app.add_url_rule('/rssch',view_func=ChRssRefresh.as_view('rssch'))
app.add_url_rule('/edone',view_func=EditorAbout.as_view('adone'))
app.add_url_rule('/mail',view_func=MailView.as_view('mail'))
app.add_url_rule('/login',view_func=UserLogin.as_view('login'))
app.add_url_rule('/error',view_func=ErrorView.as_view('error'))
app.add_url_rule('/mailadd',view_func=MailAddView.as_view('mailadd'))
app.add_url_rule('/maildel',view_func=MailDeleteView.as_view('maildel'))
app.add_url_rule('/editor',view_func=EditorView.as_view('editor'))
app.add_url_rule('/',view_func=IndexView.as_view('index'))
app.add_url_rule('/staticrss',view_func=StaticView.as_view('static_view'))
app.add_url_rule('/about',view_func=AboutView.as_view('aboutview'))
app.add_url_rule('/weibor',view_func=WeiboRefresh.as_view('nedw'))
app.add_url_rule('/weibos',view_func=WeiboSend.as_view('weibosend'))
app.add_url_rule('/go',view_func=GotoOauth.as_view('newa'))
app.add_url_rule('/oauth',view_func=ComebackOauth.as_view('neddw'))
app.add_url_rule('/wa',view_func=ShowAll.as_view('wa'))
app.add_url_rule('/weiboresult',view_func=WeiboResult.as_view('weiboresult'))
app.jinja_env.globals.update(md5=md5)
if __name__=='__main__':
    app.run()
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def interal_error(e):
	raise
	return render_template('500.html',msg=str(e)),500