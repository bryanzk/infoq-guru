# coding: utf-8
class TimeLine(ViewMethod):
	def get(self):
		return render_template('time_index.html')