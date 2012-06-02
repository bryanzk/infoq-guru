# coding: utf8
from config import *
import requests as httprequest
class TopView2(MethodView):
	def get(self):
		return render_template('top_urls.html')
	def post(self):
		urls=request.form['urls']
		urls_list=urls.replace('\r\n','').split(',')
		helper=TopHelp2()
		res=[]
		ii=0
		for x in urls_list:
			ii+=1
			title,link,content=helper.getitem(x)
			rr=UrlList(title=title,content=content,link=link)
			res.append(rr)
		return render_template('top_urls.html',res=res)
class TopHelp2():
	def getitem(self,url):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
                url2="http://www.infoq.com"+url
		results=dbSession.query(RssInfo).filter(RssInfo.guid==url2).first()
		return results.title,results.guid,results.description
class TopHelp():
	def getitem(self,url):
		url_new="https://www.googleapis.com/customsearch/v1?key=AIzaSyBChvjEv_rFz2c2wniE3xAJAJc6jaNOryM&cx=013036536707430787589:_pqjad5hr1a&q=\
					%s&alt=json" %url
		data=httprequest.get(url_new)
		j=json.loads(data.text)
		return j['items'][0]["title"],j['items'][0]['link'],j['items'][0]['snippet']
class UrlList():
	def __init__(self,title,content,link):
		self.title=title
		self.content=content
		self.link=link
class TopView(MethodView):
	def get(self):
		return render_template('top_urls.html')
	def post(self):
		urls=request.form['urls']
		urls_list=urls.split(',')
		helper=TopHelp()
		res=[]
		for x in urls_list:
			title,link,content=helper.getitem(x)
			rr=UrlList(title=title,content=content,link=link)
			res.append(rr)
		return render_template('top_urls.html',res=res)

