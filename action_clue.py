# coding: utf-8
import config
from config import *
from trollop import TrelloConnection
from action_mail import *
TrelloConn = TrelloConnection("47285d38ecf695f600ddabd7978a7355","02a2c4c83e0e47b6b4d6cc3337d85547fdb9b56d65102188862308aaefec1e49")
Labels={u"\u8bed\u8a00":"green",u"\u67b6\u6784 ":"yellow",u"\u8fc7\u7a0b":"orange",u"\u8fd0\u7ef4":"red",u"企业架构":"purple","Done":"blue"}


class TrelloTest(MethodView):
	def get(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		hello=""
		mail_pre="""

		"""
		mail_end="""

		"""
		##today=datetime.today()
		##older=today-datetime.timedelta(5)

		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' :
				hello+='<h2>%s</h2>'%x.name
				x.cards.reverse()

				for y in x.cards:
					if not y.labels :
						i+=1
						raise
						hello+='%d: <a href="trellodone?id=%s&cat=%s">%s</a> desc: %s<br/>'%(i,y.id,x.name,y.name,y.desc)
					

		return hello
class TrelloDone(MethodView):
	def get(self):
		id=request.args.get('id')
		card=TrelloConn.get_card(id)
		if card.labels:
			return u'下手晚了，已经有人认领了'
		cat=request.args.get('cat')
		return render_template('clue_add.html',id=id,cat=cat)
	def post(self):
		name=request.form['name']
		id=request.form['id']
		due=request.form['due']
		cat=Labels[(request.form['cat']).decode('utf-8')]
		#id="4fa95e2e85710c9005789345"
		#cat="green"
		params = {'value': due}
		params2={'text':name}
		params3={'value':cat}
		TrelloConn.put(path='cards/%s/due'%id, params=params, body=None)
		TrelloConn.post(path='/cards/%s/actions/comments'%id,params=params2)
		TrelloConn.post(path='/cards/%s/labels'%id,params=params3)

		return 'ok'
class TrelloTougao(MethodView):
	def get(self):
		board=TrelloConn.get_board('4f687a1b5b5ccf1b76022c38')
		lists=board.lists
		hello=""
		for x in lists:
			if x.name=='审校中' or x.name=='审校完成' or not x.due:
				hello+='<h2>%s</h2>'%x.name
				for y in x.cards:
					hello+=' %s <br/>'%(y.name)
		
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
		##today=datetime.today()
		#older=today-datetime.timedelta(5)
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' and len(x.cards)>0:
				hello+='<h3>%s</h3><br/>'%x.name
				for y in x.cards:
					i+=1
					hello+='%d  %s <br/> %s<br/><br/><br/>'%(i,y.name,y.desc)
		mail=MailMethod()
		mail._send_default(to='arthur@infoq.com',subject="InfoQ新闻线索：%s"%str(datetime.today())[0:10],content=hello)
		return 'ok'