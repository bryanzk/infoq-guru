# -*- coding: utf-8 -*-
from flask import Flask
from action_rss import *
from action_weibo import *
from action_editor import *
from action_static import *
from action_user import *
from action_mail import *
from action_task import *
from action_check import *
from action_charts import *
from action_top import *
from action_feedback import *
from action_aboutus import *
from action_timeline import *
from action_mag import *
from action_expert import *
from action_jingyao import *
from action_fee import *
from action_clue import *
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
app.add_url_rule('/logout',view_func=UserLogout.as_view('logut'))

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
app.add_url_rule('/wpadd',view_func=WPAddView.as_view('wpadd'))
app.add_url_rule('/wpcheck',view_func=WPCheckView.as_view('wpcheck'))
app.add_url_rule('/wpmail',view_func=WPSend.as_view('wpmail'))
app.add_url_rule('/wpconfig',view_func=WPConfigView.as_view('wpconfig'))

app.add_url_rule('/weibochart',view_func=WeiboChart.as_view('WeiboChart'))
app.add_url_rule('/weibochartc',view_func=WeiboCommentView.as_view('weibocommentview'))
app.add_url_rule('/feedback',view_func=FeedbackView.as_view('feedbackview'))
app.add_url_rule('/aboutus',view_func=AboutusEditor.as_view('aboutus'))
app.add_url_rule('/lab',view_func=Labs.as_view('labs'))
app.add_url_rule('/timeline',view_func=TimeLine.as_view('timeline'))
app.add_url_rule('/timelinedata',view_func=TimeLineData.as_view('timelinedata'))
app.add_url_rule('/urltop',view_func=TopView.as_view('topviewurl'))
app.add_url_rule('/mag',view_func=MagView.as_view('mag'))
app.add_url_rule('/eupdate',view_func=ExpertUpdate.as_view('eupdate'))
app.add_url_rule('/eadd',view_func=ExpertAdd.as_view('eadd'))
app.add_url_rule('/es',view_func=ExpertSearch.as_view('es'))
app.add_url_rule('/eshow',view_func=ExpertShow.as_view('eshow'))
app.add_url_rule('/jingyao',view_func=JingyaoOut.as_view('jingyao'))
app.add_url_rule('/jyi',view_func=JingyaoInput.as_view('jingyaoi'))
app.add_url_rule('/jya',view_func=JingyaoAds.as_view('jingyaoa'))

app.add_url_rule('/fimport',view_func=ImportDataToArticles.as_view('fimport'))
app.add_url_rule('/flist',view_func=FeeArticleList.as_view('flist'))
app.add_url_rule('/fshow',view_func=ShowArticleData.as_view('fshow'))
app.add_url_rule('/fweibo',view_func=FeeArticleWeibo.as_view('fweibo'))

app.add_url_rule('/trellotougao',view_func=TrelloTougao.as_view('tougao'))
app.add_url_rule('/trellosend',view_func=TrelloSend.as_view('trellosend'))
app.add_url_rule('/trello',view_func=TrelloTest.as_view('trelo'))
app.add_url_rule('/trellodone',view_func=TrelloDone.as_view('trelodone'))


app.jinja_env.globals.update(md5=md5)
if __name__=='__main__':
    app.run()
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def interal_error(e):
	raise
	return render_template('500.html',msg=str(e)),500'''