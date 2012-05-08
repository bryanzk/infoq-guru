# coding: utf-8
import config
from config import *
from trollop import TrelloConnection
from action_mail import *
TrelloConn = TrelloConnection("47285d38ecf695f600ddabd7978a7355","f81c4ae161852e226d6bc5ad3dd6f891470069e0a9e9f4463df5cd7718186c53")
class TrelloTest(MethodView):
	def get(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		hello=""
		mail_pre="""

		"""
		mail_end="""

		"""
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing':
				hello+='<h2>%s</h2>'%x.name
				for y in x.cards:
					i+=1
					hello+='%d: %s desc: %s<br/>'%(i,y.name,y.desc)
		return hello

class TrelloSend(MethodView):
	def  get(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		hello=""
		mail_pre="""

		"""
		mail_end="""

		"""
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' and len(x.cards)>0:
				hello+='<h3>%s</h3><br/>'%x.name
				for y in x.cards:
					i+=1
					hello+='%d  %s <br/> %s<br/><br/><br/>'%(i,y.name,y.desc)
		mail=MailMethod()
		mail._send_default(to='arthur@infoq.com;bryan@infoq.com;houbowei@gmail.com;cuikang@gmail.com',subject="InfoQ新闻线索：%s"%str(datetime.today())[0:10],content=hello)
		return 'ok'