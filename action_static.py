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
            w.smallcat=x.small_cat
            w.maincat=x.main_cat
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
'''class StaticWeekContentsJson(MethodView):
    def get(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        week=request.args.get('week')
        #results=dbSession.query(func.week(RssInfo.pubdate),func.count(RssInfo.guid)).group_by(func.week(RssInfo.pubdate)).all()
        results=dbSession.query(RssInfo).filter(func.week(RssInfo.pubdate)==week).all()
        raise
        return results
class StaticWeekContent(MethodView):
    def get(self):
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        results=dbSession.query(func.week(RssInfo.pubdate),func.count(RssInfo.guid)).group_by(func.week(RssInfo.pubdate)).all()
        #results=dbSession.query(RssInfo).filter(func.week(RssInfo.pubdate)==13).all()
        raise
        #output the [week_number,week_contents_count]
        return results
class StaticEditorContents(MethodView):
    def get(self):
        editor=request.args.get('editor')
        # 获取编辑的贡献信息
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        # 获取发布的
        results_f=dbSession.query(EditorCountWeiboList,RssInfo).filter(EditorCountWeiboList.fname==editor).order_by(desc(RssInfo.pubdate)).all()
        # 获取审校的
        results_s=dbSession.query(EditorCountWeiboList,RssInfo).filter(RssInfo.guid==EditorCountWeiboList.guid).filter(EditorCountWeiboList.sname==editor).order_by(desc(RssInfo.pubdate)).all()
        raise'''