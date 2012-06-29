# coding: utf-8
import config
from config import *
import helper_data
from helper_data import *
WorkComments_1={'文章翻译':0.08,'文章原创':0.15,'视频演讲':0,'新闻原创':0.2,'专家专栏':0.15,'视频采访':0,'迷你书':0.15,'新闻翻译':0.08,'新闻翻译审校':0.080,'新闻原创审校':0.03,'文章原创审校':0.06,'迷你书审校':0.3,'文章翻译审校':0.04,'虚拟采访策划':0.300,'提供新闻线索':0,'专家专栏策划':0.120,'采访策划':0.300,'迷你书策划':0.3,'文章策划':120}
def get_detail_of_cat_week(cat,small_cat,main_cat):
	db_session=sessionmaker(bind=DB)
	dbSession=db_session()
	begin,end=week_begin_end()
	count_week_news=dbSession.query(RssInfo).filter(RssInfo.main_cat.like('%'+main_cat+'%')).filter(RssInfo.small_cat.like('%'+small_cat+'%')).filter(RssInfo.guid.op('regexp')('\\/cn\\/'+cat)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).all()
	one_line='<br/>'
        if count_week_news:
		xa=(one_line.join('%s'%x.title for x in count_week_news))
                return xa
        else:
        	return ''

class CountStaticWeekDetail(MethodView):
	def post(self):
		cat=request.form['cat']
		main_cat=request.form['main_cat']
		small_cat=request.form['small_cat']

		return get_detail_of_cat_week(cat.encode('utf-8'),small_cat.encode('utf-8'),main_cat.encode('utf-8'))

class CountOD(MethodView):
	@login(wtype='admin,core')
	def get(self):
        	db_session=sessionmaker(bind=DB)
                dbSession=db_session()
        	begin,end=week_begin_end()
                b2=begin-timedelta(days=7)
                e2=end-timedelta(days=7)
        	t_no=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='ch').filter(RssInfo.guid.like('%news%')).filter(RssInfo.small_cat==u'翻译').filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                _t_no=dbSession.query(RssInfo).filter(RssInfo.small_cat==u'翻译').filter(RssInfo.guid.like('%news%')).filter(RssInfo.country=='ch').filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).all()
                t_no_current=0
                for x in _t_no:
                	if dbSession.query(RssInfo).filter(RssInfo.country=='en').filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).filter(RssInfo.guid.like('%'+x.guid.split('/')[-1]+'%')).all():
                        	t_no_current+=1
                n_no_en=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='en').filter(RssInfo.guid.like('%news%')).filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                t_a=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='ch').filter(RssInfo.guid.like('%article%')).filter(RssInfo.small_cat==u'翻译').filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                a_en=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='en').filter(RssInfo.guid.like('%article%')).filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                t_i=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='ch').filter(RssInfo.guid.like('%cn/i%')).filter(RssInfo.small_cat==u'翻译').filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                v_en=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='en').filter(RssInfo.guid.op('regexp')('com\\/[ip]')).filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                o_n=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='ch').filter(RssInfo.small_cat==u'原创').filter(RssInfo.guid.like('%cn/news%')).filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                o_a=dbSession.query(func.count(RssInfo)).filter(RssInfo.country=='ch').filter(RssInfo.small_cat==u'原创').filter(RssInfo.guid.like('%cn/ar%')).filter(and_(RssInfo.pubdate>=b2,RssInfo.pubdate<e2)).scalar()
                return render_template('count_od.html',b2=str(b2),e2=str(e2-timedelta(days=1)),t_no=t_no,t_no_current=t_no_current,n_no_en=n_no_en,t_a=t_a,a_en=a_en,t_i=t_i,v_en=v_en,o_n=o_n,o_a=o_a)
                return """from %s to %s <br/>
                	Translate N.O %d Translated N.O of Current Week %d,News %d
                        
                        <br/>
                        
                        T.A %d, A in En %d
                        
                        <br/>
                        
                        T. Interver %d,Video %d
                        
                        <br/>
                        
                        Org News %d
                        
                        <br/>
                        
                        Org Articles %d
                """%(str(b2),str(e2),t_no,t_no_current,n_no_en,t_a,a_en,t_i,v_en,o_n,o_a)
