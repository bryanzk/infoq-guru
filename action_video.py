# coding: utf-8
import config
class VideoTimeline(MethodView):
	def get(self):
		return render_template('video_timeline.html')
		