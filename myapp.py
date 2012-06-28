# -*- coding: utf-8 -*-
from flask import Flask
from action_rss import *
from action_weibo import *
from action_editor import *
from action_static import *
from action_user import *
from action_mail import *
from action_check import *
from action_top import *
from action_smile import *
from action_feedback import *
from action_timeline import *
from action_jingyao import *
from action_expert import *
from action_clue import *
from action_editor2 import *
from action_count import *
from action_index import *
from action_bean import *
from action_notify import *

from config import *

app = Flask(__name__)
app.debug=True
app.secret_key='fakdfakjbdfj#2342#FsDF>,d.fapla&fasdfa'

@app.route('/')
def login_not():
	return render_template('user_login.html')
app.add_url_rule('/rss',view_func=RssFetchRefresh.as_view('rss'))

app.add_url_rule('/rsssearch',view_func=RssNew.as_view('newrss'))
app.add_url_rule('/rssen',view_func=EnRssRefresh.as_view('rssden'))
app.add_url_rule('/rssch',view_func=ChRssRefresh.as_view('rsscdh'))
app.add_url_rule('/edone',view_func=EditorAbout.as_view('adone'))
app.add_url_rule('/mail',view_func=MailView.as_view('mail'))
app.add_url_rule('/mailen',view_func=MailEnView.as_view('mailen'))
app.add_url_rule('/mailch',view_func=MailChView.as_view('maailch'))

app.add_url_rule('/login',view_func=UserLogin.as_view('login'))
app.add_url_rule('/error',view_func=ErrorView.as_view('error'))



app.add_url_rule('/mailadd',view_func=MailAddView.as_view('madiladd'))
app.add_url_rule('/maildel',view_func=MailDeleteView.as_view('maildel'))
app.add_url_rule('/editor',view_func=EditorView.as_view('editor'))
app.add_url_rule('/',view_func=IndexView.as_view('index'))
app.add_url_rule('/staticrss',view_func=StaticView.as_view('static_adview'))
app.add_url_rule('/about',view_func=AboutView.as_view('aboutview'))
app.add_url_rule('/weibor',view_func=WeiboRefresh.as_view('weibor'))
app.add_url_rule('/weibos',view_func=WeiboSend.as_view('weibos'))
app.add_url_rule('/go',view_func=GotoOauth.as_view('go'))
app.add_url_rule('/oauth',view_func=ComebackOauth.as_view('oauth'))
app.add_url_rule('/wa',view_func=ShowAll.as_view('wa'))
app.add_url_rule('/weiboresult',view_func=WeiboResult.as_view('weiboresult'))
app.add_url_rule('/wpadd',view_func=WPAddView.as_view('wpadd'))
app.add_url_rule('/wpcheck',view_func=WPCheckView.as_view('wpcheck'))
app.add_url_rule('/wpmail',view_func=WPSend.as_view('wpmail'))
app.add_url_rule('/wpconfig',view_func=WPConfigView.as_view('wpconfig'))

app.add_url_rule('/dutymail',view_func=DutyMail.as_view('dutymail'))
app.add_url_rule('/smilemail',view_func=SmileMail.as_view('smilemail'))
app.add_url_rule('/invoicemail',view_func=InvoiceMail.as_view('invoicemail'))
app.add_url_rule('/urltop',view_func=TopView2.as_view('topviewurl'))
app.add_url_rule('/feedback',view_func=FeedbackView.as_view('feedbackview'))


app.add_url_rule('/timeline',view_func=TimeLine.as_view('timeline'))
app.add_url_rule('/timelinedata',view_func=TimeLineData.as_view('timelinedata'))

app.add_url_rule('/jingyao',view_func=JingyaoOut.as_view('jingyao'))
app.add_url_rule('/jyi',view_func=JingyaoInput.as_view('jingyaoi'))
app.add_url_rule('/jya',view_func=JingyaoAds.as_view('jingyaoa'))



app.add_url_rule('/eupdate',view_func=ExpertUpdate.as_view('eupdate'))
app.add_url_rule('/eadd',view_func=ExpertAdd.as_view('eadd'))
app.add_url_rule('/es',view_func=ExpertSearch.as_view('es'))
app.add_url_rule('/eshow',view_func=ExpertShow.as_view('eshow'))


app.add_url_rule('/trellosend',view_func=TrelloSend.as_view('trellosend'))
app.add_url_rule('/trello',view_func=TrelloTest.as_view('trelo'))
app.add_url_rule('/trellodone',view_func=TrelloDone.as_view('trelodone'))



