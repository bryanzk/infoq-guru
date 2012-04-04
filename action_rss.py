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
from helper_data import *
import json
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String
from datetime import *
from datetime import timedelta
from config import *
#res = urllib2.urlopen('http://www.infoq.com/rss/rss.action?token=v94n6E2kapoNhNXc9EWTYRXoOoLLHX5S')
#rss = BeautifulSoup(res.read())

class RssNew(MethodView):
    def post(self):
        begin=datetime.strptime((request.form['begin'])+" 00:00:00",'%Y-%m-%d %H:%M:%S')
        end=datetime.strptime((request.form['end'])+" 23:59:59",'%Y-%m-%d %H:%M:%S')
        country=request.form.get('country')
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        r=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country==country).filter(RssInfo.pubdate<=end).order_by(RssInfo.pubdate).all()
        rr=[]
        _helper=WeiboHelper()
        for x in r:
           x.cat=_helper._get_cats(x.guid)
           rr.append(x)
        count=len(rr)

        return render_template('rssnew.html',r=rr,count=count)
    def get(self):
        
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        count=dbSession.query(func.count(RssInfo.guid)).scalar()

        return render_template('rssnew.html',r=[],count=count)
class RssFetchRefresh(MethodView):
    def get(self):
        
        return  render_template('result.html',r='')
    def post(self):
        country=request.form['country']
        if country=='en':
            enrss=RssRefresh()
            return render_template('result.html',r=enrss._get(RSS_NOT_SIGN_EN,'en'))
        elif country=='ch':
            rss=RssRefresh()
            r=rss._get_data(RSS_NOT_SIGN_CH,'ch')
            u=[]
            for x in r:
                    x.pubdate= x.pubdate - timedelta(hours=5)
                    u.append(x)  
            return render_template('result.html',r=rss._save(u))
        else:
             return render_template('result.html',r='error')
class EnRssRefresh(MethodView):
    def post(self):
        enrss=RssRefresh()
        return render_template('result.html',
            r=enrss._get(RSS_NOT_SIGN_EN,'en'))
class ChRssRefresh(MethodView):
    def post(self):
        rss=RssRefresh()
        r=rss._get_data(RSS_NOT_SIGN_CH,'ch')
        u=[]
        for x in r:
            x.pubdate= x.pubdate - timedelta(hours=5)
            u.append(x)  
        return render_template('result.html',
            r=rss._save(u))
class RssRefresh():
    def _save(self,data):
        for r in data:
            if not self._if_it_exists(r.guid):
                dbSession=sessionmaker(bind=DB)
                db_session=dbSession()
                db_session.add(r)
                _nr=RssNewInfo(title=r.title,description=r.description,
                    pubdate=r.pubdate,guid=r.guid,country=r.country,category=r.category)
                db_session.add(_nr)
                db_session.commit()

        return 'ok'
    def _get(self,url,country):
        data=self._get_data(url,country)
        return self._save(data)
    def _get_data(self,url,country):
        res = urllib2.urlopen(url)
        rss = BeautifulSoup((res.read()).decode('utf-8'))
        result=[]
        for x in rss.find_all('item'):
            #self._add_to_new_list()
            category=''
            for _x in x.find_all('category'):
                category+=_x.string+','
            r=RssInfo(
            title=(x.title.string).encode('utf-8'),
            description=(x.description.string).encode('utf-8'),
            pubdate=datetime.strptime((x.pubdate.string).encode('utf-8'),'%a, %d %b %Y %H:%M:%S  GMT'),
            guid=(x.guid.string).encode('utf-8'),
            country=country,category=category)
            result.append(r)
        
        return result
    
                
                 
    '''
        judje if the guid exists in the table 
        if not exists:
            return False
        else:
            return true
    '''
    def _if_it_exists(self,guid):
        dbSession=sessionmaker(bind=DB)
        db_session=dbSession()
        it=db_session.query(RssInfo).filter(RssInfo.guid==guid).all()
        if it:

            return True
        else:

            return False
    '''
        clear the new_list table before the new data is merged into it
    '''
    def _clear_new_list(rl):
        dbSession=sessionmaker(bind=DB)
        db_session=dbSession()
        its=db_session.query(RssNewInfo).filter(RssNewInfo.guid!='').all()
        for x in its:

            db_session.delete(x)
        db_session.commit()
#for x in rss.find_all('item'):
#   print  x.title.string
#   print '--------------'
#print rss.channel.item.title.string
