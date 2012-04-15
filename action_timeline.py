# coding: utf-8
from config import *
class TimeLine(MethodView):
	def get(self):
		return render_template('time_index.html')

class TimeLineData(MethodView):
	def get(self):
		db_session=sessionmaker(bind=DB)
		dbSession=db_session()
		li=dbSession.query(RssInfo).filter(RssInfo.country=='ch').all()
		xx=""
		da="""{
"startDate":"%s",
"headline":"%s",
"text":"<a href='%s'>文章链接</a>",
"asset":
{
"media":"http://cdn3.infoq.com/styles/cn/i/logo-infoq.gif",
"credit":"",
"caption":"%s"
}
}"""
		i=0
		count=0
		for x in li:
			count+=1
		for x in li:
			i+=1
			xx+=(da % (((str(x.pubdate))[0:10]).replace('-',',')+""+((str(x.pubdate))[11:13]),x.title.replace("?",""),x.guid,x.description[0:80]))
			if i!=count:
				xx+=','



		return """{
    "timeline":
    {
        "headline":"数据Timeline",
        "type":"default",
		"startDate":"2012,3,26 11:30",
		"text":"数据展示时间线。",
        "date": [
            """+xx+"""
        ]
    }
}
		"""