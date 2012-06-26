# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import md5
import urllib2
import flask
from urllib2 import *
from modles import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from flask import *
from flask import request,render_template,session,redirect
from flask.views import MethodView
from sqlalchemy.orm import sessionmaker
import re
from helper_data import *
import string
import datetime
import helper_data
from functools import wraps
from helper_data import *
import urllib2
import json
from sqlalchemy.sql.expression import *
from sqlalchemy import and_, or_
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String
from datetime import *
from weibo import *
import logging
from logging.handlers import SMTPHandler
import string
import sys
from flask import g, request, redirect, url_for


reload(sys)
sys.setdefaultencoding('utf8') 

APP_KEY = '570026225'
APP_SECRET = '45ea1cae01eecda0e07a2b88a256d7a2'
CALLBACK_URL = 'http://127.0.0.1:5000/oauth'

DATABASE_USER = 'root'
DATABASE_PWD =''
DATABASE_NAME= 'test'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT='3306'
DB = create_engine('mysql://%s:%s@%s:%s/%s'% (DATABASE_USER,DATABASE_PWD,DATABASE_HOST,DATABASE_PORT,DATABASE_NAME),connect_args={'charset':'utf8'},echo=True,pool_recycle=3,pool_size=0)

Base = declarative_base()

RSS_SIGN_HOME='http://www.infoq.com/rss/rss.action?token=3Pkt2g0ELdPI6FKsXWnlhEytktoyTtAB'
RSS_NOT_SIGN_EN='http://www.infoq.com/rss/rss.action?token=3Pkt2g0ELdPI6FKsXWnlhEytktoyTtAB'
RSS_NOT_SIGN_CH='http://www.infoq.com/cn/rss/rss.action?token=mgnOPySplnVRGBQQHToikUWoAGFEqtDo'

Base = declarative_base()

WEIBO_MAIL_SUBJECT=u'【%s】InfoQ微博热报线索'
WEIBO_MAIL_LIST='arthur@infoq.com;frank.jia@infoq.com;kevin@infoq.com;core-editors@googlegroups.com'

SMILE_MAIL_SUBJECT=''
SMILE_MAIL_LIST=''

RSS_EN_MAIL_SUBJECT=''
RSS_CH_MAIL_SUBJECT=''
MAIL_SMTP='smtp.exmail.qq.com'
MAIL_TO='arthur@infoq.com;'
MAIL_FROM='notice@magicshui.com'
MAIL_PWD='shuishui123'
MAIL_SUBJECT=u"%s：InfoQ更新--%d篇新闻，%d篇文章，%d篇采访"

CATEGORY_LIST=['Development','Architecture & Design','Process & Practices','Enterprise Architecture','Operations & Infrastructure']
CATEGORY_LIST_CN=['']


