# coding: utf-8
import config
from config import *

from trollop import TrelloConnection
from action_mail import *
TrelloConn = TrelloConnection("47285d38ecf695f600ddabd7978a7355","02a2c4c83e0e47b6b4d6cc3337d85547fdb9b56d65102188862308aaefec1e49")
Labels={u"\u8bed\u8a00":"green",u"\u67b6\u6784 ":"yellow",u"\u8fc7\u7a0b":"orange",u"\u8fd0\u7ef4":"red",u"企业架构":"purple","Done":"blue"}


# todo 
class Editor_Clue_Get(MethodView):
	def get(self):
		board=TrelloConn.get_board("4fa88ccdb6aaa61c484ac7cf")
		lists=board.lists
		for x in lists:
			i=0
			if x.name!='Done' and x.name!='Doing' :
				for y in x.cards:
					if not y.labels :
						c=ClueList(id=y.id,cat=x.name,title=y.name,description=y.desc)
						try:
							db_session=sessionmaker(bind=DB)
							dbSession=db_session()
							dbSession.add(c)
							dbSession.commit()
							i+=1
						except:
							print ''
		return 'ok'



# get clues all
class Editor_Clue_All(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).all()
		return render_template('editor_clue_all.html',res=res)
	def post(self):
		pass
# get clue pick and input the due date
class Editor_Clue_Pick(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.id==request.args.get('id')).all()
		return render_template('editor_clue_pick.html',res=res[0])
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.id==request.form['id']).all()
		res[0].duedate=request.form['duedate']
		res[0].duty_editor=session['user'].user
		res[0].staus='pending'
		dbSession.commit()
		return redirect('/')

# get all my pending 
class Editor_Clue_Mine_Pending(MethodView):
	@login(wtype='core-editor')
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.duty_editor==session['user'].user).filter(ClueList.staus=='pending').all()
		return render_template('editor_clue_mine_pending.html',res=res)

class Editor_Clue_Mine_Pending_Done(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.id==request.args.get('id')).all()
		res[0].chief_editor='123'
		#request.form['chief_editor']
		res[0].staus='review'
		dbSession.commit()
		return redirect('/')

class Editor_Clue_Mine_Done(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.duty_editor==session['user'].user).filter(ClueList.staus=='done').all()
		return render_template('editor_clue_mine_done.html',res=res)

	
# core-editor
class Editor_Clue_Review(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.duty_editor==session['user'].user).filter(ClueList.staus=='review').all()
		return render_template('editor_clue_review.html',res=res)
	def post(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(ClueList).filter(ClueList.id==request.form['id']).all()
		res[0].staus='done'
		dbSession.commit()
		return redirect('/')