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
		results=dbSession.query(RssInfo).filter(RssInfo.country=='ch').order_by(desc(RssInfo.pubdate)).limit(20).offset(20*int(page)).all()
		if page=="0":
			pre=0
		else:
			pre=int(page)-1
		return render_template('editor_count_all.html',res=results,pre=pre,next=int(page)+1)

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
