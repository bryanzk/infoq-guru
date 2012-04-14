# coding: utf-8
from config import *
class FeedbackView(MethodView):
	def get(self):
		pass
	def post(self):
		title=request.form['title']
		content=request.form['content']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=FeedBackList(time=datetime.now(),title=title,content=content)

		dbSession.add(r)
		dbSession.commit()
		dbSession.close()
		return 'ok'