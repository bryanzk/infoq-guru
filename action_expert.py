# coding: utf-8
from config import *
class ExpertHelper():
	def add_user(self,u):
		db_session=sessionmaker(bind=DB)
		dbSessin=db_session()
		uu=dbSessin.query(ExpertList).filter(ExpertList.id==u.id).all()
		if uu:
			dbSessin.delete(uu[0])
			dbSessin.commit()
			u.bid=uu[0].bid
			u.bank=uu[0].bank
			dbSessin.add(u)
			dbSessin.commit()
		else:
			dbSessin.add(u)
			dbSessin.commit()
		dbSessin.close()
		return True
	def get_user(self,id):
		db_session=sessionmaker(bind=DB)
		dbSessin=db_session()
		u=dbSessin.query(ExpertList).filter(ExpertList.id==id).all()
		dbSessin.close()
		u[0].birth=str(u[0].birth)[0:11]
		return u[0]
	def query_it(self,cat,query):
		db_session=sessionmaker(bind=DB)
		dbSessin=db_session()
		result=''
		if cat=='name':
			result=dbSessin.query(ExpertList).filter(ExpertList.name.like('%'+query+'%')).all()
		if cat=='city':
			result=dbSessin.query(ExpertList).filter(ExpertList.location.like('%'+query+'%')).all()
		if cat=='address':
			result=dbSessin.query(ExpertList).filter(ExpertList.address.like('%'+query+'%')).all()
		if cat=='bio':
			result=dbSessin.query(ExpertList).filter(ExpertList.bio.like('%'+query+'%')).all()
		if cat=='area':
			result=dbSessin.query(ExpertList).filter(ExpertList.area.like('%'+query+'%')).all()
		dbSessin.close()
		return result
	def create_id(self):
		import md5
		return (md5.md5(str(datetime.now()))).hexdigest() 

class ExpertShow(MethodView):
	def get(self):
		id=request.args.get('id')
		helper=ExpertHelper()
		u=helper.get_user(id)
		db_session=sessionmaker(bind=DB)
		dbSessin=db_session()
		return render_template('expert_show.html',x=u,r='')

class ExpertUpdate(MethodView):
	def get(self):
		id=request.args.get('id')
		helper=ExpertHelper()
		u=helper.get_user(id)
		db_session=sessionmaker(bind=DB)
		dbSessin=db_session()
		return render_template('expert_update.html',x=u,r='')
		
	def post(self):
		id=request.form['id']
		name=request.form['name']
		ename=request.form['ename']
		email=request.form['email']
		address=request.form['address']
		location=request.form['location']
		company=request.form['company']
		phone=request.form['phone']
		im=request.form['im']
		bank=''
		bio=request.form['bio']
		img=request.form['img']
		weibo=request.form['weibo']
		blog=request.form['blog']
		area=request.form['area']
		birth=datetime.strptime(request.form['birth']+" 00:00:00",'%Y-%m-%d %H:%M:%S')
		bid=''
		helper=ExpertHelper()
		u=ExpertList(id=id,name=name,
			ename=ename,email=email,
			address=address,
			location=location,
			company=company,
			phone=phone,
			im=im,bank=bank,
			bio=bio,img=img,
			weibo=weibo,
			blog=blog,
			area=area,birth=birth,bid=bid)
		helper.add_user(u)
		flash('修改成功')
		return redirect('eshow?id='+id)

class ExpertAdd(MethodView):
	def get(self):
		return render_template('expert_add.html')
		
	def post(self):
		name=request.form['name']
		ename=request.form['ename']
		email=request.form['email']
		address=request.form['address']
		location=request.form['location']
		company=request.form['company']
		phone=request.form['phone']
		im=request.form['im']
		bank=request.form['bank']
		bio=request.form['bio']
		img=request.form['img']
		weibo=request.form['weibo']
		blog=request.form['blog']
		area=request.form['area']
		birth=datetime.strptime(request.form['birth']+" 00:00:00",'%Y-%m-%d %H:%M:%S')
		bid=request.form['bid']
		helper=ExpertHelper()
		u=ExpertList(id=helper.create_id(),name=name,
			ename=ename,email=email,
			address=address,
			location=location,
			company=company,
			phone=phone,
			im=im,bank=bank,
			bio=bio,img=img,
			weibo=weibo,
			blog=blog,
			area=area,birth=birth,bid=bid)
		helper.add_user(u)
		flash('修改成功')
		return redirect('eshow?id='+str(id))

class ExpertSearch(MethodView):
	def get(self):
		return render_template('expert_search.html')
	def post(self):
		cat=request.form['cat']
		query=request.form['query']
		helper=ExpertHelper()
		result=helper.query_it(cat,query)
		return render_template('expert_search.html',res=result)
