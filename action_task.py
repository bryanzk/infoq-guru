# -*-coding: utf-8 -*-
from config import *
# 添加新的任务

class TaskHelper():
	# create id for task and status
	def next_step_exists(self,task_id,code):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		next_code=STATUS_STEP_LIST[str(code)]
		res=dbSession.query(StatusList).filter(StatusList.code==next_code).filter(StatusList.task_id==task_id).order_by(desc(StatusList.begin)).all()
		if res:
			return False
		else:
			return True
	def create_id(self):
		import md5
		return (md5.md5(str(datetime.now()))).hexdigest() 
	def task_init(self,task):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		begin=datetime.now()
		s=StatusList(id=self.create_id(),
			task_id=task.id,code=664,description='',
			begin=datetime.now(),
			end=begin,
			contrast='',
			editor=task.editor,
			duty=task.duty,count=0)
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
		'''select max(code),id,task_id,code,begin,end,contrast,editor,duty from status_list
			group by task_id
		use_list=dbSession.
		query(func.max(StatusList.code),StatusList.id,StatusList.task_id,StatusList.code,StatusList.begin,StatusList.end,StatusList.editor,StatusList.duty)\
		.filter(or_(and_(StatusList.code>=664,StatusList.end==0000-00-00 00:00:00),and_(and_(StatusList.code>660,StatusList.code<800),StatusList.end!='0000-00-00 00:00:00'))))\
		.group_by(StatusList.task_id).order_by(StatusList.begin).all()
		return render_template('task_step.html',use_list=use_list)
		
		use_664=dbSession.query(func.max(StatusList.code),StatusList.id,StatusList.task_id,StatusList.code,StatusList.begin,StatusList.end,StatusList.editor,StatusList.duty).filter(StatusList.code==664).group_by(StatusList.task_id).order_by(StatusList.begin).all()
		user_other=dbSession.query(func.max(StatusList.code),StatusList.id,StatusList.task_id,StatusList.code,StatusList.begin,StatusList.end,StatusList.editor,StatusList.duty).filter(StatusList.code>666).filter(StatusList.code<800).filter(StatusList.end).group_by(StatusList.task_id).order_by(StatusList.begin).all()
		'''
		use_list=[]
		helper=TaskHelper()
		use_od=dbSession.query(func.max(StatusList.code),StatusList.id,StatusList.task_id,StatusList.code,StatusList.begin,StatusList.end,StatusList.editor,StatusList.duty).group_by(StatusList.task_id).filter(StatusList.code>=664).filter(StatusList.code<=800).all()
		for x in use_od:
			if x[5]!="0000-00-00 00:00:00" and not helper.next_step_exists(x.task_id,x.code):
				use_list.append(x)

		return render_template('task_step.html',use_list=use_list)


	def post(self):
		'''
		'''
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()

		helper=TaskHelper()
		status_id=request.form['status_id']
		task_id=request.form['task_id']
		code=STATUS_STEP_LIST[request.form['code']]
		editor=request.form['editor']
		duty=request.form['duty']
		contrast=datetime.strptime(request.form['contrast']+" 00:00:00",'%Y-%m-%d %H:%M:%S')
		description=''
		begin=datetime.now()
		older=dbSession.query(StatusList).filter(StatusList.id==status_id).all()
		older[0].end=datetime.now()
		s=StatusList(id=helper.create_id(),task_id=task_id,
			code=code,
			description=description,
			begin=begin,
			end='',
			contrast=contrast,
			editor=editor,
			duty=duty,count=0)
		
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
		res=dbSession.query(TaskList).filter(TaskList.id==task_id).all()
		
		title=res[0].title
		link=res[0].link
		duty=res[0].duty
		return jsonify(msg='ok',title=title,link=link,duty=duty)

		
# 提交任务完成
class TaskSubmit(MethodView):
	def get(self):
		
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		res=dbSession.query(StatusList).filter(or_(StatusList.code>=664,StatusList.code<=780)).filter(StatusList.end=='0000-00-00 00:00:00').all()
		
		return render_template('task_submit.html',use_list=res)
		
	def post(self):
		id=request.form['id']
		count=request.form['count']
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		r=dbSession.query(StatusList).filter(StatusList.id==id).first()
		r.end=datetime.now()
		r.count=count
		dbSession.commit()
		return 'ok'
class TaskHistoryList(MethodView):
	def get(self):
		pass
class TaskSearch(MethodView):
	def get(self):
		pass
	def post(self):
		pass