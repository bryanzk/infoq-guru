# coding: utf-8
from config import *
#CONVERT_TO=["运维":"","":""]
class Labs(MethodView):
	def get(self):
		return render_template('lab.html')
class AboutusEditor(MethodView):
	def get(self):
		db_sessin=sessionmaker(bind=DB)
		dbSession=db_sessin()
		fanyi=dbSession.query(AboutusList).filter(AboutusList.team=='翻译').all()
		fanyi.sort(lambda x,y:cmp(x.pinyin,y.pinyin))
		yuanchuang=dbSession.query(AboutusList).filter(AboutusList.team=='原创').all()
		yuanchuang.sort(lambda x,y:cmp(x.pinyin,y.pinyin))
		yunying=dbSession.query(InfoqList).all()
		yunying.sort(lambda x,y:cmp(x.pinyin,y.pinyin))
		dbSession.close()
		return render_template('aboutus.html',fanyi=fanyi,yuanchuang=yuanchuang,yunying=yunying)


