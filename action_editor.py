from config import *
class  EditorView(MethodView):
	"""docstring for  """
	def get(self):
		return render_template('editor.html')
class AboutView(MethodView):
	def get(self):
		return render_template('about.html')
class EditorAbout(MethodView):
	def  get(self):
		return render_template('editorone.html')