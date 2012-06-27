#coding: utf-8
import config
from config import *
class EditorIndex(MethodView):
	@login(wtype='editor,admin')
	def get(self):
		return render_template('editor_index.html')
class GofIndex(MethodView):
	@login(wtype='gof,admin,core,editor')
	def get(self):
		return render_template('editor_index.html')
