# -*-coding: utf-8 -*-
from config import *
# 添加新的任务

class TaskHelper():
	# create id for task and status
	def create_id(self):
		import md5
		return (md5.md5(str(datetime.now()))).hexdigest() 
	def task_init(self,task):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		s=StatusList(id=self.create_id(),
			task_id=task.id,code=664,description='',
			begin=datetime.now(),
			end=begin,
			contrast='',
			editor=task.editor,
			duty=task.duty)
		dbSession.add(s)
		dbSession.commit()
class TaskAddNew(MethodView):
	def get(self):
		
		return render_template('task_add.html',msg='')
	def post(self):
		helper=TaskHelper()
		bigcat=request.form['bigcat']
		smallcat=request.form['smallcat']
		title=request.form['title']
		link=request.form['link']
		duty=request.form['duty']
		editor=request.form['editor']
		t=TaskList(id=helper.create_id(),bigcat=bigcat,
			smallcat=smallcat,
			title=title,
			link=link,
			editor=editor,duty=duty,count=0)
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		dbSession.add(t)
		dbSession.commit()
		helper.task_init(t)
		return "{'status':'ok'}"
class TaskCanBack(MethodView):
	def get(self):
		pass
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
		use_list=dbSession.query(StatusList).filter(StatusList.code>=664).filter(StatusList.code<=780).filter(StatusList.end!='').order_by(StatusList.begin).all()
		
		return render_template('task_step.html',use_list=use_list)
	def post(self):
		'''
		'''
		helper=TaskHelper()
		task_id=request.form['task_id']
		code=STATUS_STEP_LIST[request.form['code']]
		editor=request.form['editor']
		duty=request.form['duty']
		contrast=datetime.strptime(request.form['contrast']+" 00:00:00",'%Y-%m-%d %H:%M:%S')
		description=''
		begin=datetime.now()
		s=StatusList(id=helper.create_id(),task_id=task_id,
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
		task_id=request.form['task_id']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(TaskList).filter(TaskList.id==task_id).first()
		
		return jsonify(msg='ok',res=res)

		
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