app.add_url_rule('/editorweibo',view_func=EditorWeibo.as_view('editorweibo'))
app.add_url_rule('/editorcountall',view_func=EditorCountListAll.as_view('editorcountall'))
app.add_url_rule('/editorshow',view_func=EditorCountShow2.as_view('editorshow'))
app.add_url_rule('/editorshare',view_func=RssWeiboShare2.as_view('ediotrweiboshare'))

app.add_url_rule('/editorcountall2',view_func=EditorCountListAll.as_view('editorcountall2'))
app.add_url_rule('/editorshow2',view_func=EditorCountShow2.as_view('editorshow2'))
app.add_url_rule('/editorshare2',view_func=RssWeiboShare2.as_view('ediotrweiboshare2'))
#used for convert from cn_contents into editor2list
app.add_url_rule('/_convert',view_func=ConvertToNew.as_view('convettonew'))
app.add_url_rule('/_2convert',view_func=ConvertToNew2.as_view('convert2view'))



app.add_url_rule('/countsearch',view_func=CountSearch.as_view('countsearch'))
app.add_url_rule('/countauthor',view_func=CountAuthor.as_view('countauthor'))
app.add_url_rule('/countstatics',view_func=CountStatics.as_view('countstatics'))
app.add_url_rule('/countstaticsmail',view_func=CountStaticsMail.as_view('contentdashboardmail'))
app.add_url_rule('/contentdashboard',view_func=CountStatics.as_view('contentdashboard'))
app.add_url_rule('/countweek',view_func=CountWeek.as_view('countweek'))
app.add_url_rule('/countweekauthor',view_func=CountWeekAuthor.as_view('countweekauthor'))
app.add_url_rule('/countwall',view_func=CountWall.as_view('countwall'))
app.add_url_rule('/countstatics2',view_func=CountStatics2.as_view('countstati2cs2'))


app.add_url_rule('/countstatics2lastweek',view_func=CountStatics2LastWeek.as_view('countstatics2lastweek'))

app.add_url_rule('/od',view_func=CountOD.as_view('od'))
app.add_url_rule('/setmaincatall',view_func=RssSetMainCatAll.as_view('setmaincatall'))
app.add_url_rule('/Persona-Setup',view_func=RssSetMainCatAll.as_view('setmaincatall'))
app.add_url_rule('/setmaincat',view_func=RssSetMainCat.as_view('setmaincat'))
app.add_url_rule('/changemaincatall',view_func=RssChangeMainCatAll.as_view('setchangemaincatall'))

app.add_url_rule('/search',view_func=GoogleSearch.as_view('googlesearch'))
app.add_url_rule('/mailbryan',view_func=BryanMail.as_view('bryanview'))
app.add_url_rule('/maildb',view_func=DashboardMail.as_view('dashboardmail'))



app.add_url_rule('/notifyget',view_func=NotifyGet.as_view('getnotify'))
app.add_url_rule('/notifycenter',view_func=NotifyCenter.as_view('notifycenter'))



app.add_url_rule('/editor-index',view_func=EditorIndex.as_view('editorindex'))
app.add_url_rule('/beannewspick',view_func=NewsBeanToPick.as_view('beannewspick'))
app.add_url_rule('/pickabean',view_func=PickABean.as_view('pickabean'))
app.add_url_rule('/_beans',view_func=Convet_Beans.as_view('convetbeans'))
app.add_url_rule('/beannewstodone',view_func=NewsBeanToDone.as_view('beannewstodone'))
app.add_url_rule('/doneabean',view_func=DoneABean.as_view('doneabean'))
app.add_url_rule('/beanpending',view_func=BeanPendingNews.as_view('pendingbeans'))
app.add_url_rule('/core-index',view_func=GofIndex.as_view('coreindex'))
app.add_url_rule('/admin-index',view_func=GofIndex.as_view('adminindex'))

app.add_url_rule('/gof-index',view_func=GofIndex.as_view('gofindex'))
app.add_url_rule('/gof36notpick',view_func=GOF36NotPickNews.as_view('gof36notpick'))
app.add_url_rule('/gof36notdone',view_func=GOF36NotDoneNews.as_view('gof36notdone'))

if __name__=='__main__':
	app.run()
@app.teardown_request
def logit():
	if not request.url.findall('notifyget')>0:
		notify_m(content='动作：'+str(request.url)+"地址："+str(request.remote_addr))

@app.errorhandler(404)
def page_not_found(e):
    notify_m(content='出现错误：'+str(request.url)+"地址："+str(request.remote_addr))
    return render_template('404.html'), 404
@app.errorhandler(500)
def interal_error(e):
	notify_m(content='出现错误：'+str(request.url)+"地址："+str(request.remote_addr)+"输入："+str(request.form))
	return render_template('500.html',msg=str(e)),500
 
 