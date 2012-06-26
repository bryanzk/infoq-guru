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
			xx+=(da % (((str(x.pubdate))[0:10]).replace('-',','),x.title.replace("?",""),x.guid,x.description[0:80]))
			if i!=count:
				xx+=','



		return """{
    "timeline":
    {
        "headline":"InfoQ内容发布时间轴--beta",
        "type":"default",
		"startDate":"2012",
		"text":"通过时间轴直接明了的展示InfoQ的内容发布情况。",
        "date": [
            """+xx+"""
        ]
    }
}
		"""