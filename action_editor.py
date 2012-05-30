from config import *
from helper_data import *
class  EditorView(MethodView):
	"""docstring for  """
	def get(self):
		return render_template('editor.html')
class EditorArticleSearch(MethodView):
	def get(self):
		return render_template('editor_search.html')
	def post(self):
		
		return render_template('editor_search.html')
class AboutView(MethodView):
	def get(self):
		return render_template('about.html')
class EditorAbout(MethodView):
	def  get(self):
		return render_template('editorone.html')
class EditorAdd(MethodView):
	def get(self):
		pass
	def post(self):
		pass
class EditorTask(MethodView):
	def get(self):
		pass
	def  post(self):
		pass
class EditorList(MethodView):
	def get(self):
		pass
	def post():
		pass
'''
don't delete , just tag 
'''
class EditorDelete(MethodView):
	def get(self):
		pass
	def  post(self):
		pass
class EditorCountListAll(MethodView):
	def get(self):
		page=request.args.get('page','0')
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		pre=0
		results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').order_by(desc(RssInfo.pubdate)).limit(20).offset(int(page)).all()
		if page=="0":
			pre=0
		else:
			pre=int(page)-1
		return render_template('editor_count_all.html',res=results,pre=pre,next=int(page)+1)
class EditorCountShow(MethodView):
	def get(self):
		guid=request.args.get('guid')
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		result=dbSession.query(EditorCountWeiboList).filter(EditorCountWeiboList.guid==guid).all()
		res=''
		if result:
			res=result[0]
		else:
			u=EditorCountWeiboList(guid=guid,fname='',fcount=0,fcomment='',sname='',scount=0,scomment='',img='')
			dbSession.add(u)
			dbSession.commit()
			res=u
		return render_template('editor_count_show.html',res=res)
	def post(self):
		guid=request.form['guid']
		fname=request.form['fname']
		fcount=request.form['fcount']
		fcomment=request.form['fcomment']
		sname=request.form['sname']
		scount=request.form['scount']
		scomment=request.form['scomment']
		img=request.form['img']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		u=dbSession.query(EditorCountWeiboList).filter(EditorCountWeiboList.guid==guid).all()
		u[0].fname=fname
		u[0].fcount=fcount
		u[0].fcomment=fcomment
		u[0].sname=sname
		u[0].scount=scount
		u[0].scomment=scomment
		u[0].img=img
		dbSession.commit()
		return redirect('editorcountall')
# show the editors weibo and add new editor's weibo 
class EditorWeibo(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(EditorWeiboList).all()
		return render_template('editor_weibo.html',ress=res)
	def post(self):
		name=request.form['name']
		wname=request.form['wname']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		#wid=request.args.get('wid')
		u=EditorWeiboList(name=name,wname=wname,wid="")
		dbSession.add(u)
		dbSession.commit()
		flash('ok')
		return redirect('editorweibo')
# share the weibo of one
class RssWeiboShare(MethodView):
	def get(self):
		helper=WeiboHelper()
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		guid=request.args.get('guid')
		_rss=dbSession.query(RssInfo).filter(RssInfo.guid==guid).first()
		_img=dbSession.query(EditorCountWeiboList).filter(EditorCountWeiboList.guid==guid).first()
		_weibo=dbSession.query(EditorWeiboList).filter(EditorWeiboList.name==_img.fname).all()
		
		title=_rss.title
		author=""
		if _weibo:
			author=_weibo[0].wname
		else:
			author=_img.sname
		content=_rss.description.replace(" ","")
		img=_img.img
		ctype=helper._get_cats(guid)
		return render_template('editor_weibo_share.html',ctype=ctype,title=title,guid=guid,content=content,author=author,img=img)
class EditorHistoryAll(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		editors=dbSession.query(EditorWeiboList).all()
		return render_template()

