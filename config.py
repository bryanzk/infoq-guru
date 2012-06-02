# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
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
#RSS_SIGN_HOME='http://www.infoq.com/rss/rss.action?token=v94n6E2kapoNhNXc9EWTYRXoOoLLHX5S'
RSS_NOT_SIGN_EN='http://www.infoq.com/rss/rss.action?token=3Pkt2g0ELdPI6FKsXWnlhEytktoyTtAB'
RSS_NOT_SIGN_CH='http://www.infoq.com/cn/rss/rss.action?token=mgnOPySplnVRGBQQHToikUWoAGFEqtDo'

WEIBO_MAIL_SUBJECT=u'%s微博热点追踪'

WEIBO_MAIL_SUBJECT=u'【%s】InfoQ微博热报线索'
WEIBO_MAIL_LIST='arthur@infoq.com'

STATUS_STEP_LIST={"664":"737","737":"780","780":"800"}
MAIL_SMTP='smtp.exmail.qq.com'
MAIL_TO='arthur@infoq.com;hello.shuiyaya@gmail.com'
MAIL_FROM=u'notice@magicshui.com'
MAIL_PWD='shuishui123'
MAIL_SUBJECT=u"%s：InfoQ更新--%d篇新闻，%d篇文章，%d篇采访"
CATEGORY_LIST=['Development','Architecture & Design','Process & Practices','Enterprise Architecture','Operations & Infrastructure']
CATEGORY_LIST_CN=['']


def login():
        try:
                token=session['user']
                if toke:
                    return True
                else:
                    return redirect('error?msg="need login"&next=/login')
        except:
            return redirect('error?msg="need login"&next=/login')
def token():
        try:
            try:
                token=session['token']
                return f(*args,**kwargs)
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
    def __init__(self,title,pubdate,description,guid,country,category):
        self.title=title
        self.pubdate=pubdate
        self.category=category
        self.country=country
        self.description=description
        self.guid=guid
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
    def __init__(self,title,pubdate,description,guid,country,category):
        self.title=title
        self.pubdate=pubdate
        self.category=category
        self.country=country
        self.description=description
        self.guid=guid
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
class TaskList(Base):
    __tablename__='task_list'
    id=Column(String(100),primary_key=True)
    bigcat=Column(String(100))
    smallcat=Column(String(100))
    title=Column(String(100))
    link=Column(String(200))
    editor=Column(String(100))
    duty=Column(String(100))
    count=Column(Integer)
    def __init__(self,id,bigcat,smallcat,title,link,
        editor,duty,count):
        self.id=id
        self.bigcat=bigcat
        self.smallcat=smallcat
        self.title=title
        self.link=link
        self.editor=editor
        self.duty=duty
        self.count=count
class StatusList(Base):
    __tablename__='status_list'
    id=Column(String(100),primary_key=True)
    task_id=Column(String(100))
    code=Column(Integer)
    description=Column(String(200))
    begin=Column(DateTime)
    end=Column(DateTime)
    contrast=Column(DateTime)
    editor=Column(String(100))
    duty=Column(String(100))
    count=Column(Integer)
    def __init__(self,id,task_id,code,description,begin,end,contrast,editor,duty,count):
        self.id=id
        self.count=count
        self.task_id=task_id
        self.code=code
        self.description=description
        self.begin=begin
        self.end=end
        self.contrast=contrast
        self.editor=editor
        self.duty=duty
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
        self.retweet=comment
        self.screen_name=screen_name
class WPUserList(Base):
    __tablename__='wpuser_list'
    email=Column(String(100),primary_key=True)
    comment=Column(Integer)
    retweet=Column(Integer)
    def __init__(self,email,comment,retweet):
        self.email=email
        self.comment=comment
        self.retweet=retweet
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




class AboutusList(Base):
    __tablename__='about_list'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    ename=Column(String(100))
    email=Column(String(100))
    desc=Column(String(1000))
    minidesc=Column(String(200))
    area=Column(String(20))
    team=Column(String(20))
    img=Column(String(50))
    pinyin=Column(String(100))
    def __init__(self,id,name,ename,email,desc,minidesc,area,pinyin,team,img):
        self.id=id
        self.name=name
        self.ename=ename
        self.email=email
        self.desc=desc
        self.minidesc=minidesc
        self.area=area
        self.team=team
        self.img=img
        self.pinyin=pinyin
class InfoqList(Base):
    __tablename__='infoq_list'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    ename=Column(String(100))
    email=Column(String(100))
    desc=Column(String(500))
    title=Column(String(100))
    img=Column(String(100))
    pinyin=Column(String(100))
    def __init__(self,id,name,ename,email,desc,title,img,pinyin):
        self.id=id
        self.name=name
        self.ename=ename
        self.email=email
        self.pinyin=pinyin
        self.desc=desc
        self.title=title
        self.img=img

'''
  `id` VARCHAR(30) NOT NULL ,
  `name` VARCHAR(45) NULL ,
  `ename` VARCHAR(45) NULL ,
  `email` VARCHAR(200) NULL ,
  `address` VARCHAR(200) NULL ,
  `location` VARCHAR(200) NULL ,
  `company` VARCHAR(200) NULL ,
  `phone` VARCHAR(45) NULL ,
  `im` VARCHAR(45) NULL ,
  `bank` VARCHAR(100) NULL ,
  `bio` VARCHAR(200) NULL ,
  `img` VARCHAR(200) NULL ,
  `weibo` VARCHAR(200) NULL ,
  `blog` VARCHAR(200) NULL ,
  `area` VARCHAR(200) NULL ,
  `birth` VARCHAR(45) NULL ,
  `bid` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) );
'''
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
    tname=Column(String(100))
    tcount=Column(Integer)
    tcomment=Column(String(100))
    img=Column(String(200))
    def __init__(self,guid,fname,fcount,fcomment,sname,scount,scomment='',img='',tname='',tcount=0,tcomment=''):
        self.guid=guid
        self.fname=fname
        self.fcount=fcount
        self.fcomment=fcomment
        self.sname=sname
        self.scount=scount
        self.scomment=scomment
        self.img=img
        self.tname=tname
        self.tcount=tcount
        self.tcomment=tcomment

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