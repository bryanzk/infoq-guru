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
DB = create_engine('mysql://%s:%s@%s:%s/%s'% (DATABASE_USER,DATABASE_PWD,DATABASE_HOST,DATABASE_PORT,DATABASE_NAME),connect_args={'charset':'utf8'},echo=True,pool_recycle=29)

Base = declarative_base()
#RSS_SIGN_HOME='http://www.infoq.com/rss/rss.action?token=v94n6E2kapoNhNXc9EWTYRXoOoLLHX5S'
RSS_NOT_SIGN_EN='http://www.infoq.com/rss/rss.action?token=3Pkt2g0ELdPI6FKsXWnlhEytktoyTtAB'
RSS_NOT_SIGN_CH='http://www.infoq.com/cn/rss/rss.action?token=mgnOPySplnVRGBQQHToikUWoAGFEqtDo'

WEIBO_MAIL_SUBJECT=u'%s微博热点追踪'

STATUS_STEP_LIST={"664":"737","737":"780","780":"800"}
MAIL_SMTP='smtp.exmail.qq.com'
MAIL_TO='arthur@infoq.com;hello.shuiyaya@gmail.com'
MAIL_FROM='notice@magicshui.com'
MAIL_PWD='shuishui123'
MAIL_SUBJECT=u"%s：InfoQ更新--%d篇新闻，%d篇文章，%d篇采访"
CATEGORY_LIST=['Development','Architecture & Design','Process & Practices','Enterprise Architecture','Operations & Infrastructure']
CATEGORY_LIST_CN=['']


def login():
        try:
                token=session['user']
                return True
        except:
            return redirect('error?msg="need login"&next=/')
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
    def __init__(self,id,task_id,code,description,begin,end,contrast,editor,duty):
        self.id=id
        self.task_id=task_id
        self.code=code
        self.description=description
        self.begin=begin
        self.end=end
        self.contrast=contrast
        self.editor=editor
        self.duty
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

