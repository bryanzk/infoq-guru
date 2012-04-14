# coding: utf-8
from config import *
class AboutusEditor(MethodView):
	def get(self):
		db_sessin=sessionmaker(bind=DB)
		dbSession=db_sessin()
		fanyi=dbSession.query(AboutusList).filter(AboutusList.team=='翻译').all()
		yuanchuang=dbSession.query(AboutusList).filter(AboutusList.team=='原创').all()
		return render_template('aboutus.html',fanyi=fanyi,yuanchuang=yuanchuang)