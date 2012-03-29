# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from flask import *
from flask import request,render_template,session,redirect
from flask.views import MethodView
from sqlalchemy.orm import sessionmaker

import json
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String
from datetime import *
from config import *
from helper_data import *
class GotoOauth(MethodView):
    def get(self):
        client  = APIClient(app_key = APP_KEY,app_secret=APP_SECRET,
                    redirect_uri=CALLBACK_URL)
        url = client.get_authorize_url()
        return render_template('gotooauth.html',url=url)

class ComebackOauth(MethodView):
    def get(self):
        code = request.args.get('code')
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        session['token']=access_token
        session['expires_in']=expires_in
        t=TokenListInfo(time=datetime.now(),token=access_token,
            expire=expires_in,level='infoq')
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        dbSession.add(t)
        dbSession.commit()
        return redirect('weibor')
        

class WeiboRefresh(MethodView):
    @login
    @token
    def get(self):
        helper=WeiboHelper()
        helper_data=Helper_Data()
        res=helper._get_data()
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        count=dbSession.query(func.count(WeiboM.url)).scalar()
        dbSession.close()
        return render_template('weibo_get.html',r=res,count=count)
    def post(self):
        page=request.form['page']
        helper=WeiboHelper()
        helper_data=Helper_Data()
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        res=helper._get_data_with_page(page)
        for x in res:
            if not helper_data.is_weibo_exists(x.org_url):
                dbSession.add(x)
                dbSession.commit()
        
        return redirect('weibor')
class WeiboResult(MethodView):
    @login
    @token
    def get(self):
        return render_template('weibo.html',r=[])
    def post(self):
        end=datetime.strptime((request.form['end'])+" 23:59:59",'%Y-%m-%d %H:%M:%S')
        begin=datetime.strptime((request.form['begin'])+" 00:00:00",'%Y-%m-%d %H:%M:%S')
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        r=dbSession.query(WeiboM).filter(WeiboM.time>=begin).filter(WeiboM.time<=end).order_by(WeiboM.time).all()
        count=dbSession.query(func.count(WeiboM.org_url)).filter(WeiboM.time>=begin).filter(WeiboM.time<=end).order_by(WeiboM.time).scalar()

        return render_template('weibo.html',r=r,count=count)

class ShowAll(MethodView):
    def get(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        res=dbSession.query(WeiboM).all()

        return render_template('test.html',res=res)



        
