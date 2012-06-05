# coding: utf-8
import config
from config import *
import helper_data
from helper_data import *
#WorkComments_1={'文章翻译':,'文章原创','视频演讲','新闻原创','专家专栏','视频采访','迷你书','新闻翻译','新闻翻译审校','新闻原创审校','文章原创审校','迷你书审校','文章翻译审校','虚拟采访策划','提供新闻线索','专家专栏策划','采访策划','迷你书策划','文章策划']
class CountSearch(MethodView):
	def get(self):
		return render_template('count_search.html',res='')
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		helper=Date_Helper()
		begin,end=helper._get_begin_end()

		results=dbSession.query(RssInfo,EditorCount2List).filter(RssInfo.guid==EditorCount2List.guid).filter(RssInfo.pubdate>begin).filter(RssInfo.pubdate<end).order_by(desc(RssInfo.pubdate)).all()
		count=0
		for x in results:
			count+=1
		return render_template('count_search.html',res=results,count=count)

class CountAuthor(MethodView):
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


class CountStatics(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		begin,end=week_begin_end()
		count_week_all=dbSession.query(func.count(RssInfo.guid)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).filter(RssInfo.country=='ch').scalar()
		
		count_week=dbSession.query(func.count(RssInfo.guid)).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end))
		count_week_news=count_week.filter(RssInfo.guid.like('%cn/news%')).


		#count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(and_(RssInfo.pubdate>=begin,RssInfo.pubdate<end)).scalar()
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
                return render_template('count_wall.html',res=authors)
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