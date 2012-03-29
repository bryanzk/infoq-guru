# -*-coding: utf-8 -*-
from config import *
# 添加新的任务
class TaskAddNew(MethodView):
	def get(self):
		pass
	def post(self):
		bigcat=request.form['bigcat']
		smallcat=request.form['smallcat']
		title=request.form['title']
		link=request.form['link']
		created=request.form['created']
		duty=request.form['duty']
		editor=request.form['editor']
		t=TaskList(bigcat=bigcat,
			smallcat=smallcat,
			title=title,
			link=link,
			created=created,
			editor=editor,duty=duty,count=0)
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		dbSession.add(t)
		dbSession.commit()
		return "{'status':'ok'}"

'''
step 0 初始任务：
	status code: 664
step 1 制作中：将任务给某一个人
	status code： 737
step 2 审核中：给某人审核
	status code: 780
step 3 排期中：排期
	status code: 800
	选取前两个
'''
class TaskToStep(MethodView):
	def get(self):
		'''获取任务code为664,737和780的任务，其editor为空'''
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		use_list=dbSession.disc(StatusList.task_id).query(StatusList).filter(StatusList.code<800).filter(StatusList.editor=='').filter(StatusList.end=='').all()
		return use_list
	def post(self):
		status_id=request.form['status_id']
		code=request.form['code']
		editor=request.form['editor']
		duty=request.form['duty']
		contrast=request.form['contrast']
		description=''
		begin=datetime.now()
		s=StatusList(id,status_id=status_id,
			code=code,
			description=description,
			begin=begin,
			end='',
			contrast=contrast,
			editor=editor,
			duty=duty)
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		dbSession.add(s)
		dbSession.commit()
		return "{'status':'ok'}"
'''
获取一个任务的信息
'''
class TaskStepInfo(MethodView):
	"""docstring for TaskInfo"""
	def get(self):
		pass
	def post(self):
		task_id=request.form['id']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(StatusList).filter(StatusList.task_id==task_id).all()
		return res

		
# 提交任务完成
class TaskSubmit(MethodView):
	def get(self):
		pass
	def post(self):
		id=request.form['id']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(StatusList).filter(StatusList.id==id).first()
		r.end=datetime.now()
		dbSession.commit()
		return 'ok'

class TaskSearch(MethodView):
	def get(self):
		pass
	def post(self):
		pass