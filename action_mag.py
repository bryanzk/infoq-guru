# coding: utf-8
from config import *
class MagView(MethodView):
	def get(self):
		return render_template('mag_%s.html'%('1204'))