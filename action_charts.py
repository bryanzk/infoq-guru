from config import *
import simplejson as json
class WeiboChart(MethodView):
	def get(self):
		return render_template('charts_weibo.html')
class WeiboCommentView(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(WeiboM).all()
		data=[]
		for x in res:
			_m=DataM(time=x.time,count=x.comment)
			data.append(_m)
		return json.dumps([p.__dict__ for p in data])
class DataM():
	time=''
	count=''
	def __init__(self,time,count):
		self.time=time
		self.count=count