class CountSearch(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		return render_template('count_search.html',res='')
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		helper=Date_Helper()
		begin,end=helper._get_begin_end()

		results=dbSession.query(RssInfo,EditorCount2List).filter(RssInfo.guid==EditorCount2List.guid).filter(RssInfo.pubdate>=begin).filter(RssInfo.pubdate<end).order_by(desc(RssInfo.pubdate)).all()
		count=0
		for x in results:
			count+=1
		return render_template('count_search.html',res=results,count=count,fee=WorkComments_1)

class CountAuthor(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		helper=Date_Helper()
		aus=dbSession.query(func.distinct(EditorCount2List.name)).all()
		
		results=dbSession.query(RssInfo,EditorCount2List).filter(RssInfo.guid==EditorCount2List.guid).filter(EditorCount2List.name==request.args.get('author')).order_by(desc(RssInfo.pubdate)).all()
		return render_template('count_author.html',aus=aus,res=results,author=request.args.get('author'))
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		helper=Date_Helper()
		aus=dbSession.query(func.distinct(EditorCount2List.name)).all()
		results=dbSession.query(RssInfo,EditorCount2List).filter(RssInfo.guid==EditorCount2List.guid).filter(EditorCount2List.name==request.form['author']).order_by(desc(RssInfo.pubdate)).all()
		return render_template('count_author.html',aus=aus,res=results,author=request.form['author'])
		


def week_begin_end():
	now=date.today()
	now_int=date.today().weekday()
	if now_int<4:
		begin=date.today()-timedelta(days=(now_int+3))
		end=begin+timedelta(days=7)
		return begin,end
	else:
		begin=date.today()-timedelta(days=(now_int-4))
		end=begin+timedelta(days=7)
		return begin,end
                
class CountStatics2LastWeek(MethodView):
	def get(self):
		cat=request.form['cat']

		return get_count_of_cat_week(cat,main_cat)
	def post(self):
		cat=request.form['cat']

		small_cat=request.form['small_cat']
                print small_cat
		return get_count_of_last_week(cat.encode('utf-8'),small_cat.encode('utf-8'))
                
def get_count_of_last_week(cat,small_cat):
	db_session=sessionmaker(bind=DB)
	dbSession=db_session()
	begin1,end1=week_begin_end()
        begin=begin1-timedelta(days=7)
        end=end1-timedelta(days=7)
	#count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.main_cat.like('%'+main_cat+'%')).filter(RssInfo.small_cat.like('%'+small_cat+'%')).filter(RssInfo.guid.like('%cn/'+cat+'%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
        count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.small_cat.like('%'+small_cat+'%')).filter(RssInfo.guid.op('regexp')('\\/cn\\/'+cat)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
	return str(count_week_news)
        
        
class CountStatics2(MethodView):
	def get(self):
		cat=request.form['cat']
		main_cat=request.form['main_cat']
		small_cat=request.form['small_cat']
                print small_cat
		return get_count_of_cat_week(cat.encode('utf-8'),small_cat.encode('utf-8'),main_cat.encode('utf-8'))
	def post(self):
		cat=request.form['cat']
		main_cat=request.form['main_cat']
		small_cat=request.form['small_cat']
                print small_cat
		return get_count_of_cat_week(cat.encode('utf-8'),small_cat.encode('utf-8'),main_cat.encode('utf-8'))
                

        
def get_count_of_cat_week(cat,small_cat,main_cat):
	db_session=sessionmaker(bind=DB)
	dbSession=db_session()
	begin,end=week_begin_end()
	#count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.main_cat.like('%'+main_cat+'%')).filter(RssInfo.small_cat.like('%'+small_cat+'%')).filter(RssInfo.guid.like('%cn/'+cat+'%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
        count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.main_cat.like('%'+main_cat+'%')).filter(RssInfo.small_cat.like('%'+small_cat+'%')).filter(RssInfo.guid.op('regexp')('\\/cn\\/'+cat)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
	return str(count_week_news)
        
class CountStaticsMail(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		begin,end=week_begin_end()
		count_week_all=dbSession.query(func.count(RssInfo.guid)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).filter(RssInfo.country=='ch').scalar()
		
		count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/presentation%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()

		lbegin=begin-timedelta(days=7)
		lend=end-timedelta(days=7)

		lcount_week_all=dbSession.query(func.count(RssInfo.guid)).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).filter(RssInfo.country=='ch').scalar()
		lcount_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/pres%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()

		count_month_all=dbSession.query(func.count(RssInfo.guid)).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).filter(RssInfo.country=='ch').scalar()
		count_month_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/pres%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()


		lcount_month_all=dbSession.query(func.count(RssInfo.guid)).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).filter(RssInfo.country=='ch').scalar()
		lcount_month_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/pre%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		
		return render_template('count_statics_mail.html',
			wl=count_week_all,wn=count_week_news,wa=count_week_article,wi=count_week_interview,wp=count_week_presentation,wm=count_week_minibooks,
			ml=count_month_all,mn=count_month_news,ma=count_month_article,mi=count_month_interview,mp=count_month_presentation,mm=count_month_minibooks,
			lwl=lcount_week_all,lwn=lcount_week_news,lwa=lcount_week_article,lwi=lcount_week_interview,lwp=lcount_week_presentation,lwm=lcount_week_minibooks,
			lml=lcount_month_all,lmn=lcount_month_news,lma=lcount_month_article,lmi=lcount_month_interview,lmp=lcount_month_presentation,lmm=lcount_month_minibooks
			,begin=begin,end=end-timedelta(days=1),lbegin=lbegin,lend=lend-timedelta(days=1))
        
