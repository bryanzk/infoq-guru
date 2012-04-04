# -*- coding: utf-8 -*-ß
from config import *
from helper_data import *
class IndexView(MethodView):
    def get(self):
        
        try:
            token=session['token']
        except:
            return redirect('go')
        return render_template('index.html')
class StaticView(MethodView):
    def get(self):
        
        try:
            token=session['token']
        except:
            return redirect('go')

        return render_template('static_rss.html',r=[])
    def post(self):
        d=Date_Helper()
        begin,end=d._get_begin_end()# get all the data of rss
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        r=dbSession.query(RssInfo).filter(RssInfo.pubdate>=begin).filter(RssInfo.country=='ch').filter(RssInfo.pubdate<=end).order_by(RssInfo.pubdate).all()
        rr=[]
        for x in r:
            w=WeiboR()
            w.time=x.pubdate
            w.title=x.title
            w.guid=x.guid
            _x=dbSession.query(WeiboM).filter(WeiboM.org_url==x.guid).all()
            if _x:
                w.weibo=_x[0].url
                w.athur=_x[0].athur
                w.cat=_x[0].cat
                w.comment=_x[0].comment
                w.retweet=_x[0].retweet
            else:
                w.weibo='none'
                w.athur='none'
               
                _helper=WeiboHelper()
                w.cat=_helper._get_cats(w.guid)
                
            rr.append(w)
        count=len(rr)

        return render_template('static_rss.html',r=rr,count=count)