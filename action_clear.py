# coding: utf-8
import config 
from flask import escape
from config import *
import requests as requ
class ClearIt(MethodView):
	def get(self):
		url=request.args.get('url')
		data=requ.get('http://api.thequeue.org/v1/clear?url=%s'%url)
		to=data.text
		ren=BeautifulSoup(to)
		raise
		datat=escape(ren.item.description)
		return render_template('clear_html.html',ren=datat)
	def escape(self,html):
		"""Returns the given HTML with ampersands, quotes and carets encoded."""
		return html.replace('&amp;','&').replace('&lt;','<').replace( '&gt;','>').replace( '&quot;','"').replace( '&#39;',"'")
