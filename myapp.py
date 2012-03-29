# -*- coding: utf-8 -*-
from flask import Flask
from action_rss import *
from action_weibo import *
from action_editor import *
from action_static import *
from action_mail import *
from config import *
app = Flask(__name__)
app.debug=True
app.secret_key='fakdfakjbdfjasdfa&fasdfa'

app.add_url_rule('/rss',view_func=RssFetchRefresh.as_view('rss'))

app.add_url_rule('/rsssearch',view_func=RssNew.as_view('newrss'))
app.add_url_rule('/rssen',view_func=EnRssRefresh.as_view('rssen'))
app.add_url_rule('/rssch',view_func=ChRssRefresh.as_view('rssch'))
app.add_url_rule('/edone',view_func=EditorAbout.as_view('adone'))
app.add_url_rule('/mail',view_func=MailView.as_view('mail'))
app.add_url_rule('/mailadd',view_func=MailAddView.as_view('mailadd'))
app.add_url_rule('/maildel',view_func=MailDeleteView.as_view('maildel'))
app.add_url_rule('/editor',view_func=EditorView.as_view('editor'))
app.add_url_rule('/',view_func=IndexView.as_view('index'))
app.add_url_rule('/staticrss',view_func=StaticView.as_view('static_view'))
app.add_url_rule('/about',view_func=AboutView.as_view('aboutview'))
app.add_url_rule('/weibor',view_func=WeiboRefresh.as_view('nedw'))
app.add_url_rule('/go',view_func=GotoOauth.as_view('newa'))
app.add_url_rule('/oauth',view_func=ComebackOauth.as_view('neddw'))
app.add_url_rule('/wa',view_func=ShowAll.as_view('wa'))
app.add_url_rule('/weiboresult',view_func=WeiboResult.as_view('weiboresult'))
if __name__=='__main__':
    app.run()
