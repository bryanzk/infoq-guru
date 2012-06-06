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
class RssChangeMainCatAll(MethodView):
    def get(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').filter(and_(RssInfo.main_cat!= None,RssInfo.main_cat!='')).order_by(RssInfo.pubdate).limit(30)
        
        return render_template('rss_change_maincat_all.html',res=results)
class RssSetMainCatAll(MethodView):
    def get(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').filter(or_(RssInfo.main_cat== None,RssInfo.main_cat=='')).order_by(RssInfo.pubdate).limit(30)
        
        return render_template('rss_set_maincat_all.html',res=results)
class RssSetMainCat(MethodView):
    def get(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        results=dbSession.query(RssInfo).filter(RssInfo.guid==request.args.get('guid')).all()
        
        return render_template('rss_set_maincat.html',res=results[0])
    def post(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        results=dbSession.query(RssInfo).filter(RssInfo.guid==request.form['guid']).first()
        CATS={'语言 ':"语言 & 开发",'架构 ':'架构 & 设计','过程 ':"过程 & 实践","运维 ":'运维 & 基础架构',"企业架构":"企业架构"}
        if request.form['main_cat']=='语言 ':
            results.main_cat='语言　＆　开发'
        elif request.form['main_cat']=='架构 ':
            results.main_cat='架构 &　设计'
        elif request.form['main_cat']=='过程 ':
            results.main_cat='过程 & 实践'
        elif request.form['main_cat']=='运维 ':
            results.main_cat='运维 & 基础架构'
        elif request.form['main_cat']=='企业架构':
            results.main_cat='企业架构'

        
        dbSession.commit()
        return 'ok'
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
                _nr=RssNewInfo(title=r.title,description=r.description,small_cat=r.small_cat,author=r.author,
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
            country=country,category=category,author=x.find('dc:creator').string,
            small_cat=self._get_smallcat(x.find('dc:creator').string))
            
            result.append(r)
        
        return result
    def _get_smallcat(self,author):
        _key=re.findall('[a-zA-Z]',author)
        if _key:
            return u'翻译'
        else:
            return u'原创'
                
                 
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
            if it[0].main_cat!='':
                return True
        db_session.delete(it[0])
        db_session.commit()
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