def login(wtype='admin'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
                if 'user'  not in session:
                    return redirect(url_for('login', next=request.url))
                return f(*args, **kwargs)
        return decorated_function
    return decorator



def token():
        try:
            try:
                token=session['token']
                return True
            except:
                db_session=sessionmaker(bind=DB)
                dbSession=db_session()
                res=dbSession.query(TokenListInfo).order_by(desc(TokenListInfo.time)).all()
                if res:
                    session['token']=res[0].token
                    session['expire']=res[0].expire
                    return True
                else:
                    return redirect('go?msg="1"')
        except :
            return redirect('go?msg=error')

class UserListInfo(Base):
    __tablename__='user_list'
    user=Column(String(100),primary_key=True)
    pwd=Column(String(45))
    """docstring for UserListInfo"""
    def __init__(self, user,pwd):
        self.user=user
        self.pwd=pwd
        
            
class TokenListInfo(Base):
    __tablename__='token_list'
    time=Column(DateTime,primary_key=True)
    token=Column(String(200))
    expire=Column(String(400))
    level=Column(String(45))
    def __init__(self,time,token,expire,level):
        self.time=time
        self.token=token
        self.expire=expire
        self.level=level
class WeiboR():
    """docstring for WeiboR"""
    time=''
    title=''
    guid=''
    weibo=''
    retweet=0
    comment=0
    athur=''
    cat=''
    smallcat=''
    maincat=''
class MInfo():
    text = ''
    r=''
    c=''
    title=''
    t=''
    u=''
    a=''
    i=0
    l=''
    wu=''
    tr=''
'''
    this clas is for mapping to mysql table:all_rss
'''
class RssInfo(Base):
    __tablename__ = 'all_rss'
    title=Column(String(100),primary_key=True)
    pubdate=Column(DateTime)
    description=Column(String(200))
    guid=Column(String(1000))
    country=Column(String(45))
    category=Column(String(200))
    small_cat=Column(String(100))
    author=Column(String(100))
    main_cat=Column(String(100))
    def __init__(self,title,pubdate,description,guid,country,category,small_cat='',author='',main_cat=''):
        self.title=title
        self.pubdate=pubdate
        self.category=category
        self.country=country
        self.description=description
        self.guid=guid
        self.small_cat=small_cat
        self.author=author
        self.main_cat=main_cat

'''
    this class is for mapping to mysql table: new_list
'''
class RssNewInfo(Base):
    __tablename__ = 'new_list'
    title=Column(String(100),primary_key=True)
    pubdate=Column(DateTime)
    description=Column(String(200))
    guid=Column(String(1000))
    country=Column(String(45))
    category=Column(String(200))
    small_cat=Column(String(100))
    author=Column(String(100))
    def __init__(self,title,pubdate,description,guid,country,category,small_cat='',author=''):
        self.title=title
        self.pubdate=pubdate
        self.category=category
        self.country=country
        self.description=description
        self.guid=guid
        self.small_cat=small_cat
        self.author=author
        
class MailListInfo(Base):
    __tablename__='mail_list'
    id=Column(String(100),primary_key=True)
    email=Column(String(100),primary_key=True)
    country=Column(String(100))
    def  __init__(self,id,email,country):
        self.email=email
        self.id=id
        self.country=country
class WeiboM(Base):
    __tablename__='weibo_list'
    title=Column(String(100))
    url=Column(String(100))
    retweet=Column(Integer)
    comment=Column(Integer)
    athur=Column(String(100))
    cat=Column(String(100))
    time=Column(DateTime)
    text=Column(String(400))
    org_url=Column(String(400),primary_key=True)
    def __init__(self,title,url,retweet,comment,text,org_url,athur,cat,time):
        self.title=title
        self.url=url
        self.athur=athur
        self.cat=cat
        self.retweet=retweet
        self.time=time
        self.comment=comment
        self.text=text
        self.org_url=org_url
class WPList(Base):
    __tablename__='wp_list'
    uid=Column(String(100),primary_key=True)
    name=Column(String(100))
    screen_name=Column(String(100))
    cat=Column(String(100))
    def __init__(self,name,uid,screen_name,cat):
        self.uid=uid
        self.name=name
        self.screen_name=screen_name
        self.cat=cat
class WPCheckList(Base):
    __tablename__='wpcheck_list'
    time=Column(DateTime)
    url=Column(String(200),primary_key=True)
    text=Column(String(200))
    comment=Column(Integer)
    retweet=Column(Integer)
    screen_name=Column(String(100))
    def __init__(self,time,url,text,comment,retweet,screen_name):
        self.time=time
        self.url=url
        self.text=text
        self.comment=comment
        self.retweet=retweet
        self.screen_name=screen_name
class WPConfig(Base):
    __tablename__='wp_config'
    retweet=Column(Integer,primary_key=True)
    comment=Column(Integer)
    order=Column(String(100))
    relation=Column(String(100))
    def __init__(self,retweet,comment,order,relation):
        self.retweet=retweet
        self.relation=relation
        self.comment=comment
        self.order=order
        
class FeedBackList(Base):
    __tablename__='feedback_list'
    time=Column(DateTime,primary_key=True)
    content=Column(String(500))
    title=Column(String(45))
    def __init__(self,time,title,content):
          self.time=time
          self.title=title
          self.content=content 
          
          
class ExpertList(Base):
    __tablename__="expert_list"
    id = Column(String(30),primary_key=True)
    name=Column(String(45))
    ename=Column(String(45))
    email=Column(String(200))
    address=Column(String(200))
    location=Column(String(200))
    company=Column(String(200))
    phone=Column(String(45))
    im=Column(String(45))
    bank=Column(String(100))
    bio=Column(String(500))
    img=Column(String(200))
    weibo=Column(String(200))
    blog=Column(String(200))
    area=Column(String(200))
    birth=Column(DateTime)
    bid=Column(String(45))
    def __init__(self,id,name,ename,email,address,location,company,phone,im,bank,bio,
        img,weibo,blog,area,birth,bid):
        self.id=id
        self.name=name
        self.ename=ename
        self.email=email
        self.address=address
        self.location=location
        self.company=company
        self.phone=phone
        self.im=im
        self.bank=bank
        self.bio=bio
        self.img=img
        self.weibo=weibo
        self.blog=blog
        self.area=area
        self.birth=birth
        self.bid=bid

class JingyaoList(Base):
    __tablename__='jingyao_list'
    count=Column(String(10))
    id=Column(String(20),primary_key=True)
    img=Column(String(100))
    content=Column(String(1000))
    title=Column(String(30))
    head_url=Column(String(100))
    img_url=Column(String(100))
    cat=Column(String(10))
    def  __init__(self,count,content,title,head_url,cat,img_url='',img=''):
        self.count=count
        self.id=str(datetime.now())
        self.content=content
        self.title=title
        self.head_url=head_url
        self.img_url=img_url
        self.cat=cat
        self.img=img
                
class EditorWeiboList(Base):
    __tablename__='editorweibo_list'
    name=Column(String(100),primary_key=True)
    wname=Column(String(45))
    wid=Column(String(45))
    def __init__(self,name,wname,wid):
        self.name=name
        self.wname=wname
        self.wid=wid

class EditorCountWeiboList(Base):
    __tablename__='editorcount_list'
    guid=Column(String(100),primary_key=True)
    fname=Column(String(100))
    fcount=Column(Integer)
    fcomment=Column(String(100))
    sname=Column(String(100))
    scount=Column(Integer)
    scomment=Column(String(100))
    img=Column(String(200))
    def __init__(self,guid,fname,fcount,fcomment,sname,scount,scomment,img):
        self.guid=guid
        self.fname=fname
        self.fcount=fcount
        self.fcomment=fcomment
        self.sname=sname
        self.scount=scount
        self.scomment=scomment
        self.img=img
class EditorCount2List(Base):
    __tablename__='editorcount2_list'
    id=Column(String(20),primary_key=True)
    guid=Column(String(100))
    version=Column(Integer)
    name=Column(String(1))
    count=Column(Integer)
    comment=Column(String(100))
    img=Column(String(200))
    def __init__(self,version,guid='',name='',comment='',img='',count=0):
        self.id=md5.new(str(datetime.now())).hexdigest()
        self.guid=guid
        self.version=version
        self.name=name
        self.count=count
        self.comment=comment
        self.img=img
Clue_Pre="""
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
<div marginwidth="0" marginheight="0" style="min-width:600px;margin:0 auto;padding:39px;font-family:'Helvetica Neue',Helvetica,Arial,Sans-serif;font-size:13px;line-height:22px;background-color:#f5f5f5"><div class="adM">
    </div><table width="552" cellspacing="0" cellpadding="0" border="0" style="border:1px solid #dedede;border-bottom:2px solid #dedede;margin:0 auto;background-color:#ffffff">
    <tbody>
        
        <tr>
            <td align="center" style="padding:30px 25px 30px">
                <div style="font-size:13px">
                    <a target="_blank" href="http://zhi.hu/BAAC?m=edm.37.19039590023205" style="float:left;color:#bbb;text-decoration:none;border:none;outline:none">InfoQ</a>                  
                    <span style="float:right;color:#bbb">%s</span>
                    <div style="font-size:25px;text-indent:3px">%s</div>
                </div>
            </td>
        </tr>
                    <tr>
            <td style="padding:0 25px 25px">
                
        """
Clue_Body="""<div style="margin-bottom:10px;border-bottom:1px dotted #dedede">
                    <div style="margin-bottom:3px">
                        <a target="_blank" href="%s" style="font-size:14px;line-height:22px;text-decoration:none;color:#259;border:none;outline:none">%s</a>
                    </div>
                    <div style="margin-bottom:3px;font-size:13px;line-height:22px">
                        <span style="float:right;color:#bbb">%s</span>
                        
                        <span style="color:#bbb">%s  %s</span>
                    </div>
                    <div style="margin-bottom:10px">
                        <span style="word-break:break-all;word-wrap:break-word;font-size:11px;line-height:22px;text-decoration:none;color:#333;display:block">%s</span>
                    </div>
                </div>
"""
Clue_End2="""       
                            </td>
        </tr>
            </tbody>
</table>
<div style="text-align:center;padding-top:10px;margin:0 auto;width:500px;color:#aaa;font-size:12px;line-height:20px">由 <a target="_blank" style="text-decoration:none;border:none;outline:none;color:#aaa!important" href="mailto:arthur@infoq.com">Arthur维护，意见或者建议请反馈给他！</a><br>InfoQ &copy; 2012<img width="0" height="0"><div class="yj6qo"></div><div class="adL">
</div></div><div class="adL">

</div></div></body>"""
Clue_End="""<div style="display:block;"><a target="_blank" href="http://gege.baihui.com/open.do?docid=95416000000003001" style="margin-left:40px;display:inline-block;padding:7px 15px;background-color:#d44b38;color:#fff;font-size:13px;font-weight:bold;border-radius:2px;border:solid 1px #c43b28;white-space:nowrap;text-decoration:none">新闻</a>
<a target="_blank" href="http://gege.baihui.com/docview.do?docid=95416000000004001" style="margin-right:40px;float:right;display:inline-block;padding:7px 15px;background-color:lightblue;color:#fff;font-size:13px;font-weight:bold;border-radius:2px;border:solid 1px lightblue;white-space:nowrap;text-decoration:none">文章</a><div style="float:right;color:#bbb;font-size:13px">
                    </div><div style="margin-top:10px;margin-bottom:10px;border-bottom:1px dotted #dedede"><p style="float:right;color:#333;font-size:11px;">Raven</p></div>
                                                
                            </td>
        </tr>
            </tbody>
</table>
<div style="text-align:center;padding-top:10px;margin:0 auto;width:500px;color:#aaa;font-size:12px;line-height:20px">由 <a target="_blank" style="text-decoration:none;border:none;outline:none;color:#aaa!important" href="mailto:arthur@infoq.com">Arthur维护，意见或者建议请反馈给他！</a><br>InfoQ &copy; 2012<img width="0" height="0"><div class="yj6qo"></div><div class="adL">
</div></div><div class="adL">

</div></div></body>"""
WEIBO_MAIL_CONTENT_BASE1="""


<div id="mailContentContainer" style="background:#ECECEC;font-size: 14px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; height: auto; font-family: 'lucida Grande', Verdana; margin-right: 170px; ">

    <title></title>
<style type="text/css">
body{background:#ECECEC;font-family:"lucida Grande",Verdana;}
.invite{width:606px;margin:0 auto;overflow:hidden;}
.invite, .invite td, .invite th{border-collapse:collapse;padding:0;vertical-align:middle;}
.invite th{font-weight:bold;font-size:16px;color:white;text-align:left;background:#3B5999;}
.invite th .mailLogo{margin:0 5px -6px 0; padding:0 0 0 30px;}
.invite th div{height:65px;overflow:hidden;}
.invite .borderLeft{width:4px;*width:3px;border-left:1px solid #EBEBEB;border-right:1px solid #C9C9C9;background:#E9E9E9;}
.invite .borderRight{width:3px;border-left:1px solid #C9C9C9;border-right:1px solid #EBEBEB;background:#E9E9E9;}
.invite h2{margin:26px 34px 16px;font-size:18px;font-weight:bold;}
.invite p{color:#313131;display:block;font-size:14px;line-height:150%;padding:1px 34px 21px;margin:0;}
.invite p.team, .invite p.team a{color:#999999;text-decoration:none;}
.invite p.team a:hover{color:#999999;text-decoration:underline;}
.invite a{color:#3B5999}
</style>


<div style="background:#ECECEC;">
<table class="invite" align="center" bgcolor="#ffffff" border="0" cellspacing="0" cellpadding="0">
    <tbody><tr>
        <td colspan="4" class="radius" style="vertical-align:bottom;overflow:hidden;line-height:6px;"><img src="http://exmail.qq.com/zh_CN/htmledition/images/newicon/sysmail/mail_invite_top.png" alt=""></td>
    </tr>
    <tr>
        <td rowspan="2" class="border borderLeft"></td>
        <th width="416"><img src="http://cdn4.infoq.com/styles/cn/i/logo-infoq.gif" alt="InfoQ的送信人" class="mailLogo">微博热报线索</th>
        <th width="180"><div><img src="http://exmail.qq.com/zh_CN/htmledition/images/bizmail/top_biz.gif" class="mailBg"></div></th>
        <td rowspan="2" class="border borderRight"></td>
    </tr>
    <tr>
        <td colspan="2">
            
            """
WEIBO_MAIL_CONTENT_BASE2="""

            
            <p>
                祝您使用愉快。如果有任何疑惑，欢迎发信至 <a href="mailto:arthur@infoq.com" target="_blank">arthur@infoq.com</a> 获取帮助。
            </p>

            <p class="team">
             
                <span style="background:#ddd;height:1px;width:100%;overflow:hidden;display:block;margin:2px 0;"></span>
                InfoQ中文站：<a href="http://infoq.com/cn" target="_blank">http://infoq.com/cn</a><br>
                
            </p>
        </td>
    </tr>
    <tr>
        <td colspan="4" style="vertical-align:top;line-height:5px;overflow:hidden;"><img src="http://exmail.qq.com/zh_CN/htmledition/images/newicon/sysmail/mail_invite_bottom.png" alt=""></td>
    </tr>
</tbody></table>
</div>
 </div>
"""
WEIBO_MAIL_CONTENT_BLOCK="""

<p>
                <img src="http://exmail.qq.com/zh_CN/htmledition/images/bizmail/icon_addr.gif" style="vertical-align:middle;margin-right:4px" height="18" width="18px">
                <strong>%s</strong>   评论%d   转发 %d<br>
                <span style="margin-left:27px;"><a  style="color:gray;text-decoration:none;font-size:13px;" href='%s'>%s</a></span>
            </p>
"""       