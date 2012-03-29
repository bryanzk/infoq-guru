# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from modles import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from flask import *
from flask import request,render_template,session,redirect
from flask.views import MethodView
from sqlalchemy.orm import sessionmaker
import re
import string
import datetime
import helper_data
from helper_data import *
import urllib2
import json
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String
from datetime import *
from weibo import *
import logging
from logging.handlers import SMTPHandler
import string
SAE_MYSQL_HOST_M = 'w.rdc.sae.sina.com.cn'
SAE_MYSQL_HOST_S = 'r.rdc.sae.sina.com.cn'
SAE_MYSQL_PORT = '3307'

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
RSS_SIGN_HOME='http://www.infoq.com/rss/rss.action?token=v94n6E2kapoNhNXc9EWTYRXoOoLLHX5S'
RSS_NOT_SIGN_EN='http://www.infoq.com/rss/rss.action?token=3Pkt2g0ELdPI6FKsXWnlhEytktoyTtAB'
RSS_NOT_SIGN_CH='http://www.infoq.com/cn/rss/rss.action?token=mgnOPySplnVRGBQQHToikUWoAGFEqtDo'

Base = declarative_base()

MAIL_SMTP='smtp.exmail.qq.com'
MAIL_TO='arthur@infoq.com;hello.shuiyaya@gmail.com'
MAIL_FROM='notice@magicshui.com'
MAIL_PWD='shuishui123'
MAIL_SUBJECT=u"%sinfoq中英文站更新数据--%s"

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
    def __init__(self,title,pubdate,description,guid,country):
        self.title=title
        self.pubdate=pubdate
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

    def __init__(self,title,pubdate,description,guid,country):
        self.title=title
        self.pubdate=pubdate
        self.description=description
        self.country=country
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
