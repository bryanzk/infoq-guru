# coding: utf-8
import config 
from helper_data import *
from config import *
import md5
WorkComments_1=['文章翻译','文章原创','视频演讲','新闻原创','专家专栏','视频采访','迷你书','新闻翻译','新闻原创']
WorkComments_2=['新闻翻译审校','新闻原创审校','文章原创审校','迷你书审校','文章翻译审校']
WorkComments_3=['虚拟采访策划','提供新闻线索','专家专栏策划','采访策划','迷你书策划','文章策划']
Convert_list={'翻译审校':'文章翻译审校',"新闻审评":"新闻翻译审校",'原创新闻审评':'希望嫩原创审校','原创新闻':'新闻原创','文章审校':'文章原创审校'}

class EditorCountShow2(MethodView):
	def get(self):
		guid=request.args.get('guid')
		version=request.args.get('version')
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		result=dbSession.query(EditorCount2List).filter(EditorCount2List.version==version).filter(EditorCount2List.guid==guid).all()
		res=''
		work=''
		if result:
			res=result[0]
			
		else:
			u=EditorCount2List(guid=guid,version=version)
			dbSession.add(u)
			dbSession.commit()
			res=u
		if version=='1':
				work=WorkComments_1
		elif version=='2':
				work=WorkComments_2
		elif version=='3':
				work=WorkComments_3
		return render_template('editor_count_show2.html',res=res,work=work,version=version)
	def post(self):
		id=request.form['id']
		guid=request.form['guid']
		version=request.form['version']
		name=request.form['name']
		count=request.form['count']
		comment=request.form['comment']
		img=request.form['img']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		u=dbSession.query(EditorCount2List).filter(EditorCount2List.id==id).all()
		u[0].name=name
		u[0].count=count
		u[0].comment=comment
		u[0].img=img
		_empty=dbSession.query(EditorCount2List).filter(EditorCount2List.name=='').all()
		for x in _empty:
			dbSession.delete(x)
		dbSession.commit()
		return redirect('editorcountall2')
# share the weibo of one
class RssWeiboShare2(MethodView):
	def get(self):
		helper=WeiboHelper()
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		guid=request.args.get('guid')
		_rss=dbSession.query(RssInfo).filter(RssInfo.guid==guid).first()
		_img=dbSession.query(EditorCount2List).filter(EditorCount2List.version==1).filter(EditorCount2List.guid==guid).first()
		_weibo=dbSession.query(EditorWeiboList).filter(EditorWeiboList.name==_img.name).all()
		
		title=_rss.title
		author=""
		if _weibo:
			author=_weibo[0].wname
		else:
			author=_img.name
		content=_rss.description.replace(" ","")
		img=_img.img
		ctype=helper._get_cats(guid)
		return render_template('editor_weibo_share.html',ctype=ctype,title=title,guid=guid,content=content,author=author,img=img)

# the data type for 
class CnContents(Base):
	__tablename__='cn_contents'
	id=Column(Integer,primary_key=True)
  	version=Column(Integer)
  	author=Column(String(100))
  	community=Column(String(100))
  	description=Column(String(500))
  	flag=Column(String(100))
  	identifier=Column(String(200))
  	length=Column(Integer)
  	link=Column(String(200))
  	pub_date=Column(DateTime)
  	title=Column(String(100))
  	type=Column(String(100))
  	worktype=Column(String(100))
  	img_url=Column(String(100))
  	def __init__(self,id,version,author,community,description,flag,identifier,length,link,pub_date,title,type,worktype,img_url):
  		self.id=id
  		self.version=version
  		self.author=author
  		self.community=community
  		self.description=description
  		self.flag=flag
  		self.identifier=identifier
  		self.length=length
  		self.link=link
  		self.pub_date=pub_date
  		self.title=title
  		self.type=type
  		self.worktype=worktype
  		self.img_url=img_url
def _convert_to_version(worktype):
	if worktype in WorkComments_1:
		return 1
	elif worktype in WorkComments_2:
		return 2
	else:
		return 3
def _convert_to_comment(url,worktype):
	if worktype==u'翻译' and url.find('news')>0:
		return '新闻翻译'
	elif worktype==u'翻译' and url.find('articles')>0:
		return '文章翻译'
	elif worktype==u'翻译' and url.find('minibooks')>0:
		return '迷你书翻译'
	elif worktype==u'翻译' and url.find('interviews')>0:
		return '视频翻译'
	elif worktype in Convert_list:
		return Convert_list[worktype]
	return worktype
class ConvertToNew(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(CnContents).all()
		for x in results:
			u=EditorCount2List(guid=x.link,name=x.author,comment=_convert_to_comment(x.link,x.worktype),count=x.length,img=x.img_url,version=_convert_to_version(_convert_to_comment(x.link,x.worktype)))
			dbSession.add(u)

		dbSession.commit()
		return true
class ConvertToNew2(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		results=dbSession.query(func.distinct(CnContents.link)).filter(CnContents.pub_date<='2012-03-24').all()
		for y in results:
			x=dbSession.query(CnContents).filter(CnContents.link==y[0]).first()
			u=RssInfo(title=x.title,guid=x.link,description=x.description,pubdate=x.pub_date,country='ch',category=x.community)
			if not dbSession.query(RssInfo).all():
				dbSession.add(u)
			
		dbSession.commit()
		return 'ok'
