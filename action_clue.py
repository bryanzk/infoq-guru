# coding: utf-8
import config
from config import *
from trollop import TrelloConnection
from action_mail import *
TrelloConn = TrelloConnection("47285d38ecf695f600ddabd7978a7355","02a2c4c83e0e47b6b4d6cc3337d85547fdb9b56d65102188862308aaefec1e49")
Labels={u"\u8bed\u8a00 ":"green",u"\u67b6\u6784 ":"yellow",u"\u8fc7\u7a0b ":"orange",u"\u8fd0\u7ef4 ":"red",u"企业架构":"purple","Done":"blue"}
CreateDate="https://api.trello.com/1/cards/%s/actions?fileds=date&filter=createCard&key=47285d38ecf695f600ddabd7978a7355&token=02a2c4c83e0e47b6b4d6cc3337d85547fdb9b56d65102188862308aaefec1e49"
def is_clue_time_ok(id):
	return True
	import requests
	d=requests.get(CreateDate%id)
	tt=json.loads(d.content)
	judje=datetime.now()-timedelta(days=20)
	if (datetime.strptime(tt[0]['date'][0:10], '%Y-%m-%d'))<judje:
		return False
	return True
class TrelloTest(MethodView):
	def get(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		hello=""
		mail_pre=(Clue_Pre%("",'Clue Mail'))

		
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' and len(x.cards)>0:
				hello+=('''<div style="margin-bottom:12px;padding-bottom:11px">
					<span style="border-bottom:1px solid #dedede;padding-bottom:12px;color:#555;font-size:15px">%s</span>
				</div>''')%x.name
				x.cards.reverse()
				for y in x.cards:
							if not y.labels and is_clue_time_ok(y.id) :
												i+=1
												hello+=(Clue_Body%(("http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s")%(y.id,x.name),y.name,'''<a target="_blank" href="http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s" style="margin-left:10px;display:inline-block;padding:2px 5px;background-color:#d44b38;color:#fff;font-size:13px;font-weight:bold;border-radius:2px;border:solid 1px #c43b28;white-space:nowrap;text-decoration:none">领取</a>'''%(y.id,x.name),"","",y.desc))
												#hello+='%d:<a href="http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s">【认领】</a> %s<br/> %s<br/><br/>'%(i,y.id,x.name,y.name,y.desc)
												break
		hello+=Clue_End2

		return hello
class TrelloDone(MethodView):
	def get(self):
        
		id=request.args.get('id')
		card=TrelloConn.get_card(id)
		if card.labels:
			return u'orz 下手晚了，已经有人认领了'
		cat=request.args.get('cat')
		return render_template('clue_add.html',id=id,cat=cat)
	def post(self):
		name=request.form['name']
		id=request.form['id']
		due=request.form['due']
		cat=Labels[(request.form['cat'])]

		params = {'value': due}
		params2={'text':name}
		params3={'value':cat}
		TrelloConn.put(path='cards/%s/due'%id, params=params, body=None)
		TrelloConn.post(path='/cards/%s/actions/comments'%id,params=params2)
		TrelloConn.post(path='/cards/%s/labels'%id,params=params3)

		return 'ok'
class TrelloSend(MethodView):
	def  get(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		hello=""
		mail_pre=(Clue_Pre%(str(date.today()),'原创新闻线索'))
		hello+=mail_pre
		
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' and len(x.cards)>0:
				hello+=('''<div style="margin-bottom:12px;padding-bottom:11px">
					<span style="border-bottom:1px solid #dedede;padding-bottom:12px;color:#555;font-size:15px">%s</span>
				</div>''')%x.name
				x.cards.reverse()
				for y in x.cards:
					if not y.labels and is_clue_time_ok(y.id) :
						i+=1
						hello+=(Clue_Body%(("http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s")%(y.id,x.name),y.name,'''<a target="_blank" href="http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s" style="margin-left:10px;display:inline-block;padding:2px 5px;background-color:#d44b38;color:#fff;font-size:13px;font-weight:bold;border-radius:2px;border:solid 1px #c43b28;white-space:nowrap;text-decoration:none">领取</a>'''%(y.id,x.name),"","<br/>",y.desc))
						#hello+='%d:<a href="http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s">【认领】</a> %s<br/> %s<br/><br/>'%(i,y.id,x.name,y.name,y.desc)
						hello+="<br/><br/>"
                                                break
		hello+=Clue_End2
		mail=MailMethod()
		mail._send_default(to='arthur@infoq.com',subject="InfoQ新闻线索：%s"%str(datetime.today())[0:10],content=hello)
		return 'ok'
	def  post(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		hello=""
		mail_pre=(Clue_Pre%(str(date.today()),'原创新闻线索'))
		hello+=mail_pre
		
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' and len(x.cards)>0:
				hello+=('''<div style="margin-bottom:12px;padding-bottom:11px">
					<span style="border-bottom:1px solid #dedede;padding-bottom:12px;color:#555;font-size:15px">%s</span>
				</div>''')%x.name
				x.cards.reverse()
				for y in x.cards:
					if not y.labels and is_clue_time_ok(y.id) :
						i+=1
						hello+=(Clue_Body%(("http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s")%(y.id,x.name),y.name,'''<a target="_blank" href="http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s" style="margin-left:0px;display:inline-block;padding:2px 2px;background-color:#d44b38;color:#fff;font-size:13px;font-weight:bold;border-radius:2px;border:solid 1px #c43b28;white-space:nowrap;text-decoration:none">领取</a>'''%(y.id,x.name),"","<br/>",y.desc))
						#hello+='%d:<a href="http://infoqhelp.sinaapp.com/trellodone?id=%s&cat=%s">【认领】</a> %s<br/> %s<br/><br/>'%(i,y.id,x.name,y.name,y.desc)
						hello+="<br/><br/>"
                                                break
		hello+=Clue_End2
		mail=MailMethod()
		mail._send_default(to='core-editors@googlegroups.com',subject="InfoQ新闻线索：%s"%str(datetime.today())[0:10],content=hello)
		return 'ok'