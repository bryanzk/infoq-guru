import requests
import bs4
from config import *
from bs4 import BeautifulSoup

SEARCH_URL='http://movie.douban.com/tv/calendar/%s/'

class MeijuView(MethodView):
	def get(self):
        	return render_template('meiju.html')
        def post(self):
        	date=request.form['date']
                res=BeautifulSoup((requests.get(SEARCH_URL % date)).text)
                r=res.find('table',{'class':'series_list'})
                x=r.findAll('a',{"class":"report"})
                rr=[]
                for xx in x:
                	rr.append(xx['data-sname'])
                return render_template('meiju.html',r=rr)