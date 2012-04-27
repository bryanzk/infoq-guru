# coding: utf-8
from config import *
class GetFileImage(MethodView):
	def  get(self):
		return "http://www.google.com.hk/images/nav_logo107.png"

# 获取文章的所有
class GetContent(MethodView):
	def  get(self):
		return render_template('')
	def post(self):
		pass
class UpdateContent(MethodView):
	def get(self):
		id=''
		return render_template('')
	def  post():
		pass