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
		return render_template('count_author.html',aus=aus,res=results)
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		helper=Date_Helper()
		aus=dbSession.query(func.distinct(EditorCount2List.name)).all()
		results=dbSession.query(RssInfo,EditorCount2List).filter(RssInfo.guid==EditorCount2List.guid).filter(EditorCount2List.name==request.form['author']).order_by(desc(RssInfo.pubdate)).all()
		return render_template('count_author.html',aus=aus,res=results)
		


class CountStatics(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		count_week_all=dbSession.query(func.count(RssInfo.guid)).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).scalar()
		count_week_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).scalar()
		count_week_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(func.week(RssInfo.pubdate)==func.week(datetime.today())).scalar()

		count_month_all=dbSession.query(func.count(RssInfo.guid)).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_news=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/news%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
		count_month_article=dbSession.query(func.count(RssInfo.guid)).filter(RssInfo.guid.like('%cn/articles%')).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).scalar()
                month_al=dbSession.query(RssInfo).filter(func.month(RssInfo.pubdate)==func.month(datetime.today())).all())

		return render_template('count_statics.html',wl=count_week_all,wn=count_week_news,wa=count_week_article,
			ml=count_month_all,mn=count_month_news,ma=count_month_article,month_al=month_al)

                        
                        
                      



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
class CountWeek(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(RssInfo.pubdate,func.count(RssInfo.pubdate)).group_by(func.week(RssInfo.pubdate)).all()
		results2=','.join('[date:"%s",price:%d]'%(x[0],x[1]) for x in results)
		return "{'data':"+results2+"}"