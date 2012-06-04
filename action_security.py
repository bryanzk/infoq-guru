# coding: utf-8
# this is for security
import config
class SecurityList(Base):
	__tablename__='security_list'
	name=Column(String(100),primary_key=True)
	type=Column(String(45))
	pwd=Column(String(45))
	def __init__(self,name,type,pwd):
		self.name=name
		self.type=type
		self.pwd=pwd
class InfoQSecurity():
	def auth(self):
		if 'user' in session:
			user=session['user']
			if user!='':
				return True
			else self.goauth()
		else:
			self.goauth()
	def goauth(self):
		session['user']=SecurityList(name='',type='',pwd='')
		return redirect('/login')
