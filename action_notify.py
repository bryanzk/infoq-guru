# coding: utf-8
import config
from config import *

	
class NotifyGet(MethodView):
	def get(self):
		user=session['user'].user
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		result=dbSession.query(NotificationList).filter(NotificationList.to==user).filter(NotificationList.status==0).all()
		if result:
			result[0].status=1
			dbSession.commit()
			return result[0].hey+result[0].content
		return  ''


class NotifyCenter(MethodView):
	def get(self):
		user=session['user'].user
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		result=dbSession.query(NotificationList).filter(NotificationList.to==user).order_by(desc(NotificationList.pubdate)).limit(30)
		return render_template('notify_center.html',res=result)