class CountStatics(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		begin,end=week_begin_end()
		count_week_all=dbSession.query(func.count(RssInfo.guid)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).filter(RssInfo.country=='ch').scalar()
		
		count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/presentation%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
		count_week_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()

		lbegin=begin-timedelta(days=7)
		lend=end-timedelta(days=7)

		lcount_week_all=dbSession.query(func.count(RssInfo.guid)).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).filter(RssInfo.country=='ch').scalar()
		lcount_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/pres%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()
		lcount_week_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(and_(RssInfo.pubdate>=lbegin,RssInfo.pubdate<lend)).scalar()

		count_month_all=dbSession.query(func.count(RssInfo.guid)).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).filter(RssInfo.country=='ch').scalar()
		count_month_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/pres%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()


		lcount_month_all=dbSession.query(func.count(RssInfo.guid)).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).filter(RssInfo.country=='ch').scalar()
		lcount_month_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_interview=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/interviews%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_presentation=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/pre%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		lcount_month_minibooks=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/minibook%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())-1).scalar()
		
		return render_template('count_statics.html',
			wl=count_week_all,wn=count_week_news,wa=count_week_article,wi=count_week_interview,wp=count_week_presentation,wm=count_week_minibooks,
			ml=count_month_all,mn=count_month_news,ma=count_month_article,mi=count_month_interview,mp=count_month_presentation,mm=count_month_minibooks,
			lwl=lcount_week_all,lwn=lcount_week_news,lwa=lcount_week_article,lwi=lcount_week_interview,lwp=lcount_week_presentation,lwm=lcount_week_minibooks,
			lml=lcount_month_all,lmn=lcount_month_news,lma=lcount_month_article,lmi=lcount_month_interview,lmp=lcount_month_presentation,lmm=lcount_month_minibooks
			,begin=begin,end=end-timedelta(days=1),lbegin=lbegin,lend=lend-timedelta(days=1))

class CountContents(MethodView):
	@login(wtype='admin,core,editor,gof')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		_results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').all()
		_results_week=dbSession.query(RssInfo).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).all()
		_results_month=dbSession.query(RssInfo).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).all()		
		
		_results_week_news=dbSession.query(RssInfo).filter(RssInfo.guid.like('%cn/news')).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).all()
		_results_month_news=dbSession.query(RssInfo).filter(RssInfo.guid.like('%cn/news')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).all()		
		raise
	def post(self):
		pass
class CountHelper():
	def convert_to_detail_count(self,all):
		pass
class CountEditors(MethodView):
	def get(self):
		pass
class CountWeek2(MethodView):
	def get(self):
		return render_template('count_week.html')
class CountWall(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()	
		authors=dbSession.query(func.distinct(EditorCount2List.name)).order_by(func.count(EditorCount2List.guid)).group_by(EditorCount2List.name).all()
		authors.reverse()
                return render_template('count_wall.html',res=authors[:29])
class CountWeekAuthor(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		author=request.args.get('author')
		results=dbSession.query(RssInfo.pubdate,func.count(RssInfo.pubdate)).order_by(RssInfo.pubdate).filter(RssInfo.guid==EditorCount2List.guid).filter(EditorCount2List.name==author).group_by(func.week(RssInfo.pubdate)).filter(RssInfo.country=='ch').all()
		results2=','.join('{"date":"%s","price":"%d"}'%((str(x[0])[0:10]).replace('-',' '),x[1]) for x in results)
		return "["+results2+"]"

class CountWeek(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(RssInfo.pubdate,func.count(RssInfo.pubdate)).order_by(RssInfo.pubdate).group_by(func.week(RssInfo.pubdate)).filter(RssInfo.country=='ch').all()
		results2=','.join('{"date":"%s","price":"%d"}'%((str(x[0])[0:10]).replace('-',' '),x[1]) for x in results)
		return "["+results2+"]"