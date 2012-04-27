from config import *
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